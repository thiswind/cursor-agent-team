#!/usr/bin/env python3
"""
Test if TRAE SOLO adaptation can correctly access ai_workspace directory
"""

import os
import sys

# Get absolute path of current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Build absolute path of ai_workspace directory
ai_workspace_path = os.path.join(current_dir, '..', 'ai_workspace')

print(f"Testing ai_workspace access from TRAE SOLO adaptation...")
print(f"Current directory: {current_dir}")
print(f"ai_workspace path: {ai_workspace_path}")

# Check if ai_workspace directory exists
if os.path.exists(ai_workspace_path):
    print("✅ ai_workspace directory exists")
    
    # Check if inspiration_capital subdirectory exists
    inspiration_capital_path = os.path.join(ai_workspace_path, 'inspiration_capital')
    if os.path.exists(inspiration_capital_path):
        print("✅ inspiration_capital directory exists")
        
        # Check if scripts subdirectory exists
        scripts_path = os.path.join(inspiration_capital_path, 'scripts')
        if os.path.exists(scripts_path):
            print("✅ scripts directory exists")
            
            # Check if create_card.py exists
            create_card_path = os.path.join(scripts_path, 'create_card.py')
            if os.path.exists(create_card_path):
                print("✅ create_card.py exists")
                
                # Check if draw_cards.py exists
                draw_cards_path = os.path.join(scripts_path, 'draw_cards.py')
                if os.path.exists(draw_cards_path):
                    print("✅ draw_cards.py exists")
                    print("\n🎉 All tests passed! TRAE SOLO adaptation can access ai_workspace directory.")
                    sys.exit(0)
                else:
                    print("❌ draw_cards.py not found")
            else:
                print("❌ create_card.py not found")
        else:
            print("❌ scripts directory not found")
    else:
        print("❌ inspiration_capital directory not found")
else:
    print("❌ ai_workspace directory not found")

print("\n❌ Some tests failed. TRAE SOLO adaptation cannot access ai_workspace directory.")
sys.exit(1)