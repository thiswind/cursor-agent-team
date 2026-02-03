#!/usr/bin/env python3
"""
Preflight Check - AI Agent 预飞检查系统

在所有角色启动时自动运行，提供：
1. 当前时间
2. 工作区状态检查
3. 操作约定提醒

核心理念：用脚本替代记忆，减轻 AI 认知负担。
"""

import os
from datetime import datetime
from pathlib import Path


def get_project_root() -> Path:
    """获取项目根目录 (cursor-agent-team/)"""
    return Path(__file__).parent.parent


def check_file_exists(filepath: Path) -> tuple[bool, str]:
    """检查文件是否存在"""
    exists = filepath.exists()
    status = "✅" if exists else "❌"
    return exists, status


def count_files_in_directory(dirpath: Path, pattern: str = "*.md") -> int:
    """统计目录中符合模式的文件数量"""
    if not dirpath.exists():
        return 0
    return len(list(dirpath.glob(pattern)))


def run_preflight_check() -> str:
    """执行预飞检查，返回格式化的输出"""
    project_root = get_project_root()
    ai_workspace = project_root / "ai_workspace"
    
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 检查关键文件和目录
    topics_path = ai_workspace / "discussion_topics.md"
    topics_exists, topics_status = check_file_exists(topics_path)
    
    cards_dir = ai_workspace / "inspiration_capital" / "cards"
    cards_count = count_files_in_directory(cards_dir, "*.md")
    cards_status = "✅" if cards_dir.exists() else "❌"
    
    notes_dir = ai_workspace / "notes"
    notes_count = count_files_in_directory(notes_dir, "*.md")
    notes_status = "✅" if notes_dir.exists() else "❌"
    
    # 构建输出
    output_lines = [
        "=== Preflight Check ===",
        f"⏰ 当前时间: {current_time}",
        "",
        "📋 工作区状态:",
        f"  {topics_status} discussion_topics.md",
        f"  {cards_status} inspiration_capital/ ({cards_count} cards)",
        f"  {notes_status} notes/ ({notes_count} files)",
        "",
        "📌 操作约定:",
        "  • 删除 → _scripts/cleanup_ai_workspace.py",
        "  • 创卡 → ai_workspace/inspiration_capital/scripts/create_card.py",
        "  • 抽卡 → ai_workspace/inspiration_capital/scripts/draw_cards.py",
        "",
        "⚠️ 结束前必做 (DO NOT SKIP):",
        "  1. persona_output.py → 加载人格后再输出",
        "  2. Gleaning → 有价值洞见就创卡",
        "",
        "=== Ready ===",
    ]
    
    return "\n".join(output_lines)


def main():
    """主函数"""
    print(run_preflight_check())


if __name__ == "__main__":
    main()
