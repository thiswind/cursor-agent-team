#!/bin/bash
# install.sh - Install Cursor AI Agent Team Framework
#
# This script installs the Cursor AI Agent Team Framework into your project
# by copying command and rule files to the project root's .cursor/ directory.
#
# Usage:
#   ./cursor-agent-team/install.sh
#
# Prerequisites:
#   - Git submodule must be added first:
#     git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
#     git submodule update --init --recursive

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Submodule directory (relative to project root)
SUBMODULE_DIR="cursor-agent-team"

echo "=========================================="
echo "Cursor AI Agent Team Framework Installer"
echo "=========================================="
echo ""

# Step 1: Environment Detection
echo "Step 1: Checking environment..."

# Check if we're in a git repository (project root)
if [ ! -d "$PROJECT_ROOT/.git" ]; then
    echo -e "${RED}Error: Not in a git repository.${NC}"
    echo "Please run this script from a git repository root directory."
    exit 1
fi

# Check if submodule exists
if [ ! -d "$PROJECT_ROOT/$SUBMODULE_DIR" ]; then
    echo -e "${RED}Error: Submodule not found.${NC}"
    echo "Please add the submodule first:"
    echo "  git submodule add https://github.com/thiswind/cursor-agent-team.git $SUBMODULE_DIR"
    echo "  git submodule update --init --recursive"
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

mkdir -p "$PROJECT_ROOT/.cursor/commands"
mkdir -p "$PROJECT_ROOT/.cursor/rules"

echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Step 3: Copy files (direct overwrite)
echo "Step 3: Copying files..."

# Copy command files
echo "  Copying command files..."
cp "$PROJECT_ROOT/$SUBMODULE_DIR/.cursor/commands/discuss.md" "$PROJECT_ROOT/.cursor/commands/" || {
    echo -e "${RED}Error: Failed to copy discuss.md${NC}"
    exit 1
}
cp "$PROJECT_ROOT/$SUBMODULE_DIR/.cursor/commands/prompt_engineer.md" "$PROJECT_ROOT/.cursor/commands/" || {
    echo -e "${RED}Error: Failed to copy prompt_engineer.md${NC}"
    exit 1
}
cp "$PROJECT_ROOT/$SUBMODULE_DIR/.cursor/commands/crew.md" "$PROJECT_ROOT/.cursor/commands/" || {
    echo -e "${RED}Error: Failed to copy crew.md${NC}"
    exit 1
}

# Copy rule files
echo "  Copying rule files..."
cp "$PROJECT_ROOT/$SUBMODULE_DIR/.cursor/rules/discussion_assistant.mdc" "$PROJECT_ROOT/.cursor/rules/" || {
    echo -e "${RED}Error: Failed to copy discussion_assistant.mdc${NC}"
    exit 1
}
cp "$PROJECT_ROOT/$SUBMODULE_DIR/.cursor/rules/prompt_engineer_assistant.mdc" "$PROJECT_ROOT/.cursor/rules/" || {
    echo -e "${RED}Error: Failed to copy prompt_engineer_assistant.mdc${NC}"
    exit 1
}
cp "$PROJECT_ROOT/$SUBMODULE_DIR/.cursor/rules/crew_assistant.mdc" "$PROJECT_ROOT/.cursor/rules/" || {
    echo -e "${RED}Error: Failed to copy crew_assistant.mdc${NC}"
    exit 1
}

echo -e "${GREEN}✓ Files copied${NC}"
echo ""

# Step 4: Create symbolic link for workspace
echo "Step 4: Creating workspace symbolic link..."

# Create 00_meta directory if not exists
mkdir -p "$PROJECT_ROOT/00_meta"

# Create symbolic link (if not exists or not a symlink)
if [ ! -L "$PROJECT_ROOT/00_meta/ai_workspace" ]; then
    if [ -d "$PROJECT_ROOT/00_meta/ai_workspace" ]; then
        echo -e "${YELLOW}Warning: 00_meta/ai_workspace/ already exists as a directory${NC}"
        echo "If you have existing data, please migrate it first before installing."
        echo "The framework will create a symbolic link, but existing directory must be migrated manually."
        exit 1
    fi
    ln -s "../cursor-agent-team/ai_workspace" "$PROJECT_ROOT/00_meta/ai_workspace"
    echo -e "${GREEN}✓ Symbolic link created${NC}"
else
    echo -e "${GREEN}✓ Symbolic link already exists${NC}"
fi
echo ""

# Step 5: Record installation information
echo "Step 5: Recording installation information..."

# Get version from git tag or CHANGELOG
VERSION="0.1.0"
if [ -f "$PROJECT_ROOT/$SUBMODULE_DIR/CHANGELOG.md" ]; then
    # Try to extract version from CHANGELOG
    CHANGELOG_VERSION=$(grep -m 1 "^## \[" "$PROJECT_ROOT/$SUBMODULE_DIR/CHANGELOG.md" | sed 's/## \[\(.*\)\].*/\1/' || echo "0.1.0")
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
INSTALL_INFO_FILE="$PROJECT_ROOT/.cursor/.cursor-agent-team-installed"
cat > "$INSTALL_INFO_FILE" << EOF
{
  "version": "$VERSION",
  "installed_at": "$INSTALLED_AT",
  "source": "$SUBMODULE_DIR",
  "files": [
    ".cursor/commands/discuss.md",
    ".cursor/commands/prompt_engineer.md",
    ".cursor/commands/crew.md",
    ".cursor/rules/discussion_assistant.mdc",
    ".cursor/rules/prompt_engineer_assistant.mdc",
    ".cursor/rules/crew_assistant.mdc"
  ]
}
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Installation information recorded${NC}"
else
    echo -e "${YELLOW}Warning: Failed to create installation info file${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Installation completed successfully!${NC}"
echo "=========================================="
echo ""
echo "Installed files:"
echo "  - .cursor/commands/discuss.md"
echo "  - .cursor/commands/prompt_engineer.md"
echo "  - .cursor/commands/crew.md"
echo "  - .cursor/rules/discussion_assistant.mdc"
echo "  - .cursor/rules/prompt_engineer_assistant.mdc"
echo "  - .cursor/rules/crew_assistant.mdc"
echo ""
echo "Version: $VERSION"
echo "Installed at: $INSTALLED_AT"
echo ""
echo "You can now use the following commands in Cursor:"
echo "  /discuss - Discussion partner"
echo "  /prompt_engineer - Prompt engineer"
echo "  /crew - Crew member"
echo ""

