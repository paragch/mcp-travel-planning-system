#!/usr/bin/env python3
"""
Simple test script for the MCP server greet function
"""
import json
import subprocess
import sys

def test_greet(name):
    """Test the greet function with a given name"""
    # Create the JSON-RPC request
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "greet",
            "arguments": {
                "name": name
            }
        }
    }
    
    # Convert to JSON string
    request_json = json.dumps(request)
    
    # Run the MCP server with the request
    try:
        result = subprocess.run(
            ["./venv/bin/python", "mcp_server.py"],
            input=request_json,
            text=True,
            capture_output=True,
            timeout=5
        )
        
        if result.returncode == 0:
            response = json.loads(result.stdout.strip())
            if "result" in response:
                greeting = response["result"]["content"][0]["text"]
                print(f"✅ Success: {greeting}")
            else:
                print(f"❌ Error: {response.get('error', 'Unknown error')}")
        else:
            print(f"❌ Process failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout: Server took too long to respond")
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    # Test with different names
    test_names = ["Alice", "Bob", "Charlie", "Parag", "World"]
    
    print("Testing MCP Server greet() function:")
    print("=" * 40)
    
    for name in test_names:
        print(f"\nTesting with name: '{name}'")
        test_greet(name)
    
    # Test with command line argument if provided
    if len(sys.argv) > 1:
        custom_name = sys.argv[1]
        print(f"\nTesting with custom name: '{custom_name}'")
        test_greet(custom_name)