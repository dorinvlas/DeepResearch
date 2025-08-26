#!/usr/bin/env python3
"""
Deploy DeepResearch Enhanced Threat Modeling Function to OpenWebUI

This script uploads the function to a local OpenWebUI instance running on localhost:3003
using the /api/v1/functions endpoint.

Usage:
    python deploy_to_openwebui.py

Requirements:
    - OpenWebUI running on localhost:3003
    - Valid authentication token (will be prompted)
"""

import requests
import json
import sys
from pathlib import Path

def read_function_code():
    """Read the function code from the prototype file"""
    function_file = Path("openwebui_function_prototype.py")
    
    if not function_file.exists():
        print(f"❌ Error: {function_file} not found")
        return None
    
    with open(function_file, 'r', encoding='utf-8') as f:
        return f.read()

def create_function_metadata(code: str):
    """Create function metadata for OpenWebUI"""
    return {
        "id": "deepresearch_threat_modeling",
        "name": "DeepResearch Enhanced Threat Modeling",
        "type": "function",
        "content": code,
        "meta": {
            "description": "Advanced AI research with automated threat modeling and self-learning discovery",
            "author": "DeepResearch Team",
            "version": "1.0.0",
            "license": "MIT",
            "requirements": [
                "aiohttp",
                "pyyaml",
                "pickle"
            ],
            "tags": [
                "threat-modeling",
                "research",
                "security",
                "threagile",
                "ai"
            ]
        }
    }

def deploy_function(openwebui_url: str, auth_token: str = None):
    """Deploy function to OpenWebUI"""
    
    print("🚀 Deploying DeepResearch Enhanced Threat Modeling Function...")
    
    # Read function code
    code = read_function_code()
    if not code:
        return False
    
    # Create function metadata
    function_data = create_function_metadata(code)
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json"
    }
    
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    
    # Deploy to OpenWebUI
    try:
        print(f"📡 Connecting to {openwebui_url}/api/v1/functions")
        
        response = requests.post(
            f"{openwebui_url}/api/v1/functions",
            headers=headers,
            json=function_data,
            timeout=30
        )
        
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Function deployed successfully!")
            print(f"📊 Response: {response.json()}")
            return True
        else:
            print(f"❌ Deployment failed: {response.status_code}")
            print(f"📋 Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

def test_function_availability(openwebui_url: str, auth_token: str = None):
    """Test if the function is available after deployment"""
    
    print("\n🔍 Testing function availability...")
    
    headers = {}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    
    try:
        response = requests.get(
            f"{openwebui_url}/api/v1/functions",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            functions = response.json()
            
            # Look for our function
            for func in functions:
                if func.get("id") == "deepresearch_threat_modeling":
                    print("✅ Function found in OpenWebUI!")
                    print(f"📝 Name: {func.get('name')}")
                    print(f"🆔 ID: {func.get('id')}")
                    return True
            
            print("⚠️  Function deployed but not found in function list")
            return False
        else:
            print(f"❌ Cannot retrieve functions: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Test connection error: {e}")
        return False

def main():
    """Main deployment function"""
    
    print("🔒 DeepResearch Enhanced Threat Modeling - OpenWebUI Deployment")
    print("=" * 60)
    
    # Configuration
    openwebui_url = "http://localhost:3003"
    
    print(f"🎯 Target: {openwebui_url}")
    print(f"📁 Function file: openwebui_function_prototype.py")
    
    # Get auth token (optional for local testing)
    auth_token = input("\n🔑 Enter OpenWebUI auth token (or press Enter to skip): ").strip()
    if not auth_token:
        auth_token = None
        print("⚠️  Proceeding without authentication (local testing mode)")
    
    # Deploy function
    if deploy_function(openwebui_url, auth_token):
        # Test availability
        test_function_availability(openwebui_url, auth_token)
        
        print("\n" + "=" * 60)
        print("🎉 Deployment Complete!")
        print("\n📋 Next Steps:")
        print("1. Go to OpenWebUI at http://localhost:3003")
        print("2. Look for 'DeepResearch Enhanced Threat Modeling' in functions")
        print("3. Test with: 'Generate a threat model for my web application'")
        print("4. Monitor logs with: docker logs open-webui")
        print("\n🔍 Test Queries:")
        print("- 'Create a threat model for e-commerce platform'")
        print("- 'Perform threat modeling for payment system'")
        print("- 'Generate Threagile YAML for microservices architecture'")
    else:
        print("\n❌ Deployment failed. Please check the error messages above.")
        print("\n🛠️  Troubleshooting:")
        print("1. Ensure OpenWebUI is running on localhost:3003")
        print("2. Check if authentication is required")
        print("3. Verify network connectivity")
        print("4. Check OpenWebUI logs: docker logs open-webui")

if __name__ == "__main__":
    main()
