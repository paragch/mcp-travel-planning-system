#!/usr/bin/env python3
"""
Test script for the Trainline MCP server
"""
import json
import subprocess

def test_trainline_function(function_name, arguments):
    """Test a specific Trainline MCP function"""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": function_name,
            "arguments": arguments
        }
    }
    
    request_json = json.dumps(request)
    
    try:
        result = subprocess.Popen(
            ["./venv/bin/python", "trainline_mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = result.communicate(input=request_json.encode())
        
        if result.returncode == 0:
            response = json.loads(stdout.decode().strip())
            if "result" in response:
                content = response["result"]["content"][0]["text"]
                print(f"✅ {function_name} Success:")
                print(content)
                print("\n" + "="*60 + "\n")
            else:
                print(f"❌ {function_name} Error: {response.get('error', 'Unknown error')}")
        else:
            print(f"❌ {function_name} Process failed: {stderr.decode()}")
            
    except Exception as e:
        print(f"❌ {function_name} Unexpected error: {e}")

if __name__ == "__main__":
    print("🚂 Testing Trainline MCP Server")
    print("=" * 60)
    
    # Test 1: Search for trains
    print("Test 1: Search trains from London to Manchester")
    test_trainline_function("search_trains", {
        "from_station": "London",
        "to_station": "Manchester", 
        "date": "2024-12-25",
        "time": "10:00"
    })
    
    # Test 2: Get station info
    print("Test 2: Get information about Manchester Piccadilly")
    test_trainline_function("get_station_info", {
        "station_name": "Manchester Piccadilly"
    })
    
    # Test 3: Find stations
    print("Test 3: Find stations in Birmingham")
    test_trainline_function("find_stations", {
        "search_term": "Birmingham"
    })
    
    # Test 4: Get popular routes
    print("Test 4: Get popular routes in France")
    test_trainline_function("get_popular_routes", {
        "country": "FR"
    })
    
    print("🎉 All tests completed!")