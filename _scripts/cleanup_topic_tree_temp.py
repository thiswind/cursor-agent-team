#!/usr/bin/env python3
"""
话题树临时文件清理脚本 - 安全删除临时文件

此脚本用于清理话题树验证流程产生的临时文件。
通过白名单机制确保只能删除特定文件，防止误删。

使用方法:
    python cleanup_topic_tree_temp.py [选项]

选项:
    --dry-run     仅显示将删除的文件，不实际删除
    --all         清理所有临时文件（匹配扩展白名单）
    --quiet       静默模式，不输出到终端（仍写日志）
    --help        显示帮助信息

输出格式 (JSON):
    {
        "success": true/false,
        "deleted": ["file1.md", "file2.md"],
        "skipped": ["file3.md"],
        "dry_run": true/false,
        "log_file": "ai_workspace/temp/cleanup.log"
    }

退出码:
    0 - 成功
    1 - 失败
"""

import argparse
import fnmatch
import json
import os
import sys
from datetime import datetime
from pathlib import Path


# 白名单文件（硬编码，安全边界）
ALLOWED_FILES = {
    "discussion_topics.md.bak",
    "new_topic_tree.md",
}

# 扩展白名单模式（--all 模式）
EXTENDED_PATTERNS = [
    "*.bak",
    "*.tmp",
]

# 相对于脚本位置的临时目录路径
TEMP_DIR_RELATIVE = "../ai_workspace/temp"


def get_temp_dir() -> Path:
    """获取临时文件目录的绝对路径"""
    script_dir = Path(__file__).parent.resolve()
    temp_dir = (script_dir / TEMP_DIR_RELATIVE).resolve()
    return temp_dir


def get_log_file(temp_dir: Path) -> Path:
    """获取日志文件路径"""
    return temp_dir / "cleanup.log"


def write_log(log_file: Path, message: str):
    """写入日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    # 确保目录存在
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)


def is_file_allowed(filename: str, use_extended: bool = False) -> bool:
    """检查文件是否在白名单中"""
    # 检查基本白名单
    if filename in ALLOWED_FILES:
        return True
    
    # 如果使用扩展模式，检查扩展白名单
    if use_extended:
        for pattern in EXTENDED_PATTERNS:
            if fnmatch.fnmatch(filename, pattern):
                return True
    
    return False


def cleanup_temp_files(
    dry_run: bool = False,
    use_all: bool = False,
    quiet: bool = False
) -> dict:
    """
    清理临时文件
    
    Args:
        dry_run: 是否只预览不实际删除
        use_all: 是否使用扩展白名单
        quiet: 是否静默模式
    
    Returns:
        dict: 包含清理结果的字典
    """
    temp_dir = get_temp_dir()
    log_file = get_log_file(temp_dir)
    
    result = {
        "success": True,
        "deleted": [],
        "skipped": [],
        "dry_run": dry_run,
        "log_file": str(log_file.relative_to(temp_dir.parent.parent))
    }
    
    # 检查目录是否存在
    if not temp_dir.exists():
        # 目录不存在，创建它并返回成功（无需删除）
        temp_dir.mkdir(parents=True, exist_ok=True)
        write_log(log_file, "INIT: Created temp directory (was missing)")
        return result
    
    # 遍历目录中的文件
    for item in temp_dir.iterdir():
        if not item.is_file():
            continue
        
        filename = item.name
        
        # 跳过日志文件本身
        if filename == "cleanup.log":
            continue
        
        # 检查是否在白名单中
        if is_file_allowed(filename, use_all):
            if dry_run:
                result["deleted"].append(filename)
                write_log(log_file, f"DRY-RUN: Would delete {filename}")
            else:
                try:
                    item.unlink()
                    result["deleted"].append(filename)
                    write_log(log_file, f"DELETED: {filename}")
                except Exception as e:
                    result["skipped"].append(filename)
                    result["success"] = False
                    write_log(log_file, f"ERROR: Failed to delete {filename}: {e}")
        else:
            result["skipped"].append(filename)
            write_log(log_file, f"SKIPPED: {filename} (not in whitelist)")
    
    return result


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="清理话题树验证流程产生的临时文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
安全机制:
  - 白名单限制：只能删除预定义的文件名（硬编码）
  - 路径限制：只能操作 ai_workspace/temp/ 目录
  - 无任意路径暴露：无法通过参数删除其他文件

示例:
  python cleanup_topic_tree_temp.py              # 基本清理
  python cleanup_topic_tree_temp.py --dry-run    # 预览模式
  python cleanup_topic_tree_temp.py --all        # 扩展清理
  python cleanup_topic_tree_temp.py --quiet      # 静默模式
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅显示将删除的文件，不实际删除"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="清理所有临时文件（匹配扩展白名单 *.bak, *.tmp）"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="静默模式，不输出到终端（仍写日志）"
    )
    
    args = parser.parse_args()
    
    # 执行清理
    result = cleanup_temp_files(
        dry_run=args.dry_run,
        use_all=args.all,
        quiet=args.quiet
    )
    
    # 输出结果
    if not args.quiet:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 返回退出码
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
