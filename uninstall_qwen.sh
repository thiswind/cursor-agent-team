#!/bin/bash
# uninstall_qwen.sh - Uninstall Cursor AI Agent Team Framework for Qwen Code
#
# This script removes the Cursor AI Agent Team Framework from your project
# by deleting the files that were installed by install_qwen.sh.
#
# Usage:
#   ./cursor-agent-team/uninstall_qwen.sh

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
INSTALL_INFO_FILE="$PROJECT_ROOT/.qwen/.qwen-agent-team-installed"

echo "=========================================="
echo "Qwen Code AI Agent Team Framework Uninstaller"
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
# Delete command files (TOML)
if [ -f "$PROJECT_ROOT/.qwen/commands/discuss.toml" ]; then
    rm -f "$PROJECT_ROOT/.qwen/commands/discuss.toml"
    REMOVED_ITEMS+=(".qwen/commands/discuss.toml")
fi
if [ -f "$PROJECT_ROOT/.qwen/commands/prompt_engineer.toml" ]; then
    rm -f "$PROJECT_ROOT/.qwen/commands/prompt_engineer.toml"
    REMOVED_ITEMS+=(".qwen/commands/prompt_engineer.toml")
fi
if [ -f "$PROJECT_ROOT/.qwen/commands/crew.toml" ]; then
    rm -f "$PROJECT_ROOT/.qwen/commands/crew.toml"
    REMOVED_ITEMS+=(".qwen/commands/crew.toml")
fi
if [ -f "$PROJECT_ROOT/.qwen/commands/spec_translator.toml" ]; then
    rm -f "$PROJECT_ROOT/.qwen/commands/spec_translator.toml"
    REMOVED_ITEMS+=(".qwen/commands/spec_translator.toml")
fi

# Delete context files (Markdown)
if [ -f "$PROJECT_ROOT/.qwen/context/discussion_assistant.md" ]; then
    rm -f "$PROJECT_ROOT/.qwen/context/discussion_assistant.md"
    REMOVED_ITEMS+=(".qwen/context/discussion_assistant.md")
fi
if [ -f "$PROJECT_ROOT/.qwen/context/prompt_engineer_assistant.md" ]; then
    rm -f "$PROJECT_ROOT/.qwen/context/prompt_engineer_assistant.md"
    REMOVED_ITEMS+=(".qwen/context/prompt_engineer_assistant.md")
fi
if [ -f "$PROJECT_ROOT/.qwen/context/crew_assistant.md" ]; then
    rm -f "$PROJECT_ROOT/.qwen/context/crew_assistant.md"
    REMOVED_ITEMS+=(".qwen/context/crew_assistant.md")
fi
if [ -f "$PROJECT_ROOT/.qwen/context/spec_translator_assistant.md" ]; then
    rm -f "$PROJECT_ROOT/.qwen/context/spec_translator_assistant.md"
    REMOVED_ITEMS+=(".qwen/context/spec_translator_assistant.md")
fi

# Step 3: Remove installation info
if [ -f "$INSTALL_INFO_FILE" ]; then
    rm -f "$INSTALL_INFO_FILE"
    REMOVED_ITEMS+=(".qwen/.qwen-agent-team-installed")
fi

# Step 4: Clean up empty directories
# Remove commands directory if empty
if [ -d "$PROJECT_ROOT/.qwen/commands" ]; then
    if [ -z "$(ls -A "$PROJECT_ROOT/.qwen/commands" 2>/dev/null)" ]; then
        if rmdir "$PROJECT_ROOT/.qwen/commands" 2>/dev/null; then
            REMOVED_ITEMS+=(".qwen/commands/")
        fi
    fi
fi

# Remove context directory if empty
if [ -d "$PROJECT_ROOT/.qwen/context" ]; then
    if [ -z "$(ls -A "$PROJECT_ROOT/.qwen/context" 2>/dev/null)" ]; then
        if rmdir "$PROJECT_ROOT/.qwen/context" 2>/dev/null; then
            REMOVED_ITEMS+=(".qwen/context/")
        fi
    fi
fi

# Remove .qwen directory if empty
if [ -d "$PROJECT_ROOT/.qwen" ]; then
    REMAINING_ITEMS=$(find "$PROJECT_ROOT/.qwen" -mindepth 1 -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')
    if [ "$REMAINING_ITEMS" -eq 0 ]; then
        if rmdir "$PROJECT_ROOT/.qwen" 2>/dev/null; then
            REMOVED_ITEMS+=(".qwen/")
        fi
    fi
fi

# Step 5: Note about QWEN.md
# We don't automatically remove QWEN.md as it might contain user's custom content
if [ -f "$PROJECT_ROOT/QWEN.md" ]; then
    echo -e "${YELLOW}Note: QWEN.md file exists but was not removed.${NC}"
    echo "  You may want to manually remove or update it if it only contained"
    echo "  the framework imports."
fi

# Step 6: Remove submodule if it exists
if [ "$REMOVE_SUBMODULE" -eq 1 ]; then
    cd "$PROJECT_ROOT"
    
    # Check if submodule directory exists before removal
    SUBMODULE_DIR_EXISTS=0
    if [ -d "$PROJECT_ROOT/cursor-agent-team" ]; then
        SUBMODULE_DIR_EXISTS=1
    fi
    
    # Deinitialize submodule
    if git submodule deinit -f cursor-agent-team 2>/dev/null; then
        REMOVED_ITEMS+=("Submodule deinitialized")
    fi
    
    # Remove submodule from Git index (this also removes the directory)
    if git rm -f cursor-agent-team 2>/dev/null; then
        REMOVED_ITEMS+=("Submodule removed from Git index")
        if [ "$SUBMODULE_DIR_EXISTS" -eq 1 ]; then
            REMOVED_ITEMS+=("Submodule directory (cursor-agent-team/)")
        fi
    fi
    
    # Remove Git internal module configuration
    if [ -d "$PROJECT_ROOT/.git/modules/cursor-agent-team" ]; then
        rm -rf "$PROJECT_ROOT/.git/modules/cursor-agent-team"
        REMOVED_ITEMS+=("Git internal module configuration")
    fi
    
    # Fallback: Remove submodule directory if still exists (shouldn't happen after git rm)
    if [ -d "$PROJECT_ROOT/cursor-agent-team" ]; then
        rm -rf "$PROJECT_ROOT/cursor-agent-team"
        if [ "$SUBMODULE_DIR_EXISTS" -eq 1 ] && ! printf '%s\n' "${REMOVED_ITEMS[@]}" | grep -q "Submodule directory"; then
            REMOVED_ITEMS+=("Submodule directory (cursor-agent-team/)")
        fi
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

echo "The Qwen Code AI Agent Team Framework has been removed from your project."
echo ""
