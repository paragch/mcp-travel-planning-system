#!/usr/bin/env python3
"""
Travel Planner Client - Comprehensive travel planning using Trainline + Multi-Hotel MCP servers
"""
import json
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class TravelPlannerClient:
    def __init__(self):
        self.python_path = "./venv/bin/python"
        self.trainline_server = "real_trainline_mcp_server.py"
        self.hotels_server = "multi_hotel_api_server.py"
    
    def call_mcp_server(self, server_script: str, tool_name: str, arguments: dict) -> Optional[str]:
        """Call a specific MCP server tool"""
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
                [self.python_path, server_script],
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
                    return f"Error: {response.get('error', {}).get('message', 'Unknown error')}"
            else:
                return f"Server error: {stderr.decode()}"
                
        except Exception as e:
            return f"Client error: {str(e)}"
    
    def plan_complete_trip(self, from_city: str, to_city: str, travel_date: str, 
                          return_date: str = None, guests: int = 2) -> str:
        """Plan a complete trip with trains and hotels"""
        print(f"🎯 Planning complete trip: {from_city} → {to_city}")
        
        result = f"""🧳 Complete Travel Plan: {from_city} → {to_city}
{'='*60}
📅 Travel Date: {travel_date}
{f'📅 Return Date: {return_date}' if return_date else '📅 One-way trip'}
👥 Guests: {guests}

"""
        
        # 1. Search for outbound trains
        print("🚂 Searching outbound trains...")
        train_search = self.call_mcp_server(
            self.trainline_server,
            "search_live_trains",
            {
                "from_station": from_city,
                "to_station": to_city,
                "date": travel_date
            }
        )
        
        result += f"""🚂 OUTBOUND TRAINS
{'-'*30}
{train_search}

"""
        
        # 2. Search for return trains if return date provided
        if return_date:
            print("🚂 Searching return trains...")
            return_train_search = self.call_mcp_server(
                self.trainline_server,
                "search_live_trains",
                {
                    "from_station": to_city,
                    "to_station": from_city,
                    "date": return_date
                }
            )
            
            result += f"""🚂 RETURN TRAINS
{'-'*30}
{return_train_search}

"""
        
        # 3. Search for hotels in destination
        print("🏨 Searching hotels...")
        checkout_date = return_date if return_date else (
            datetime.strptime(travel_date, "%Y-%m-%d") + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        
        hotel_search = self.call_mcp_server(
            self.hotels_server,
            "search_hotels_multi",
            {
                "location": to_city,
                "checkin": travel_date,
                "checkout": checkout_date,
                "guests": guests
            }
        )
        
        result += f"""🏨 ACCOMMODATION
{'-'*30}
{hotel_search}

"""
        
        # 4. Get destination information
        print("📍 Getting destination info...")
        station_info = self.call_mcp_server(
            self.trainline_server,
            "find_station_codes",
            {
                "search_term": to_city
            }
        )
        
        result += f"""📍 DESTINATION INFO
{'-'*30}
{station_info}

"""
        
        # 5. Add travel tips
        result += f"""💡 TRAVEL PLANNING TIPS
{'-'*30}
🎫 BOOKING STRATEGY:
• Book trains in advance for better prices
• Consider off-peak times for savings
• Check for railcard discounts
• Look for advance purchase tickets

🏨 HOTEL TIPS:
• Compare prices across dates
• Read recent guest reviews
• Check cancellation policies
• Consider location vs. price

🧳 PACKING ESSENTIALS:
• Valid ID for travel
• Booking confirmations
• Travel insurance documents
• Weather-appropriate clothing

📱 USEFUL APPS:
• Trainline app for mobile tickets
• Hotels.com app for hotel management
• Local transport apps
• Weather forecast apps

🔗 QUICK LINKS:
• Trainline: https://www.trainline.com
• Hotels.com: https://www.hotels.com
• National Rail: https://www.nationalrail.co.uk

"""
        
        return result
    
    def find_hotels_near_station(self, city: str, station_name: str, checkin: str, checkout: str) -> str:
        """Find hotels near a specific train station"""
        print(f"🏨 Finding hotels near {station_name} in {city}")
        
        # Use general hotel search for the station area
        return self.call_mcp_server(
            self.hotels_server,
            "search_hotels_multi",
            {
                "location": f"{city} {station_name}",
                "checkin": checkin,
                "checkout": checkout,
                "guests": 2
            }
        )
    
    def compare_travel_costs(self, destinations: List[str], travel_date: str, return_date: str) -> str:
        """Compare travel costs across multiple destinations"""
        print(f"💰 Comparing costs for destinations: {', '.join(destinations)}")
        
        result = f"""💰 Travel Cost Comparison
{'='*50}
📅 Travel: {travel_date} → {return_date}
🏙️  Destinations: {', '.join(destinations)}

"""
        
        # Compare hotel prices across destinations
        hotel_comparisons = []
        for destination in destinations:
            hotel_result = self.call_mcp_server(
                self.hotels_server,
                "search_hotels_multi",
                {
                    "location": destination,
                    "checkin": travel_date,
                    "checkout": return_date,
                    "guests": 2
                }
            )
            if hotel_result:
                hotel_comparisons.append(f"📍 {destination}:\n{hotel_result}\n")
        
        hotel_comparison = "\n".join(hotel_comparisons) if hotel_comparisons else "No hotel data available"
        
        result += f"""🏨 HOTEL PRICE COMPARISON
{'-'*30}
{hotel_comparison}

"""
        
        # Get train info for each destination
        result += f"""🚂 TRAIN INFORMATION
{'-'*30}
"""
        
        for dest in destinations:
            train_info = self.call_mcp_server(
                self.trainline_server,
                "search_live_trains",
                {
                    "from_station": "London",  # Assuming London as starting point
                    "to_station": dest,
                    "date": travel_date
                }
            )
            
            result += f"""
📍 TO {dest.upper()}:
{train_info[:300]}...
"""
        
        return result
    
    def get_travel_suggestions(self, region: str = "Europe") -> str:
        """Get travel suggestions and popular destinations"""
        print(f"🌍 Getting travel suggestions for {region}")
        
        # Provide popular UK destinations (since multi-hotel server focuses on UK)
        destinations = f"""🌍 Popular UK Travel Destinations

🏴󠁧󠁢󠁥󠁮󠁧󠁿 ENGLAND:
• London - Historic capital with world-class museums
• Bath - Georgian architecture and Roman baths
• York - Medieval city with stunning cathedral
• Cambridge - University town with beautiful colleges
• Brighton - Seaside resort with vibrant culture

🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND:
• Edinburgh - Festival city with castle views
• Glasgow - Cultural hub with great museums
• Stirling - Historic castle and battlefields

🏴󠁧󠁢󠁷󠁬󠁳󠁿 WALES:
• Cardiff - Capital with castle and bay area
• Swansea - Coastal city near Gower Peninsula

💡 All destinations accessible by train via our system!"""
        
        # Get popular train routes
        train_routes = self.call_mcp_server(
            self.trainline_server,
            "get_popular_routes",
            {
                "country": "UK" if region == "Europe" else region
            }
        )
        
        result = f"""🌍 Travel Suggestions for {region}
{'='*50}

{destinations}

{train_routes}

💡 PLANNING YOUR TRIP:
• Consider shoulder seasons for better prices
• Book accommodation and transport together
• Check visa requirements for international travel
• Research local customs and etiquette
• Plan for currency exchange
• Consider travel insurance

🎯 NEXT STEPS:
1. Choose your destination
2. Select travel dates
3. Book trains in advance
4. Reserve accommodation
5. Plan activities and attractions
6. Prepare travel documents

"""
        
        return result

def interactive_travel_planner():
    """Interactive travel planning session"""
    planner = TravelPlannerClient()
    
    print("🧳 Welcome to the Complete Travel Planner!")
    print("=" * 50)
    print("I can help you plan trips using Trainline and UK hotel chains")
    print()
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Plan a complete trip (trains + hotels)")
        print("2. Find hotels near a train station")
        print("3. Compare costs across destinations")
        print("4. Get travel suggestions")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        try:
            if choice == "1":
                from_city = input("From city: ").strip()
                to_city = input("To city: ").strip()
                travel_date = input("Travel date (YYYY-MM-DD): ").strip()
                return_date = input("Return date (YYYY-MM-DD, or press Enter for one-way): ").strip()
                guests = int(input("Number of guests (default 2): ").strip() or "2")
                
                if not return_date:
                    return_date = None
                
                result = planner.plan_complete_trip(from_city, to_city, travel_date, return_date, guests)
                print("\n" + result)
                
            elif choice == "2":
                city = input("City: ").strip()
                station = input("Station name: ").strip()
                checkin = input("Check-in date (YYYY-MM-DD): ").strip()
                checkout = input("Check-out date (YYYY-MM-DD): ").strip()
                
                result = planner.find_hotels_near_station(city, station, checkin, checkout)
                print("\n" + result)
                
            elif choice == "3":
                destinations_input = input("Destinations (comma-separated): ").strip()
                destinations = [d.strip() for d in destinations_input.split(",")]
                travel_date = input("Travel date (YYYY-MM-DD): ").strip()
                return_date = input("Return date (YYYY-MM-DD): ").strip()
                
                result = planner.compare_travel_costs(destinations, travel_date, return_date)
                print("\n" + result)
                
            elif choice == "4":
                region = input("Region (Europe, Asia, etc., or press Enter for Europe): ").strip() or "Europe"
                
                result = planner.get_travel_suggestions(region)
                print("\n" + result)
                
            elif choice == "5":
                print("👋 Happy travels!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    interactive_travel_planner()