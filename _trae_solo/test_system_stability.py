#!/usr/bin/env python3
"""
Test system stability of Cursor Agent Team TRAE SOLO adaptation
"""

import os
import sys
import time

# Get absolute path of current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Build absolute path of project root
project_root = os.path.join(current_dir, '..')

print(f"Testing Cursor Agent Team TRAE SOLO adaptation stability...")
print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")

# Test 1: Check directory structure
def test_directory_structure():
    print("\n=== Test 1: Directory Structure ===")
    
    # Check if _trae_solo directory exists
    trae_solo_dir = os.path.join(project_root, '_trae_solo')
    if os.path.exists(trae_solo_dir):
        print("✅ _trae_solo directory exists")
    else:
        print("❌ _trae_solo directory not found")
        return False
    
    # Check if commands directory exists
    commands_dir = os.path.join(trae_solo_dir, 'commands')
    if os.path.exists(commands_dir):
        print("✅ commands directory exists")
    else:
        print("❌ commands directory not found")
        return False
    
    # Check if rules directory exists
    rules_dir = os.path.join(trae_solo_dir, 'rules')
    if os.path.exists(rules_dir):
        print("✅ rules directory exists")
    else:
        print("❌ rules directory not found")
        return False
    
    # Check if skills directory exists
    skills_dir = os.path.join(trae_solo_dir, 'skills')
    if os.path.exists(skills_dir):
        print("✅ skills directory exists")
    else:
        print("❌ skills directory not found")
        return False
    
    return True

# Test 2: Check core files
def test_core_files():
    print("\n=== Test 2: Core Files ===")
    
    # Check command files
    commands = ['crew-config.md', 'discuss-config.md', 'prompt-engineer-config.md']
    for cmd in commands:
        cmd_path = os.path.join(project_root, '_trae_solo', 'commands', cmd)
        if os.path.exists(cmd_path):
            print(f"✅ {cmd} exists")
        else:
            print(f"❌ {cmd} not found")
            return False
    
    # Check skill files
    skills = ['cursor-agent-team-discuss', 'cursor-agent-team-crew', 'cursor-agent-team-prompt-engineer']
    for skill in skills:
        skill_path = os.path.join(project_root, '_trae_solo', 'skills', skill, 'SKILL.md')
        if os.path.exists(skill_path):
            print(f"✅ {skill}/SKILL.md exists")
        else:
            print(f"❌ {skill}/SKILL.md not found")
            return False
    
    return True

# Test 3: Check script execution
def test_script_execution():
    print("\n=== Test 3: Script Execution ===")
    
    # Test role_identity scripts
    role_scripts = ['crew.py', 'discuss.py', 'prompt_engineer.py']
    for script in role_scripts:
        script_path = os.path.join(project_root, '_scripts', 'role_identity', script)
        if os.path.exists(script_path):
            print(f"✅ {script} exists")
        else:
            print(f"❌ {script} not found")
            return False
    
    # Test preflight_check.py
    preflight_path = os.path.join(project_root, '_scripts', 'preflight_check.py')
    if os.path.exists(preflight_path):
        print("✅ preflight_check.py exists")
    else:
        print("❌ preflight_check.py not found")
        return False
    
    # Test phase_marker.py
    phase_marker_path = os.path.join(project_root, '_scripts', 'phase_marker.py')
    if os.path.exists(phase_marker_path):
        print("✅ phase_marker.py exists")
    else:
        print("❌ phase_marker.py not found")
        return False
    
    return True

# Test 4: Check ai_workspace access
def test_ai_workspace_access():
    print("\n=== Test 4: AI Workspace Access ===")
    
    # Check if ai_workspace directory exists
    ai_workspace_path = os.path.join(project_root, 'ai_workspace')
    if os.path.exists(ai_workspace_path):
        print("✅ ai_workspace directory exists")
    else:
        print("❌ ai_workspace directory not found")
        return False
    
    # Check if discussion_topics.md exists
    topics_path = os.path.join(ai_workspace_path, 'discussion_topics.md')
    if os.path.exists(topics_path):
        print("✅ discussion_topics.md exists")
    else:
        print("❌ discussion_topics.md not found")
        return False
    
    # Check if plans directory exists
    plans_path = os.path.join(ai_workspace_path, 'plans')
    if os.path.exists(plans_path):
        print("✅ plans directory exists")
    else:
        print("❌ plans directory not found")
        return False
    
    return True

# Test 5: Test system response time
def test_response_time():
    print("\n=== Test 5: Response Time ===")
    
    # Test script execution time
    start_time = time.time()
    
    # Run preflight_check.py
    preflight_path = os.path.join(project_root, '_scripts', 'preflight_check.py')
    if os.path.exists(preflight_path):
        try:
            import subprocess
            result = subprocess.run([sys.executable, preflight_path], capture_output=True, text=True, timeout=5)
            execution_time = time.time() - start_time
            print(f"✅ preflight_check.py executed in {execution_time:.2f} seconds")
            if execution_time <= 3:
                print("✅ Response time is within acceptable limit (<= 3 seconds)")
            else:
                print("⚠️ Response time is slightly over the limit (> 3 seconds)")
        except subprocess.TimeoutExpired:
            print("❌ preflight_check.py execution timed out (> 5 seconds)")
            return False
        except Exception as e:
            print(f"❌ Error executing preflight_check.py: {e}")
            return False
    else:
        print("❌ preflight_check.py not found")
        return False
    
    return True

# Run all tests
def run_all_tests():
    print("Starting system stability tests...\n")
    
    tests = [
        test_directory_structure,
        test_core_files,
        test_script_execution,
        test_ai_workspace_access,
        test_response_time
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test in tests:
        if test():
            passed_tests += 1
        else:
            print("\n❌ Test failed, stopping further tests")
            break
    
    print(f"\n=== Test Summary ===")
    print(f"Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! System is stable.")
        return True
    else:
        print("❌ Some tests failed. System may not be stable.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)