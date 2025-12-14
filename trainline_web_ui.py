#!/usr/bin/env python3
"""
Trainline Web UI - Flask-based web interface for Trainline MCP client
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import subprocess
from datetime import datetime, timedelta
import os

app = Flask(__name__)

class TrainlineWebClient:
    def __init__(self):
        self.server_script = "trainline_mcp_server.py"
        self.python_path = "./venv/bin/python"
    
    def call_mcp_server(self, method: str, params: dict) -> dict:
        """Call the MCP server and return structured response"""
        request_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        
        try:
            process = subprocess.Popen(
                [self.python_path, self.server_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = process.communicate(input=json.dumps(request_data).encode())
            
            if process.returncode == 0:
                response = json.loads(stdout.decode().strip())
                if "result" in response:
                    return {
                        "success": True,
                        "data": response["result"]["content"][0]["text"]
                    }
                else:
                    return {
                        "success": False,
                        "error": response.get("error", {}).get("message", "Unknown error")
                    }
            else:
                return {
                    "success": False,
                    "error": f"Server error: {stderr.decode()}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Client error: {str(e)}"
            }

# Initialize the client
client = TrainlineWebClient()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/search_trains', methods=['POST'])
def api_search_trains():
    """API endpoint for train search"""
    data = request.get_json()
    
    from_station = data.get('from_station', '').strip()
    to_station = data.get('to_station', '').strip()
    date = data.get('date', '').strip()
    time = data.get('time', '').strip()
    
    if not from_station or not to_station:
        return jsonify({
            "success": False,
            "error": "Please provide both departure and destination stations"
        })
    
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    params = {
        "name": "search_trains",
        "arguments": {
            "from_station": from_station,
            "to_station": to_station,
            "date": date
        }
    }
    
    if time:
        params["arguments"]["time"] = time
    
    result = client.call_mcp_server("tools/call", params)
    return jsonify(result)

@app.route('/api/station_info', methods=['POST'])
def api_station_info():
    """API endpoint for station information"""
    data = request.get_json()
    station_name = data.get('station_name', '').strip()
    
    if not station_name:
        return jsonify({
            "success": False,
            "error": "Please provide a station name"
        })
    
    params = {
        "name": "get_station_info",
        "arguments": {
            "station_name": station_name
        }
    }
    
    result = client.call_mcp_server("tools/call", params)
    return jsonify(result)

@app.route('/api/find_stations', methods=['POST'])
def api_find_stations():
    """API endpoint for finding stations"""
    data = request.get_json()
    search_term = data.get('search_term', '').strip()
    
    if not search_term:
        return jsonify({
            "success": False,
            "error": "Please provide a search term"
        })
    
    params = {
        "name": "find_stations",
        "arguments": {
            "search_term": search_term
        }
    }
    
    result = client.call_mcp_server("tools/call", params)
    return jsonify(result)

@app.route('/api/popular_routes')
def api_popular_routes():
    """API endpoint for popular routes"""
    country = request.args.get('country', 'UK')
    
    params = {
        "name": "get_popular_routes",
        "arguments": {
            "country": country
        }
    }
    
    result = client.call_mcp_server("tools/call", params)
    return jsonify(result)

@app.route('/api/quick_routes')
def api_quick_routes():
    """API endpoint for quick route suggestions"""
    routes = [
        {"from": "London", "to": "Edinburgh", "description": "London to Edinburgh (East Coast)"},
        {"from": "London", "to": "Manchester", "description": "London to Manchester (West Coast)"},
        {"from": "London", "to": "Birmingham", "description": "London to Birmingham"},
        {"from": "Manchester", "to": "Liverpool", "description": "Manchester to Liverpool"},
        {"from": "London", "to": "Bristol", "description": "London to Bristol"},
        {"from": "Birmingham", "to": "<Location A>", "description": "Birmingham to <Location A>"},
        {"from": "London", "to": "Glasgow", "description": "London to Glasgow"},
        {"from": "Newcastle", "to": "London", "description": "Newcastle to London"},
        {"from": "Cardiff", "to": "London", "description": "Cardiff to London"},
        {"from": "Edinburgh", "to": "Glasgow", "description": "Edinburgh to Glasgow"}
    ]
    
    return jsonify({"success": True, "routes": routes})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    print("🚂 Starting Trainline Web UI...")
    print("📱 Open your browser to: http://localhost:5001")
    print("🔄 Connecting to MCP server...")
    
    # Test MCP connection
    test_result = client.call_mcp_server("tools/call", {
        "name": "get_popular_routes",
        "arguments": {"country": "UK"}
    })
    
    if test_result["success"]:
        print("✅ MCP server connection successful!")
    else:
        print(f"❌ MCP server connection failed: {test_result['error']}")
        print("⚠️  Web UI will start but may not function properly")
    
    app.run(debug=True, host='0.0.0.0', port=5001)