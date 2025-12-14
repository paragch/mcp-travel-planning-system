#!/usr/bin/env python3
"""
Quick Train Search - Simple command-line tool for UK train queries
Usage: python quick_train_search.py [from] [to] [date] [time]
"""
import sys
import json
import subprocess
from datetime import datetime, timedelta

class QuickTrainSearch:
    def __init__(self):
        self.server_script = "trainline_mcp_server.py"
        self.python_path = "./venv/bin/python"
    
    def call_server(self, tool_name: str, arguments: dict) -> str:
        """Call the MCP server"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        try:
            process = subprocess.Popen(
                [self.python_path, self.server_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = process.communicate(input=json.dumps(request).encode())
            
            if process.returncode == 0:
                response = json.loads(stdout.decode().strip())
                if "result" in response:
                    return response["result"]["content"][0]["text"]
                else:
                    return f"❌ Error: {response.get('error', {}).get('message', 'Unknown error')}"
            else:
                return f"❌ Server Error: {stderr.decode()}"
                
        except Exception as e:
            return f"❌ Client Error: {e}"
    
    def search_trains(self, from_station: str, to_station: str, date: str = None, time: str = None):
        """Search for trains"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        arguments = {
            "from_station": from_station,
            "to_station": to_station,
            "date": date
        }
        
        if time:
            arguments["time"] = time
        
        return self.call_server("search_trains", arguments)
    
    def show_help(self):
        """Show usage help"""
        help_text = """
🚂 Quick Train Search - UK Journey Planner

USAGE:
    python quick_train_search.py [from] [to] [date] [time]

EXAMPLES:
    python quick_train_search.py London Manchester
    python quick_train_search.py London Edinburgh 2024-12-25
    python quick_train_search.py Birmingham Liverpool 2024-12-20 09:30

PARAMETERS:
    from     - Departure station (required)
    to       - Destination station (required)  
    date     - Travel date in YYYY-MM-DD format (optional, defaults to today)
    time     - Departure time in HH:MM format (optional)

POPULAR UK ROUTES:
    • London ↔ Edinburgh
    • London ↔ Manchester  
    • London ↔ Birmingham
    • Manchester ↔ Liverpool
    • London ↔ Bristol
    • Birmingham ↔ Leeds

SHORTCUTS:
    python quick_train_search.py --popular    # Show popular routes
    python quick_train_search.py --help       # Show this help
        """
        print(help_text)

def main():
    searcher = QuickTrainSearch()
    
    if len(sys.argv) == 1 or "--help" in sys.argv:
        searcher.show_help()
        return
    
    if "--popular" in sys.argv:
        result = searcher.call_server("get_popular_routes", {"country": "UK"})
        print(result)
        return
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    if len(args) < 2:
        print("❌ Error: Please provide at least departure and destination stations.")
        print("Usage: python quick_train_search.py [from] [to] [date] [time]")
        print("Use --help for more information.")
        return
    
    from_station = args[0]
    to_station = args[1]
    date = args[2] if len(args) > 2 else None
    time = args[3] if len(args) > 3 else None
    
    # Validate date format if provided
    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print(f"❌ Invalid date format: {date}")
            print("Please use YYYY-MM-DD format (e.g., 2024-12-25)")
            return
    
    # Validate time format if provided
    if time:
        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            print(f"❌ Invalid time format: {time}")
            print("Please use HH:MM format (e.g., 09:30)")
            return
    
    print(f"🔍 Searching trains: {from_station} → {to_station}")
    if date:
        print(f"📅 Date: {date}")
    if time:
        print(f"⏰ Time: {time}")
    print("-" * 50)
    
    result = searcher.search_trains(from_station, to_station, date, time)
    print(result)

if __name__ == "__main__":
    main()