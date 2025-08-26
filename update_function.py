#!/usr/bin/env python3
"""
Update existing OpenWebUI function with corrected signature
"""

import requests
import json
import sys
from pathlib import Path

# Configuration
OPENWEBUI_URL = "http://localhost:3003"
API_KEY = "sk-73d4135f41e64e928a6921bd6dfadc3e"
FUNCTION_ID = "deepresearch_threat_modeling_fixed"
FUNCTION_FILE = "openwebui_function_prototype_fixed.py"

def load_function_code():
    """Load the function code from file"""
    try:
        current_dir = Path(__file__).parent
        function_path = current_dir / FUNCTION_FILE
        
        if not function_path.exists():
            print(f"❌ Function file not found: {function_path}")
            return None
            
        with open(function_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading function file: {e}")
        return None

def update_function(function_code):
    """Update existing function in OpenWebUI"""
    try:
        url = f"{OPENWEBUI_URL}/api/v1/functions/id/{FUNCTION_ID}/update"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "id": FUNCTION_ID,
            "name": "DeepResearch Enhanced Threat Modeling Function (Updated)",
            "content": function_code,
            "meta": {
                "description": "Enhanced threat modeling with AAF BNPL support and corrected function signature",
                "author": "DeepResearch System",
                "version": "1.2.0",
                "tags": ["threat-modeling", "security", "analysis", "AAF", "BNPL"],
                "updated": "Fixed function signature to match OpenWebUI expectations"
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            print("✅ Function updated successfully!")
            result = response.json()
            print(f"📋 Function ID: {result.get('id', 'Unknown')}")
            print(f"📋 Function Name: {result.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ Update failed: {response.status_code}")
            print(f"📋 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating function: {e}")
        return False

def main():
    print("🔄 DeepResearch Function Update - OpenWebUI")
    print("=" * 50)
    print(f"🎯 Target: {OPENWEBUI_URL}")
    print(f"📁 Function file: {FUNCTION_FILE}")
    print(f"🆔 Function ID: {FUNCTION_ID}")
    print(f"🔑 Using provided API key")
    print()
    
    # Load function code
    print("📖 Loading function code...")
    function_code = load_function_code()
    if not function_code:
        sys.exit(1)
    print(f"✅ Loaded {len(function_code)} characters")
    print()
    
    # Update function
    print("🔄 Updating existing function...")
    if update_function(function_code):
        print("\n🎉 Function update completed successfully!")
        print("\n📋 Next steps:")
        print("1. Refresh OpenWebUI web interface")
        print("2. Test with: 'Generate a threat model for AAF BNPL architecture'")
        print("3. Check Docker logs: wsl docker logs openwebui")
    else:
        print("\n❌ Update failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
