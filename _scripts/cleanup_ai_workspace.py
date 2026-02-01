#!/usr/bin/env python3
"""
AI Workspace 安全删除脚本 - 受限的文件清理工具

此脚本允许智能体安全地删除 ai_workspace/ 目录内的文件，
同时确保无法删除目录外的任何内容。

安全机制：
  - 路径硬编码：只能操作 ../ai_workspace/ 目录
  - 路径验证：所有目标路径必须解析后落在 ai_workspace/ 内
  - 保护名单：某些关键文件不可删除（除非使用 --force）
  - 日志记录：所有操作记录到 ai_workspace/temp/cleanup.log

使用方法:
    python cleanup_ai_workspace.py [选项]

选项:
    --file <path>       删除指定文件（相对于 ai_workspace/）
    --dir <path>        删除指定目录（递归删除）
    --pattern <glob>    按模式删除（如 *.bak, *.tmp）
    --older-than <days> 删除N天前的文件
    --dry-run           预览模式，不实际删除
    --quiet             静默模式，不输出到终端（仍写日志）
    --force             强制删除（包括保护文件，需谨慎）
    --help              显示帮助信息

输出格式 (JSON):
    {
        "success": true/false,
        "deleted": ["file1.md", "temp/file2.txt"],
        "skipped": [],
        "protected": ["README.md"],
        "errors": [],
        "dry_run": false,
        "log_file": "ai_workspace/temp/cleanup.log"
    }

退出码:
    0 - 成功
    1 - 失败（参数错误、权限问题等）
    2 - 部分失败（某些文件删除失败）
"""

import argparse
import fnmatch
import json
import os
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Set


# 保护名单（硬编码，这些文件默认不可删除）
PROTECTED_FILES: Set[str] = {
    "README.md",
    "crew/README.md",
    "plans/README.md",
    "plans/INDEX.md",
    "prompt_engineer/README.md",
    "discussion_topics.md",
}

# 相对于脚本位置的 ai_workspace 目录路径
WORKSPACE_DIR_RELATIVE = "../ai_workspace"


def get_workspace_dir() -> Path:
    """获取 ai_workspace 目录的绝对路径"""
    script_dir = Path(__file__).parent.resolve()
    workspace_dir = (script_dir / WORKSPACE_DIR_RELATIVE).resolve()
    return workspace_dir


def get_log_file(workspace_dir: Path) -> Path:
    """获取日志文件路径"""
    temp_dir = workspace_dir / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / "cleanup.log"


def write_log(log_file: Path, message: str):
    """写入日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    # 确保目录存在
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)


def is_path_safe(target_path: Path, workspace_dir: Path) -> bool:
    """
    检查目标路径是否安全（在 ai_workspace 目录内）
    
    防止路径逃逸攻击（如 ../../../etc/passwd）
    """
    try:
        # 解析为绝对路径
        resolved_target = target_path.resolve()
        resolved_workspace = workspace_dir.resolve()
        
        # 检查目标路径是否在 workspace 目录内
        # 使用 is_relative_to（Python 3.9+）或手动检查
        try:
            resolved_target.relative_to(resolved_workspace)
            return True
        except ValueError:
            return False
    except Exception:
        return False


def is_protected(relative_path: str, force: bool = False) -> bool:
    """
    检查文件是否在保护名单中
    
    Args:
        relative_path: 相对于 ai_workspace 的路径
        force: 是否强制模式（忽略保护）
    
    Returns:
        True 如果文件被保护且非强制模式
    """
    if force:
        return False
    
    # 规范化路径分隔符
    normalized = relative_path.replace("\\", "/")
    return normalized in PROTECTED_FILES


def delete_file(
    file_path: Path,
    workspace_dir: Path,
    dry_run: bool,
    force: bool,
    log_file: Path
) -> dict:
    """
    删除单个文件
    
    Returns:
        dict: {"status": "deleted"|"protected"|"skipped"|"error", "path": str, "message": str}
    """
    try:
        relative_path = str(file_path.relative_to(workspace_dir))
    except ValueError:
        relative_path = str(file_path)
    
    # 检查路径安全
    if not is_path_safe(file_path, workspace_dir):
        write_log(log_file, f"REJECTED: {relative_path} (path escape attempt)")
        return {
            "status": "error",
            "path": relative_path,
            "message": "路径逃逸被拒绝：目标不在 ai_workspace/ 目录内"
        }
    
    # 检查文件是否存在
    if not file_path.exists():
        write_log(log_file, f"SKIPPED: {relative_path} (not found)")
        return {
            "status": "skipped",
            "path": relative_path,
            "message": "文件不存在"
        }
    
    # 检查是否被保护
    if is_protected(relative_path, force):
        write_log(log_file, f"PROTECTED: {relative_path}")
        return {
            "status": "protected",
            "path": relative_path,
            "message": "文件在保护名单中，使用 --force 强制删除"
        }
    
    # 执行删除
    if dry_run:
        write_log(log_file, f"DRY-RUN: Would delete {relative_path}")
        return {
            "status": "deleted",
            "path": relative_path,
            "message": "预览模式：将被删除"
        }
    else:
        try:
            if file_path.is_dir():
                shutil.rmtree(file_path)
            else:
                file_path.unlink()
            write_log(log_file, f"DELETED: {relative_path}")
            return {
                "status": "deleted",
                "path": relative_path,
                "message": "已删除"
            }
        except Exception as e:
            write_log(log_file, f"ERROR: Failed to delete {relative_path}: {e}")
            return {
                "status": "error",
                "path": relative_path,
                "message": f"删除失败: {e}"
            }


def delete_directory(
    dir_path: Path,
    workspace_dir: Path,
    dry_run: bool,
    force: bool,
    log_file: Path
) -> List[dict]:
    """
    递归删除目录
    
    Returns:
        List[dict]: 每个文件/目录的删除结果
    """
    results = []
    
    try:
        relative_path = str(dir_path.relative_to(workspace_dir))
    except ValueError:
        relative_path = str(dir_path)
    
    # 检查路径安全
    if not is_path_safe(dir_path, workspace_dir):
        write_log(log_file, f"REJECTED: {relative_path} (path escape attempt)")
        return [{
            "status": "error",
            "path": relative_path,
            "message": "路径逃逸被拒绝：目标不在 ai_workspace/ 目录内"
        }]
    
    # 检查目录是否存在
    if not dir_path.exists():
        write_log(log_file, f"SKIPPED: {relative_path} (not found)")
        return [{
            "status": "skipped",
            "path": relative_path,
            "message": "目录不存在"
        }]
    
    if not dir_path.is_dir():
        # 如果是文件，当作文件处理
        return [delete_file(dir_path, workspace_dir, dry_run, force, log_file)]
    
    # 收集目录内所有文件
    protected_found = []
    files_to_delete = []
    
    for item in dir_path.rglob("*"):
        if item.is_file():
            try:
                item_relative = str(item.relative_to(workspace_dir))
            except ValueError:
                item_relative = str(item)
            
            if is_protected(item_relative, force):
                protected_found.append(item_relative)
            else:
                files_to_delete.append(item)
    
    # 如果有保护文件且非强制模式，拒绝删除整个目录
    if protected_found and not force:
        for p in protected_found:
            results.append({
                "status": "protected",
                "path": p,
                "message": "文件在保护名单中"
            })
        write_log(log_file, f"REJECTED: Cannot delete {relative_path} (contains protected files: {protected_found})")
        return results
    
    # 执行删除
    if dry_run:
        write_log(log_file, f"DRY-RUN: Would delete directory {relative_path}")
        results.append({
            "status": "deleted",
            "path": relative_path,
            "message": "预览模式：目录将被删除"
        })
    else:
        try:
            shutil.rmtree(dir_path)
            write_log(log_file, f"DELETED: directory {relative_path}")
            results.append({
                "status": "deleted",
                "path": relative_path,
                "message": "目录已删除"
            })
        except Exception as e:
            write_log(log_file, f"ERROR: Failed to delete directory {relative_path}: {e}")
            results.append({
                "status": "error",
                "path": relative_path,
                "message": f"删除失败: {e}"
            })
    
    return results


def delete_by_pattern(
    pattern: str,
    workspace_dir: Path,
    dry_run: bool,
    force: bool,
    log_file: Path
) -> List[dict]:
    """
    按模式删除文件
    
    Args:
        pattern: glob 模式（如 *.bak, temp/*.tmp）
    
    Returns:
        List[dict]: 每个文件的删除结果
    """
    results = []
    
    # 使用 glob 查找匹配的文件
    for item in workspace_dir.rglob(pattern):
        if item.is_file():
            result = delete_file(item, workspace_dir, dry_run, force, log_file)
            results.append(result)
    
    if not results:
        write_log(log_file, f"PATTERN: No files matched '{pattern}'")
    
    return results


def delete_older_than(
    days: int,
    workspace_dir: Path,
    dry_run: bool,
    force: bool,
    log_file: Path
) -> List[dict]:
    """
    删除 N 天前的文件
    
    Args:
        days: 天数阈值
    
    Returns:
        List[dict]: 每个文件的删除结果
    """
    results = []
    cutoff_time = datetime.now() - timedelta(days=days)
    
    for item in workspace_dir.rglob("*"):
        if item.is_file():
            # 获取文件修改时间
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            if mtime < cutoff_time:
                result = delete_file(item, workspace_dir, dry_run, force, log_file)
                results.append(result)
    
    if not results:
        write_log(log_file, f"OLDER-THAN: No files older than {days} days")
    
    return results


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="AI Workspace 安全删除脚本 - 受限的文件清理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
安全机制:
  - 路径硬编码：只能操作 ai_workspace/ 目录
  - 路径验证：防止路径逃逸攻击（如 ../../../etc/passwd）
  - 保护名单：README.md、discussion_topics.md 等关键文件默认不可删除
  - 日志记录：所有操作记录到 ai_workspace/temp/cleanup.log

示例:
  python cleanup_ai_workspace.py --file temp/old_note.md
  python cleanup_ai_workspace.py --dir temp/test_cleanup
  python cleanup_ai_workspace.py --pattern "*.bak"
  python cleanup_ai_workspace.py --older-than 7
  python cleanup_ai_workspace.py --dry-run --pattern "*.tmp"
  python cleanup_ai_workspace.py --file README.md --force  # 危险！
        """
    )
    
    # 互斥的删除目标参数
    target_group = parser.add_mutually_exclusive_group()
    target_group.add_argument(
        "--file",
        type=str,
        help="删除指定文件（相对于 ai_workspace/）"
    )
    target_group.add_argument(
        "--dir",
        type=str,
        help="删除指定目录（递归删除）"
    )
    target_group.add_argument(
        "--pattern",
        type=str,
        help="按 glob 模式删除（如 *.bak, temp/*.tmp）"
    )
    target_group.add_argument(
        "--older-than",
        type=int,
        metavar="DAYS",
        help="删除 N 天前的文件"
    )
    
    # 其他选项
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览模式，不实际删除"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="静默模式，不输出到终端（仍写日志）"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制删除（包括保护文件，需谨慎）"
    )
    
    args = parser.parse_args()
    
    # 检查是否指定了删除目标
    if not any([args.file, args.dir, args.pattern, args.older_than]):
        parser.print_help()
        sys.exit(1)
    
    # 初始化
    workspace_dir = get_workspace_dir()
    log_file = get_log_file(workspace_dir)
    
    # 检查 workspace 目录是否存在
    if not workspace_dir.exists():
        result = {
            "success": False,
            "deleted": [],
            "skipped": [],
            "protected": [],
            "errors": ["ai_workspace/ 目录不存在"],
            "dry_run": args.dry_run,
            "log_file": str(log_file.relative_to(workspace_dir.parent))
        }
        if not args.quiet:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    # 执行删除操作
    results = []
    
    if args.file:
        target_path = workspace_dir / args.file
        results.append(delete_file(target_path, workspace_dir, args.dry_run, args.force, log_file))
    
    elif args.dir:
        target_path = workspace_dir / args.dir
        results.extend(delete_directory(target_path, workspace_dir, args.dry_run, args.force, log_file))
    
    elif args.pattern:
        results.extend(delete_by_pattern(args.pattern, workspace_dir, args.dry_run, args.force, log_file))
    
    elif args.older_than:
        results.extend(delete_older_than(args.older_than, workspace_dir, args.dry_run, args.force, log_file))
    
    # 汇总结果
    deleted = [r["path"] for r in results if r["status"] == "deleted"]
    skipped = [r["path"] for r in results if r["status"] == "skipped"]
    protected = [r["path"] for r in results if r["status"] == "protected"]
    errors = [f"{r['path']}: {r['message']}" for r in results if r["status"] == "error"]
    
    success = len(errors) == 0
    
    output = {
        "success": success,
        "deleted": deleted,
        "skipped": skipped,
        "protected": protected,
        "errors": errors,
        "dry_run": args.dry_run,
        "log_file": str(log_file.relative_to(workspace_dir.parent))
    }
    
    # 输出结果
    if not args.quiet:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    
    # 返回退出码
    if not success:
        if deleted:
            sys.exit(2)  # 部分失败
        else:
            sys.exit(1)  # 完全失败
    sys.exit(0)


if __name__ == "__main__":
    main()
