#!/usr/bin/env python3
"""
Setup script for Real Train API integration
"""
import os
import json

def setup_transport_api():
    """Guide user through Transport API setup"""
    print("🚂 Real Train API Setup")
    print("=" * 40)
    print()
    
    print("To get live UK train data, you need a Transport API account:")
    print("1. Visit: https://transportapi.com")
    print("2. Click 'Sign Up' (free tier available)")
    print("3. Verify your email")
    print("4. Go to 'My Account' → 'API Keys'")
    print("5. Copy your App ID and API Key")
    print()
    
    # Get API credentials from user
    app_id = input("Enter your Transport API App ID: ").strip()
    api_key = input("Enter your Transport API Key: ").strip()
    
    if not app_id or not api_key:
        print("❌ Both App ID and API Key are required!")
        return False
    
    # Update the server file
    try:
        with open('real_trainline_mcp_server.py', 'r') as f:
            content = f.read()
        
        # Replace placeholder values
        content = content.replace('self.transport_api_key = "YOUR_TRANSPORT_API_KEY"', 
                                f'self.transport_api_key = "{api_key}"')
        content = content.replace('self.transport_app_id = "YOUR_TRANSPORT_APP_ID"', 
                                f'self.transport_app_id = "{app_id}"')
        
        with open('real_trainline_mcp_server.py', 'w') as f:
            f.write(content)
        
        print("✅ API credentials configured successfully!")
        
        # Update MCP configuration
        update_mcp_config()
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating configuration: {e}")
        return False

def update_mcp_config():
    """Update MCP configuration to use real API server"""
    try:
        config_path = '.kiro/settings/mcp.json'
        
        # Read current config
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Add real API server
        config['mcpServers']['real-trainline'] = {
            "command": "./venv/bin/python",
            "args": ["real_trainline_mcp_server.py"],
            "disabled": False
        }
        
        # Optionally disable demo server
        if 'trainline-connector' in config['mcpServers']:
            config['mcpServers']['trainline-connector']['disabled'] = True
        
        # Write updated config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ MCP configuration updated!")
        print("📝 Added 'real-trainline' server")
        print("⏸️  Disabled demo 'trainline-connector' server")
        
    except Exception as e:
        print(f"❌ Error updating MCP config: {e}")

def test_api_connection():
    """Test the API connection"""
    print("\n🔄 Testing API connection...")
    
    try:
        import subprocess
        
        # Test the real server
        test_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "find_station_codes",
                "arguments": {
                    "search_term": "London"
                }
            }
        }
        
        process = subprocess.Popen(
            ["./venv/bin/python", "real_trainline_mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, stderr = process.communicate(input=json.dumps(test_request).encode())
        
        if process.returncode == 0:
            response = json.loads(stdout.decode().strip())
            if "result" in response:
                print("✅ API server is working!")
                print("🎉 You can now get live UK train data!")
                return True
            else:
                print(f"❌ Server error: {response.get('error', 'Unknown error')}")
        else:
            print(f"❌ Process error: {stderr.decode()}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    return False

def show_api_features():
    """Show what features are available with real API"""
    print("\n🌟 Real API Features Available:")
    print("=" * 40)
    print("✅ Live departure times")
    print("✅ Real-time delays and cancellations")
    print("✅ Platform information")
    print("✅ Journey planning with connections")
    print("✅ Operator information")
    print("✅ Station departure boards")
    print("✅ Service disruption alerts")
    print()
    print("🎯 Available Functions:")
    print("• search_live_trains - Live train search")
    print("• get_live_departures - Station departure board")
    print("• find_station_codes - Find station codes")
    print("• get_journey_details - Detailed journey info")
    print()
    print("💡 Free tier includes:")
    print("• 1,000 requests per day")
    print("• All UK rail data")
    print("• Real-time updates")

def main():
    print("🚂 Welcome to Real Train API Setup!")
    print()
    
    # Check if already configured
    try:
        with open('real_trainline_mcp_server.py', 'r') as f:
            content = f.read()
            if 'YOUR_TRANSPORT_API_KEY' not in content:
                print("✅ API appears to already be configured!")
                choice = input("Reconfigure? (y/N): ").strip().lower()
                if choice != 'y':
                    test_api_connection()
                    return
    except FileNotFoundError:
        print("❌ real_trainline_mcp_server.py not found!")
        return
    
    # Setup process
    if setup_transport_api():
        if test_api_connection():
            show_api_features()
            print("\n🎉 Setup complete! Your MCP server now has live UK train data!")
            print("🔄 Restart your web UI to use the new features.")
        else:
            print("\n⚠️  Setup completed but test failed. Check your API credentials.")
    else:
        print("\n❌ Setup failed. Please try again.")

if __name__ == "__main__":
    main()