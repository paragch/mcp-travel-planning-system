#!/usr/bin/env python3
"""
Test Web Interface Integration
"""
import requests
import json

def test_web_interface():
    """Test the web interface API endpoints"""
    
    print("🌐 Testing Web Interface Integration")
    print("=" * 50)
    
    base_url = "http://localhost:5002"
    
    # Test 1: Check if server is running
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Web server is running")
        else:
            print(f"❌ Web server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to web server: {e}")
        return False
    
    # Test 2: Check capabilities endpoint
    try:
        response = requests.get(f"{base_url}/api/capabilities", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Capabilities endpoint working")
            
            servers = data.get('servers', {})
            print(f"📋 Connected servers: {list(servers.keys())}")
            
            if 'multi_hotels' in servers:
                print("✅ Multi-hotels server detected in web interface")
                tools = servers['multi_hotels'].get('tools', [])
                print(f"🔧 Multi-hotels tools: {[t.get('name') for t in tools]}")
            else:
                print("❌ Multi-hotels server not found in web interface")
                
        else:
            print(f"❌ Capabilities endpoint error: {response.status_code}")
    except Exception as e:
        print(f"❌ Capabilities endpoint failed: {e}")
    
    # Test 3: Test hotel search via web API
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json={"message": "hotels in <Location B> for December 15-16"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get('reply', '')
            
            if 'Premier Inn <Location B>' in reply:
                print("✅ Hotel search working via web interface!")
                print("📋 Sample response:")
                print(reply[:300] + "...")
            else:
                print("⚠️  Hotel search response received but no hotel data:")
                print(reply[:200] + "...")
        else:
            print(f"❌ Chat endpoint error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Chat endpoint failed: {e}")
    
    return True

def main():
    print("🧪 Web Interface Integration Test")
    print("This tests if the Multi-API Hotel Server is working via the web interface")
    print()
    
    success = test_web_interface()
    
    if success:
        print("\n🎯 CONCLUSION:")
        print("Web interface is accessible. Check the test results above.")
        print("If multi-hotels server is detected, the integration is working!")
    else:
        print("\n❌ Web interface is not accessible")
        print("Make sure the web server is running: python strand_agent_web.py")

if __name__ == "__main__":
    main()