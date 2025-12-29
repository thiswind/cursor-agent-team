#!/bin/bash
# uninstall.sh - Uninstall Cursor AI Agent Team Framework
#
# This script removes the Cursor AI Agent Team Framework from your project
# by deleting the files that were installed by install.sh.
#
# Usage:
#   ./cursor-agent-team/uninstall.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Installation info file
INSTALL_INFO_FILE="$PROJECT_ROOT/.cursor/.cursor-agent-team-installed"

echo "=========================================="
echo "Cursor AI Agent Team Framework Uninstaller"
echo "=========================================="
echo ""

# Step 1: Check installation info
echo "Step 1: Checking installation information..."

if [ ! -f "$INSTALL_INFO_FILE" ]; then
    echo -e "${YELLOW}Framework not installed or installation info missing.${NC}"
    echo "Nothing to uninstall."
    exit 0
fi

# Read installation info
INSTALLED_VERSION=$(grep -o '"version": "[^"]*"' "$INSTALL_INFO_FILE" | cut -d'"' -f4 || echo "unknown")
INSTALLED_AT=$(grep -o '"installed_at": "[^"]*"' "$INSTALL_INFO_FILE" | cut -d'"' -f4 || echo "unknown")

echo "Found installation:"
echo "  Version: $INSTALLED_VERSION"
echo "  Installed at: $INSTALLED_AT"
echo ""

# Step 2: Delete files
echo "Step 2: Removing installed files..."

# Delete command files
echo "  Removing command files..."
rm -f "$PROJECT_ROOT/.cursor/commands/discuss.md"
rm -f "$PROJECT_ROOT/.cursor/commands/prompt_engineer.md"
rm -f "$PROJECT_ROOT/.cursor/commands/crew.md"

# Delete rule files
echo "  Removing rule files..."
rm -f "$PROJECT_ROOT/.cursor/rules/discussion_assistant.mdc"
rm -f "$PROJECT_ROOT/.cursor/rules/prompt_engineer_assistant.mdc"
rm -f "$PROJECT_ROOT/.cursor/rules/crew_assistant.mdc"

echo -e "${GREEN}✓ Files removed${NC}"
echo ""

# Step 3: Clean up directories
echo "Step 3: Cleaning up directories..."

# Check if commands directory is empty
if [ -d "$PROJECT_ROOT/.cursor/commands" ]; then
    if [ -z "$(ls -A "$PROJECT_ROOT/.cursor/commands" 2>/dev/null)" ]; then
        read -p "Remove empty .cursor/commands/ directory? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rmdir "$PROJECT_ROOT/.cursor/commands"
            echo -e "${GREEN}✓ Removed .cursor/commands/ directory${NC}"
        fi
    fi
fi

# Check if rules directory is empty
if [ -d "$PROJECT_ROOT/.cursor/rules" ]; then
    if [ -z "$(ls -A "$PROJECT_ROOT/.cursor/rules" 2>/dev/null)" ]; then
        read -p "Remove empty .cursor/rules/ directory? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rmdir "$PROJECT_ROOT/.cursor/rules"
            echo -e "${GREEN}✓ Removed .cursor/rules/ directory${NC}"
        fi
    fi
fi

# Check if .cursor directory is empty (excluding .cursor-agent-team-installed)
if [ -d "$PROJECT_ROOT/.cursor" ]; then
    # Count files/dirs excluding the install info file
    REMAINING_ITEMS=$(find "$PROJECT_ROOT/.cursor" -mindepth 1 -maxdepth 1 ! -name ".cursor-agent-team-installed" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$REMAINING_ITEMS" -eq 0 ]; then
        read -p "Remove empty .cursor/ directory? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rmdir "$PROJECT_ROOT/.cursor"
            echo -e "${GREEN}✓ Removed .cursor/ directory${NC}"
        fi
    fi
fi

echo ""

# Step 4: Remove installation info
echo "Step 4: Removing installation information..."

rm -f "$INSTALL_INFO_FILE"
echo -e "${GREEN}✓ Installation information removed${NC}"
echo ""

# Step 5: Optional submodule removal
echo "Step 5: Submodule removal (optional)..."

read -p "Remove submodule? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing submodule..."
    cd "$PROJECT_ROOT"
    
    # Deinitialize submodule
    if git submodule deinit -f cursor-agent-team 2>/dev/null; then
        echo -e "${GREEN}✓ Submodule deinitialized${NC}"
    else
        echo -e "${YELLOW}Warning: Failed to deinitialize submodule${NC}"
    fi
    
    # Remove submodule
    if git rm -f cursor-agent-team 2>/dev/null; then
        echo -e "${GREEN}✓ Submodule removed${NC}"
        echo ""
        echo -e "${YELLOW}Note: Don't forget to commit the changes:${NC}"
        echo "  git commit -m 'Remove cursor-agent-team submodule'"
    else
        echo -e "${YELLOW}Warning: Failed to remove submodule${NC}"
        echo "You may need to manually remove it from .gitmodules and .git/config"
    fi
else
    echo "Submodule kept. You can remove it later with:"
    echo "  git submodule deinit cursor-agent-team"
    echo "  git rm cursor-agent-team"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Uninstallation completed!${NC}"
echo "=========================================="
echo ""
echo "The Cursor AI Agent Team Framework has been removed from your project."
echo ""

