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

# Confirm uninstallation
echo -e "${YELLOW}This will remove all installed files and directories.${NC}"
if [ -d "$PROJECT_ROOT/cursor-agent-team" ] && [ -f "$PROJECT_ROOT/.gitmodules" ]; then
    echo -e "${YELLOW}This will also remove the git submodule.${NC}"
fi
read -p "Are you sure you want to uninstall? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "Uninstalling..."

# Track removed items
REMOVED_ITEMS=()
# Track if submodule should be removed (default: yes if submodule exists)
REMOVE_SUBMODULE=0
if [ -d "$PROJECT_ROOT/cursor-agent-team" ] && [ -f "$PROJECT_ROOT/.gitmodules" ]; then
    REMOVE_SUBMODULE=1
fi

# Step 2: Delete files
# Delete command files
if [ -f "$PROJECT_ROOT/.cursor/commands/discuss.md" ]; then
    rm -f "$PROJECT_ROOT/.cursor/commands/discuss.md"
    REMOVED_ITEMS+=(".cursor/commands/discuss.md")
fi
if [ -f "$PROJECT_ROOT/.cursor/commands/prompt_engineer.md" ]; then
    rm -f "$PROJECT_ROOT/.cursor/commands/prompt_engineer.md"
    REMOVED_ITEMS+=(".cursor/commands/prompt_engineer.md")
fi
if [ -f "$PROJECT_ROOT/.cursor/commands/crew.md" ]; then
    rm -f "$PROJECT_ROOT/.cursor/commands/crew.md"
    REMOVED_ITEMS+=(".cursor/commands/crew.md")
fi

# Delete rule files
if [ -f "$PROJECT_ROOT/.cursor/rules/discussion_assistant.mdc" ]; then
    rm -f "$PROJECT_ROOT/.cursor/rules/discussion_assistant.mdc"
    REMOVED_ITEMS+=(".cursor/rules/discussion_assistant.mdc")
fi
if [ -f "$PROJECT_ROOT/.cursor/rules/prompt_engineer_assistant.mdc" ]; then
    rm -f "$PROJECT_ROOT/.cursor/rules/prompt_engineer_assistant.mdc"
    REMOVED_ITEMS+=(".cursor/rules/prompt_engineer_assistant.mdc")
fi
if [ -f "$PROJECT_ROOT/.cursor/rules/crew_assistant.mdc" ]; then
    rm -f "$PROJECT_ROOT/.cursor/rules/crew_assistant.mdc"
    REMOVED_ITEMS+=(".cursor/rules/crew_assistant.mdc")
fi

# Step 3: Remove installation info
if [ -f "$INSTALL_INFO_FILE" ]; then
    rm -f "$INSTALL_INFO_FILE"
    REMOVED_ITEMS+=(".cursor/.cursor-agent-team-installed")
fi

# Step 4: Clean up empty directories
# Remove commands directory if empty
if [ -d "$PROJECT_ROOT/.cursor/commands" ]; then
    if [ -z "$(ls -A "$PROJECT_ROOT/.cursor/commands" 2>/dev/null)" ]; then
        if rmdir "$PROJECT_ROOT/.cursor/commands" 2>/dev/null; then
            REMOVED_ITEMS+=(".cursor/commands/")
        fi
    fi
fi

# Remove rules directory if empty
if [ -d "$PROJECT_ROOT/.cursor/rules" ]; then
    if [ -z "$(ls -A "$PROJECT_ROOT/.cursor/rules" 2>/dev/null)" ]; then
        if rmdir "$PROJECT_ROOT/.cursor/rules" 2>/dev/null; then
            REMOVED_ITEMS+=(".cursor/rules/")
        fi
    fi
fi

# Remove .cursor directory if empty
if [ -d "$PROJECT_ROOT/.cursor" ]; then
    REMAINING_ITEMS=$(find "$PROJECT_ROOT/.cursor" -mindepth 1 -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')
    if [ "$REMAINING_ITEMS" -eq 0 ]; then
        if rmdir "$PROJECT_ROOT/.cursor" 2>/dev/null; then
            REMOVED_ITEMS+=(".cursor/")
        fi
    fi
fi

# Step 5: Remove submodule if it exists
if [ "$REMOVE_SUBMODULE" -eq 1 ]; then
    cd "$PROJECT_ROOT"
    
    # Deinitialize submodule
    if git submodule deinit -f cursor-agent-team 2>/dev/null; then
        REMOVED_ITEMS+=("Submodule deinitialized")
    fi
    
    # Remove submodule from Git index
    if git rm -f cursor-agent-team 2>/dev/null; then
        REMOVED_ITEMS+=("Submodule removed from Git index")
    fi
    
    # Remove Git internal module configuration
    if [ -d "$PROJECT_ROOT/.git/modules/cursor-agent-team" ]; then
        rm -rf "$PROJECT_ROOT/.git/modules/cursor-agent-team"
        REMOVED_ITEMS+=("Git internal module configuration")
    fi
    
    # Remove submodule directory
    if [ -d "$PROJECT_ROOT/cursor-agent-team" ]; then
        rm -rf "$PROJECT_ROOT/cursor-agent-team"
        REMOVED_ITEMS+=("Submodule directory (cursor-agent-team/)")
    fi
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Uninstallation completed!${NC}"
echo "=========================================="
echo ""
echo "Removed items:"
for item in "${REMOVED_ITEMS[@]}"; do
    echo -e "  ${GREEN}✅${NC} $item"
done
echo ""

# Check if submodule was removed
if [ "$REMOVE_SUBMODULE" -eq 1 ]; then
    # Check if any submodule-related items were removed
    if printf '%s\n' "${REMOVED_ITEMS[@]}" | grep -q "Submodule"; then
        echo -e "${YELLOW}Note: Don't forget to commit the changes:${NC}"
        echo "  git commit -m 'Remove cursor-agent-team submodule'"
        echo ""
    fi
fi

echo "The Cursor AI Agent Team Framework has been removed from your project."
echo ""

