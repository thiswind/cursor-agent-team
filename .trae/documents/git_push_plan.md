# Git Push Plan for Cursor Agent Team

## Overview
This plan outlines the steps to clean the ai_workspace directory and make fine-grained commits before pushing the Cursor Agent Team framework to the remote repository.

## Objectives
1. **Clean the ai_workspace directory**: Remove all specific project content, leaving only directory structure and necessary template content
2. **Make fine-grained commits**: Commit changes in logical, focused commits
3. **Push to remote repository**: Ensure the clean version is pushed to GitHub

## Step 1: Clean the ai_workspace Directory

### Directories to Clean
- **ai_workspace/plans/**: Remove all plan files except template/example files
- **ai_workspace/inspiration_capital/cards/**: Remove all card files except example_card.md
- **ai_workspace/scratchpad/**: Remove all files except README.md
- **ai_workspace/topic_archives/**: Remove all archive files
- **ai_workspace/crew/**: Remove if not needed
- **ai_workspace/prompt_engineer/**: Remove if not needed
- **ai_workspace/spec_translator/**: Remove if not needed

### Files to Remove
- **ai_workspace/.DS_Store**
- **ai_workspace/.tts_capability.json**
- **ai_workspace/test_data_consistency.txt**
- Any other specific project files not needed for the framework

### Files to Keep
- **ai_workspace/README.md**
- **ai_workspace/agent_requirements/** with template files
- **ai_workspace/inspiration_capital/** with scripts and README.md
- **ai_workspace/scratchpad/README.md**
- **ai_workspace/templates/** with template files
- **ai_workspace/discussion_topics.md** (if it contains only template structure)

## Step 2: Make Fine-Grained Commits

### Commit 1: Remove old adaptations
- Remove _openclaw/ directory
- Remove _qwen/ directory
- Remove _trae/ directory
- Remove install_qwen.py and uninstall_qwen.py
- Remove TRAE_README.md

### Commit 2: Add TRAE SOLO adaptation
- Add _trae_solo/ directory with all its contents
- Add install_trae_solo.py
- Add TRAE_SOLO_README.md

### Commit 3: Update existing files
- Update README.md
- Update _scripts/_install_utils.py

### Commit 4: Clean ai_workspace directory
- Remove all specific project content from ai_workspace
- Keep only directory structure and template files

## Step 3: Push to Remote Repository

### Verify Cleanliness
- Ensure ai_workspace contains only directory structure and template content
- Ensure no specific project files are included

### Push Changes
- Push all commits to the remote repository
- Verify the push was successful

## Step 4: Verification

### Check Remote Repository
- Verify the repository on GitHub contains the clean version
- Ensure ai_workspace is properly structured with only template content

### Test Installation
- Test the TRAE SOLO installation process to ensure it works correctly

## Notes
- The ai_workspace directory should remain clean for future use as a shared workspace between Cursor and TRAE SOLO
- Only template files and directory structure should be committed, no specific project content
- Fine-grained commits make it easier to track changes and roll back if needed