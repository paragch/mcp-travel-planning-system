#!/usr/bin/env python3
"""
Trainline MCP Client - Interactive client to query trains between UK destinations
"""
import json
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class TrainlineMCPClient:
    def __init__(self, server_script="trainline_mcp_server.py"):
        self.server_script = server_script
        self.python_path = "./venv/bin/python"
        
    def call_mcp_server(self, method: str, params: Dict[str, Any]) -> Optional[str]:
        """Call the MCP server with a specific method and parameters"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        
        request_json = json.dumps(request)
        
        try:
            process = subprocess.Popen(
                [self.python_path, self.server_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = process.communicate(input=request_json.encode())
            
            if process.returncode == 0:
                response = json.loads(stdout.decode().strip())
                if "result" in response:
                    return response["result"]["content"][0]["text"]
                else:
                    print(f"❌ Server Error: {response.get('error', {}).get('message', 'Unknown error')}")
                    return None
            else:
                print(f"❌ Process Error: {stderr.decode()}")
                return None
                
        except Exception as e:
            print(f"❌ Client Error: {e}")
            return None
    
    def search_trains(self, from_station: str, to_station: str, date: str, time: Optional[str] = None) -> Optional[str]:
        """Search for trains between two stations"""
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
            
        return self.call_mcp_server("tools/call", params)
    
    def get_station_info(self, station_name: str) -> Optional[str]:
        """Get information about a station"""
        params = {
            "name": "get_station_info",
            "arguments": {
                "station_name": station_name
            }
        }
        
        return self.call_mcp_server("tools/call", params)
    
    def find_stations(self, search_term: str) -> Optional[str]:
        """Find stations matching a search term"""
        params = {
            "name": "find_stations",
            "arguments": {
                "search_term": search_term
            }
        }
        
        return self.call_mcp_server("tools/call", params)
    
    def get_popular_routes(self, country: str = "UK") -> Optional[str]:
        """Get popular routes for a country"""
        params = {
            "name": "get_popular_routes",
            "arguments": {
                "country": country
            }
        }
        
        return self.call_mcp_server("tools/call", params)

class TrainlineUI:
    def __init__(self):
        self.client = TrainlineMCPClient()
        self.uk_stations = [
            "London", "Manchester", "Birmingham", "Liverpool", "Edinburgh", 
            "Glasgow", "Bristol", "<Location A>", "Sheffield", "Newcastle",
            "Cardiff", "Nottingham", "Leicester", "Coventry", "Bradford",
            "Oxford", "Cambridge", "Brighton", "Portsmouth", "Southampton"
        ]
    
    def display_menu(self):
        """Display the main menu"""
        print("\n🚂 Trainline UK Journey Planner")
        print("=" * 40)
        print("1. Search for trains")
        print("2. Get station information")
        print("3. Find stations in a city")
        print("4. View popular UK routes")
        print("5. Quick search (common routes)")
        print("6. Exit")
        print("=" * 40)
    
    def get_date_input(self) -> str:
        """Get travel date from user with helpful prompts"""
        print("\n📅 Travel Date Options:")
        print("1. Today")
        print("2. Tomorrow") 
        print("3. Custom date (YYYY-MM-DD)")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == "1":
            return datetime.now().strftime("%Y-%m-%d")
        elif choice == "2":
            return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif choice == "3":
            date_str = input("Enter date (YYYY-MM-DD): ").strip()
            try:
                # Validate date format
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                print("❌ Invalid date format. Using today instead.")
                return datetime.now().strftime("%Y-%m-%d")
        else:
            print("❌ Invalid choice. Using today.")
            return datetime.now().strftime("%Y-%m-%d")
    
    def search_trains_interactive(self):
        """Interactive train search"""
        print("\n🔍 Train Search")
        print("-" * 20)
        
        from_station = input("From station: ").strip()
        to_station = input("To station: ").strip()
        
        if not from_station or not to_station:
            print("❌ Please enter both departure and arrival stations.")
            return
        
        date = self.get_date_input()
        
        time_input = input("Preferred departure time (HH:MM, or press Enter to skip): ").strip()
        time = time_input if time_input else None
        
        print(f"\n🔄 Searching trains from {from_station} to {to_station} on {date}...")
        
        result = self.client.search_trains(from_station, to_station, date, time)
        if result:
            print("\n" + result)
        else:
            print("❌ Failed to get train information.")
    
    def get_station_info_interactive(self):
        """Interactive station information lookup"""
        print("\n🚉 Station Information")
        print("-" * 22)
        
        station = input("Enter station name: ").strip()
        
        if not station:
            print("❌ Please enter a station name.")
            return
        
        print(f"\n🔄 Getting information for {station}...")
        
        result = self.client.get_station_info(station)
        if result:
            print("\n" + result)
        else:
            print("❌ Failed to get station information.")
    
    def find_stations_interactive(self):
        """Interactive station finder"""
        print("\n🔍 Find Stations")
        print("-" * 16)
        
        city = input("Enter city or area name: ").strip()
        
        if not city:
            print("❌ Please enter a city name.")
            return
        
        print(f"\n🔄 Finding stations in {city}...")
        
        result = self.client.find_stations(city)
        if result:
            print("\n" + result)
        else:
            print("❌ Failed to find stations.")
    
    def show_popular_routes(self):
        """Show popular UK routes"""
        print("\n🔄 Getting popular UK routes...")
        
        result = self.client.get_popular_routes("UK")
        if result:
            print("\n" + result)
        else:
            print("❌ Failed to get popular routes.")
    
    def quick_search_menu(self):
        """Quick search for common UK routes"""
        print("\n⚡ Quick Search - Popular UK Routes")
        print("-" * 35)
        
        routes = [
            ("London", "Edinburgh"),
            ("London", "Manchester"),
            ("London", "Birmingham"),
            ("Manchester", "Liverpool"),
            ("London", "Bristol"),
            ("Birmingham", "<Location A>"),
            ("Custom route", "")
        ]
        
        for i, (from_city, to_city) in enumerate(routes, 1):
            if to_city:
                print(f"{i}. {from_city} → {to_city}")
            else:
                print(f"{i}. {from_city}")
        
        choice = input("\nChoose route (1-7): ").strip()
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(routes) - 1:
                from_station, to_station = routes[choice_idx]
                date = self.get_date_input()
                
                print(f"\n🔄 Searching {from_station} to {to_station} on {date}...")
                result = self.client.search_trains(from_station, to_station, date)
                if result:
                    print("\n" + result)
                else:
                    print("❌ Failed to get train information.")
            elif choice_idx == len(routes) - 1:
                self.search_trains_interactive()
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def run(self):
        """Main application loop"""
        print("🚂 Welcome to Trainline UK Journey Planner!")
        print("Connecting to MCP server...")
        
        # Test connection
        test_result = self.client.get_popular_routes("UK")
        if not test_result:
            print("❌ Failed to connect to MCP server. Please ensure the server is configured correctly.")
            return
        
        print("✅ Connected to Trainline MCP server!")
        
        while True:
            try:
                self.display_menu()
                choice = input("\nChoose an option (1-6): ").strip()
                
                if choice == "1":
                    self.search_trains_interactive()
                elif choice == "2":
                    self.get_station_info_interactive()
                elif choice == "3":
                    self.find_stations_interactive()
                elif choice == "4":
                    self.show_popular_routes()
                elif choice == "5":
                    self.quick_search_menu()
                elif choice == "6":
                    print("\n👋 Thank you for using Trainline Journey Planner!")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-6.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("Press Enter to continue...")

if __name__ == "__main__":
    app = TrainlineUI()
    app.run()