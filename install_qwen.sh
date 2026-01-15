#!/bin/bash
# install_qwen.sh - Install Cursor AI Agent Team Framework for Qwen Code
#
# This script installs the Cursor AI Agent Team Framework into your project
# by copying command and context files to the project root's .qwen/ directory.
#
# Usage:
#   ./cursor-agent-team/install_qwen.sh
#
# Prerequisites:
#   - Git submodule must be added first:
#     git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Submodule directory (relative to project root)
SUBMODULE_DIR="cursor-agent-team"

echo "=========================================="
echo "Qwen Code AI Agent Team Framework Installer"
echo "=========================================="
echo ""

# Step 1: Environment Detection
echo "Step 1: Checking environment..."

# Check if we're in a git repository (project root)
if [ ! -d "$PROJECT_ROOT/.git" ]; then
    echo -e "${YELLOW}Warning: Not in a git repository.${NC}"
    echo "Continuing anyway (installation can work without git)..."
fi

# Check if submodule exists
if [ ! -d "$PROJECT_ROOT/$SUBMODULE_DIR" ]; then
    echo -e "${RED}Error: Submodule not found.${NC}"
    echo "Please add the submodule first:"
    echo "  git submodule add https://github.com/thiswind/cursor-agent-team.git $SUBMODULE_DIR"
    exit 1
fi

# Verify script is in submodule directory
if [ "$SCRIPT_DIR" != "$PROJECT_ROOT/$SUBMODULE_DIR" ]; then
    echo -e "${YELLOW}Warning: Script location mismatch.${NC}"
    echo "Expected: $PROJECT_ROOT/$SUBMODULE_DIR"
    echo "Actual: $SCRIPT_DIR"
    echo "Continuing anyway..."
fi

echo -e "${GREEN}✓ Environment check passed${NC}"
echo ""

# Step 2: Create directory structure
echo "Step 2: Creating directory structure..."

mkdir -p "$PROJECT_ROOT/.qwen/commands"
mkdir -p "$PROJECT_ROOT/.qwen/context"

echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Step 3: Copy files (direct overwrite)
echo "Step 3: Copying files..."

# Track installed items
INSTALLED_ITEMS=()

# Copy command files (TOML format)
echo "  Copying command files (TOML)..."
if cp "$PROJECT_ROOT/$SUBMODULE_DIR/_qwen/commands/discuss.toml" "$PROJECT_ROOT/.qwen/commands/"; then
    INSTALLED_ITEMS+=(".qwen/commands/discuss.toml")
else
    echo -e "${RED}Error: Failed to copy discuss.toml${NC}"
    exit 1
fi
if cp "$PROJECT_ROOT/$SUBMODULE_DIR/_qwen/commands/prompt_engineer.toml" "$PROJECT_ROOT/.qwen/commands/"; then
    INSTALLED_ITEMS+=(".qwen/commands/prompt_engineer.toml")
else
    echo -e "${RED}Error: Failed to copy prompt_engineer.toml${NC}"
    exit 1
fi
if cp "$PROJECT_ROOT/$SUBMODULE_DIR/_qwen/commands/crew.toml" "$PROJECT_ROOT/.qwen/commands/"; then
    INSTALLED_ITEMS+=(".qwen/commands/crew.toml")
else
    echo -e "${RED}Error: Failed to copy crew.toml${NC}"
    exit 1
fi
if cp "$PROJECT_ROOT/$SUBMODULE_DIR/_qwen/commands/spec_translator.toml" "$PROJECT_ROOT/.qwen/commands/"; then
    INSTALLED_ITEMS+=(".qwen/commands/spec_translator.toml")
else
    echo -e "${RED}Error: Failed to copy spec_translator.toml${NC}"
    exit 1
fi

# Copy context files (Markdown format)
echo "  Copying context files (Markdown)..."
if cp "$PROJECT_ROOT/$SUBMODULE_DIR/_qwen/context/discussion_assistant.md" "$PROJECT_ROOT/.qwen/context/"; then
    INSTALLED_ITEMS+=(".qwen/context/discussion_assistant.md")
else
    echo -e "${RED}Error: Failed to copy discussion_assistant.md${NC}"
    exit 1
fi
if cp "$PROJECT_ROOT/$SUBMODULE_DIR/_qwen/context/prompt_engineer_assistant.md" "$PROJECT_ROOT/.qwen/context/"; then
    INSTALLED_ITEMS+=(".qwen/context/prompt_engineer_assistant.md")
else
    echo -e "${RED}Error: Failed to copy prompt_engineer_assistant.md${NC}"
    exit 1
fi
if cp "$PROJECT_ROOT/$SUBMODULE_DIR/_qwen/context/crew_assistant.md" "$PROJECT_ROOT/.qwen/context/"; then
    INSTALLED_ITEMS+=(".qwen/context/crew_assistant.md")
else
    echo -e "${RED}Error: Failed to copy crew_assistant.md${NC}"
    exit 1
fi
if cp "$PROJECT_ROOT/$SUBMODULE_DIR/_qwen/context/spec_translator_assistant.md" "$PROJECT_ROOT/.qwen/context/"; then
    INSTALLED_ITEMS+=(".qwen/context/spec_translator_assistant.md")
else
    echo -e "${RED}Error: Failed to copy spec_translator_assistant.md${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Files copied${NC}"
echo ""

# Step 4: Create main QWEN.md file (optional - using import mechanism)
echo "Step 4: Creating main QWEN.md file (optional)..."

QWEN_MAIN_FILE="$PROJECT_ROOT/QWEN.md"
if [ ! -f "$QWEN_MAIN_FILE" ]; then
    cat > "$QWEN_MAIN_FILE" << 'EOF'
# Qwen Code Context

This file imports all context files from the cursor-agent-team framework.

@.qwen/context/discussion_assistant.md
@.qwen/context/crew_assistant.md
@.qwen/context/prompt_engineer_assistant.md
@.qwen/context/spec_translator_assistant.md
EOF
    INSTALLED_ITEMS+=("QWEN.md")
    echo -e "${GREEN}✓ Created QWEN.md with import statements${NC}"
else
    echo -e "${YELLOW}  QWEN.md already exists, skipping...${NC}"
    echo -e "${YELLOW}  You can manually add import statements if needed:${NC}"
    echo "    @.qwen/context/discussion_assistant.md"
    echo "    @.qwen/context/crew_assistant.md"
    echo "    @.qwen/context/prompt_engineer_assistant.md"
    echo "    @.qwen/context/spec_translator_assistant.md"
fi

echo ""

# Step 5: Record installation information
echo "Step 5: Recording installation information..."

# Get version from git tag or CHANGELOG
VERSION="0.1.0"
if [ -f "$PROJECT_ROOT/$SUBMODULE_DIR/CHANGELOG.md" ]; then
    # Try to extract version from CHANGELOG
    CHANGELOG_VERSION=$(grep -m 1 "^## \[" "$PROJECT_ROOT/$SUBMODULE_DIR/CHANGELOG.md" 2>/dev/null | sed -n 's/## \[\(.*\)\].*/\1/p')
    if [ -n "$CHANGELOG_VERSION" ]; then
        VERSION="$CHANGELOG_VERSION"
    fi
fi

# Try to get version from git tag
cd "$PROJECT_ROOT/$SUBMODULE_DIR"
if git describe --tags --exact-match HEAD >/dev/null 2>&1; then
    VERSION=$(git describe --tags --exact-match HEAD)
elif git describe --tags HEAD >/dev/null 2>&1; then
    VERSION=$(git describe --tags HEAD)
fi
cd "$PROJECT_ROOT"

INSTALLED_AT=$(date '+%Y-%m-%d %H:%M:%S')

# Create installation info file
INSTALL_INFO_FILE="$PROJECT_ROOT/.qwen/.qwen-agent-team-installed"
cat > "$INSTALL_INFO_FILE" << EOF
{
  "version": "$VERSION",
  "installed_at": "$INSTALLED_AT",
  "source": "$SUBMODULE_DIR",
  "platform": "qwen-code",
  "files": [
    ".qwen/commands/discuss.toml",
    ".qwen/commands/prompt_engineer.toml",
    ".qwen/commands/crew.toml",
    ".qwen/commands/spec_translator.toml",
    ".qwen/context/discussion_assistant.md",
    ".qwen/context/prompt_engineer_assistant.md",
    ".qwen/context/crew_assistant.md",
    ".qwen/context/spec_translator_assistant.md"
  ]
}
EOF

if [ $? -eq 0 ]; then
    INSTALLED_ITEMS+=(".qwen/.qwen-agent-team-installed")
    echo -e "${GREEN}✓ Installation information recorded${NC}"
else
    echo -e "${YELLOW}Warning: Failed to create installation info file${NC}"
fi

echo ""

# Step 6: Update .gitignore
echo "Step 6: Updating .gitignore..."

GITIGNORE_FILE="$PROJECT_ROOT/.gitignore"
IGNORE_PATTERN="$SUBMODULE_DIR"

# Check if .gitignore exists, create if not
if [ ! -f "$GITIGNORE_FILE" ]; then
    touch "$GITIGNORE_FILE"
    echo -e "${GREEN}✓ Created .gitignore file${NC}"
fi

# Check if the pattern already exists
if grep -q "^$IGNORE_PATTERN$" "$GITIGNORE_FILE" 2>/dev/null || grep -q "^/$IGNORE_PATTERN$" "$GITIGNORE_FILE" 2>/dev/null; then
    echo -e "${YELLOW}  Pattern already exists in .gitignore${NC}"
else
    # Add the pattern to .gitignore
    # Add a comment and the pattern
    if [ -s "$GITIGNORE_FILE" ]; then
        # File is not empty, add a newline if last line doesn't end with newline
        if [ "$(tail -c 1 "$GITIGNORE_FILE")" != "" ]; then
            echo "" >> "$GITIGNORE_FILE"
        fi
    fi
    echo "# Cursor AI Agent Team Framework (submodule)" >> "$GITIGNORE_FILE"
    echo "$IGNORE_PATTERN" >> "$GITIGNORE_FILE"
    echo -e "${GREEN}✓ Added $IGNORE_PATTERN to .gitignore${NC}"
fi

echo ""

echo "=========================================="
echo -e "${GREEN}Installation completed successfully!${NC}"
echo "=========================================="
echo ""
echo "Installed items:"
for item in "${INSTALLED_ITEMS[@]}"; do
    echo -e "  ${GREEN}✅${NC} $item"
done
echo ""
echo "Version: $VERSION"
echo "Installed at: $INSTALLED_AT"
echo ""
echo "You can now use the following commands in Qwen Code:"
echo "  /discuss - Discussion partner"
echo "  /prompt_engineer - Prompt engineer"
echo "  /crew - Crew member"
echo "  /spec_translator - Spec-Kit translator (additional feature)"
echo ""
echo "Note: The workspace at cursor-agent-team/ai_workspace/ is SHARED"
echo "      between Cursor and Qwen Code platforms."
echo ""
