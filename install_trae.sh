#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

TRAE_DIR="$PROJECT_ROOT/.trae"
TRAE_RULES_DIR="$TRAE_DIR/rules"
TRAE_SKILLS_DIR="$TRAE_DIR/skills"

SOURCE_RULES="$SCRIPT_DIR/_trae/rules"
SOURCE_SKILLS="$SCRIPT_DIR/_trae/skills"

echo "=== cursor-agent-team TRAE Installation ==="
echo ""
echo "Project root: $PROJECT_ROOT"
echo "Source: $SCRIPT_DIR/_trae/"
echo "Target: $TRAE_DIR/"
echo ""

if [ ! -d "$SOURCE_RULES" ] || [ ! -d "$SOURCE_SKILLS" ]; then
    echo "ERROR: Source _trae/ directory not found at $SCRIPT_DIR/_trae/"
    echo "Make sure you are on the trae-cn branch."
    exit 1
fi

echo "[1/3] Creating .trae directories..."
mkdir -p "$TRAE_RULES_DIR"
mkdir -p "$TRAE_SKILLS_DIR"

echo "[2/3] Copying project rules..."
cp "$SOURCE_RULES/project_rules.md" "$TRAE_RULES_DIR/project_rules.md"
echo "  -> $TRAE_RULES_DIR/project_rules.md"

echo "[3/3] Copying skills..."
for skill_dir in "$SOURCE_SKILLS"/skill-*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p "$TRAE_SKILLS_DIR/$skill_name"
    cp "$skill_dir/SKILL.md" "$TRAE_SKILLS_DIR/$skill_name/SKILL.md"
    echo "  -> $TRAE_SKILLS_DIR/$skill_name/SKILL.md"
done

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Files installed:"
echo "  Rules:  $TRAE_RULES_DIR/project_rules.md"
find "$TRAE_SKILLS_DIR" -name "SKILL.md" -exec echo "  Skill:  {}" \;
echo ""
echo "=== Manual Steps Required ==="
echo ""
echo "You need to manually create 3 Agents in TRAE GUI (Settings -> Agent):"
echo ""
echo "  1. Discussion Partner (讨论搭档)"
echo "     Prompt: $SCRIPT_DIR/_trae/agent_prompts/discussion_partner.md"
echo "     Tools:  File System, Terminal, Web Search"
echo ""
echo "  2. Crew Member (执行组员)"
echo "     Prompt: $SCRIPT_DIR/_trae/agent_prompts/crew_member.md"
echo "     Tools:  File System, Terminal, Web Search"
echo ""
echo "  3. TRAE Prompt Engineer (TRAE 提示工程师)"
echo "     Prompt: $SCRIPT_DIR/_trae/agent_prompts/trae_prompt_engineer.md"
echo "     Tools:  File System, Terminal, Web Search"
echo ""
echo "Copy each prompt file's full content into the corresponding Agent's prompt field."
echo ""
echo "Done! Use @Discussion Partner, @Crew Member, or @TRAE Prompt Engineer to start."
