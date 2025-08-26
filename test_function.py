#!/usr/bin/env python3
"""
Test the updated DeepResearch function with proper signature
"""

import requests
import json

# Configuration
OPENWEBUI_URL = "http://localhost:3003"
API_KEY = "sk-73d4135f41e64e928a6921bd6dfadc3e"
FUNCTION_ID = "deepresearch_threat_modeling_fixed"

def test_function():
    """Test the function with a simple query"""
    try:
        url = f"{OPENWEBUI_URL}/api/v1/functions/id/{FUNCTION_ID}/call"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Test data matching the expected signature
        data = {
            "user_message": "Generate a threat model for AAF BNPL architecture",
            "model_id": "gemma3:12b",
            "messages": [
                {
                    "role": "user",
                    "content": "Generate a threat model for AAF BNPL architecture"
                }
            ],
            "body": {
                "model": "gemma3:12b",
                "stream": False,
                "max_tokens": 4000
            }
        }
        
        print("🧪 Testing DeepResearch function...")
        print(f"📡 URL: {url}")
        print(f"📋 Query: {data['user_message']}")
        print()
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Function test successful!")
            print(f"📋 Response type: {type(result)}")
            if isinstance(result, dict) and 'response' in result:
                print(f"📋 Response preview: {result['response'][:200]}...")
            elif isinstance(result, str):
                print(f"📋 Response preview: {result[:200]}...")
            else:
                print(f"📋 Full response: {result}")
            return True
        else:
            print(f"❌ Test failed: {response.status_code}")
            print(f"📋 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing function: {e}")
        return False

def main():
    print("🧪 DeepResearch Function Test")
    print("=" * 40)
    print(f"🎯 Target: {OPENWEBUI_URL}")
    print(f"🆔 Function ID: {FUNCTION_ID}")
    print(f"🔑 Using provided API key")
    print()
    
    if test_function():
        print("\n🎉 Test completed successfully!")
        print("\n📋 Function is ready for use:")
        print("1. Web interface: http://localhost:3003")
        print("2. Function: DeepResearch Enhanced Threat Modeling Function (Updated)")
        print("3. Test query: 'Generate a threat model for AAF BNPL architecture'")
    else:
        print("\n❌ Test failed. Check logs for details.")

if __name__ == "__main__":
    main()
