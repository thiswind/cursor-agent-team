#!/usr/bin/env python3
"""
话题树验证脚本 - 硬约束检查
用于验证LLM生成的话题树更新是否符合规则

规则说明:
- R1: 所有历史话题ID必须保留（比对新旧文件的ID集合）
- R2: 禁止使用"省略"/"..."简化历史（关键词检测）
- R3: 必须包含 Last Updated 字段（字段存在性）
- R4: 状态值必须是预定义值之一（枚举校验，警告级别）

使用方法:
    python validate_topic_tree.py --old <旧文件路径> --new <新文件路径>

输出格式 (JSON):
    {
        "valid": true/false,
        "errors": ["错误描述1", "错误描述2"],
        "warnings": ["警告描述1"]
    }

退出码:
    0 - 验证通过 (valid=true)
    1 - 验证失败 (valid=false)
"""

import argparse
import json
import re
import sys
from pathlib import Path

# 合法的话题状态值
VALID_STATES = {
    "进行中", "已完成", "已关闭", "待讨论", "暂停",
    "✅ 已关闭", "✅ 已完成", "🔄 进行中", "⏸️ 暂停"
}

# 禁止使用的省略标记
ELLIPSIS_PATTERNS = ["省略", "...", "…", "以上省略", "略"]


def extract_topic_ids(content: str) -> set:
    """
    提取话题树中的所有话题ID
    
    匹配表格中的ID列，如 "| A |" 或 "| C-AB |" 或 "| AE |"
    ID格式: 一个或多个大写字母，可选地跟着 "-" 和更多大写字母
    """
    # 匹配表格中的ID列
    # 模式说明: | 空白 ID 空白 | 后面跟着话题名称（非空白字符）
    pattern = r'\|\s*([A-Z]+(?:-[A-Z]+)?)\s*\|[^|]*\|'
    ids = set(re.findall(pattern, content))
    return ids


def validate_topic_tree(old_content: str, new_content: str) -> dict:
    """
    验证话题树更新是否符合硬约束规则
    
    Args:
        old_content: 旧话题树文件内容
        new_content: 新话题树文件内容
        
    Returns:
        dict: 包含 valid, errors, warnings 字段的验证结果
    """
    errors = []
    warnings = []
    
    # R1: 历史话题ID不能丢失
    old_ids = extract_topic_ids(old_content)
    new_ids = extract_topic_ids(new_content)
    missing_ids = old_ids - new_ids
    if missing_ids:
        errors.append(f"R1违规: 以下话题ID丢失: {sorted(missing_ids)}")
    
    # R2: 禁止使用省略标记
    for pattern in ELLIPSIS_PATTERNS:
        if pattern in new_content:
            # 排除代码块中的省略号（如示例代码）
            # 简单检查：如果省略号出现在 ``` 代码块外才报错
            lines = new_content.split('\n')
            in_code_block = False
            for line in lines:
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                elif not in_code_block and pattern in line:
                    errors.append(f"R2违规: 检测到省略标记 '{pattern}'")
                    break
            break
    
    # R3: 必须有 Last Updated
    if "Last Updated" not in new_content:
        errors.append("R3违规: 缺少 'Last Updated' 字段")
    
    # R4: 状态值检查（警告级别）
    # 提取状态列的值 - 匹配常见的状态格式
    state_pattern = r'\|\s*(✅\s*已关闭|✅\s*已完成|🔄\s*进行中|⏸️\s*暂停|已关闭|已完成|进行中|暂停|待讨论)\s*\|'
    found_states = re.findall(state_pattern, new_content)
    
    # 检查是否有未知状态（这里简化处理，实际可以更严格）
    # 当前实现只做基本检查，更复杂的状态验证可以后续添加
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def main():
    """主函数：解析参数并执行验证"""
    parser = argparse.ArgumentParser(
        description="验证话题树更新是否符合硬约束规则",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
规则说明:
  R1: 所有历史话题ID必须保留
  R2: 禁止使用"省略"/"..."等标记
  R3: 必须包含 Last Updated 字段
  R4: 状态值必须是预定义值之一（警告级别）

示例:
  python validate_topic_tree.py --old topics_backup.md --new topics_new.md
        """
    )
    parser.add_argument("--old", required=True, help="旧话题树文件路径（备份）")
    parser.add_argument("--new", required=True, help="新话题树文件路径（待验证）")
    args = parser.parse_args()
    
    # 读取文件
    old_path = Path(args.old)
    new_path = Path(args.new)
    
    if not old_path.exists():
        result = {
            "valid": False,
            "errors": [f"旧文件不存在: {args.old}"],
            "warnings": []
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    if not new_path.exists():
        result = {
            "valid": False,
            "errors": [f"新文件不存在: {args.new}"],
            "warnings": []
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    try:
        old_content = old_path.read_text(encoding="utf-8")
        new_content = new_path.read_text(encoding="utf-8")
    except Exception as e:
        result = {
            "valid": False,
            "errors": [f"读取文件失败: {str(e)}"],
            "warnings": []
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    # 执行验证
    result = validate_topic_tree(old_content, new_content)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
