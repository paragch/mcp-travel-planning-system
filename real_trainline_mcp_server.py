#!/usr/bin/env python3
"""
Real Trainline MCP Server - Connects to actual UK train APIs for live data
"""
import json
import sys
import requests
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
import urllib.parse
import xml.etree.ElementTree as ET

class RealTrainlineMCPServer:
    def __init__(self):
        self.tools = {}
        
        # API Configuration
        self.national_rail_api = "https://lite.realtime.nationalrail.co.uk/OpenLDBWS/ldb12.asmx"
        self.trainline_api = "https://www.trainline.com/api"
        self.transport_api_base = "https://transportapi.com/v3/uk"
        
        # You'll need to get these API keys (free registration)
        self.transport_api_key = "55eadb1b8f2e648fcaf0de14a8f297b2"  # Get from transportapi.com
        self.transport_app_id = "d948d452"
        
        # Register all available tools
        self.register_tool("search_live_trains", self.search_live_trains, {
            "type": "function",
            "function": {
                "name": "search_live_trains",
                "description": "Search for live train times and prices between two UK stations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from_station": {
                            "type": "string",
                            "description": "Departure station code or name (e.g., 'KGX' for King's Cross or 'London')"
                        },
                        "to_station": {
                            "type": "string",
                            "description": "Arrival station code or name (e.g., 'EDB' for Edinburgh or 'Edinburgh')"
                        },
                        "date": {
                            "type": "string",
                            "description": "Travel date in YYYY-MM-DD format"
                        },
                        "time": {
                            "type": "string",
                            "description": "Departure time in HH:MM format (optional)"
                        }
                    },
                    "required": ["from_station", "to_station", "date"]
                }
            }
        })
        
        self.register_tool("get_live_departures", self.get_live_departures, {
            "type": "function",
            "function": {
                "name": "get_live_departures",
                "description": "Get live departure board for a specific station.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "station_code": {
                            "type": "string",
                            "description": "3-letter station code (e.g., 'KGX', 'MAN', 'EDB')"
                        },
                        "destination": {
                            "type": "string",
                            "description": "Filter by destination (optional)"
                        }
                    },
                    "required": ["station_code"]
                }
            }
        })
        
        self.register_tool("find_station_codes", self.find_station_codes, {
            "type": "function",
            "function": {
                "name": "find_station_codes",
                "description": "Find station codes for a given station name or city.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_term": {
                            "type": "string",
                            "description": "Station name or city to search for"
                        }
                    },
                    "required": ["search_term"]
                }
            }
        })
        
        self.register_tool("get_journey_details", self.get_journey_details, {
            "type": "function",
            "function": {
                "name": "get_journey_details",
                "description": "Get detailed journey information including changes and duration.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from_code": {
                            "type": "string",
                            "description": "Departure station code"
                        },
                        "to_code": {
                            "type": "string",
                            "description": "Arrival station code"
                        },
                        "date": {
                            "type": "string",
                            "description": "Travel date in YYYY-MM-DD format"
                        },
                        "time": {
                            "type": "string",
                            "description": "Departure time in HH:MM format"
                        }
                    },
                    "required": ["from_code", "to_code", "date", "time"]
                }
            }
        })

    def register_tool(self, name: str, func, schema: Dict[str, Any]):
        self.tools[name] = {"func": func, "schema": schema}

    def get_station_code(self, station_name: str) -> str:
        """Convert station name to 3-letter code"""
        # Common UK station codes mapping
        station_codes = {
            "london": "KGX",  # Default London to King's Cross for better results
            "london kings cross": "KGX", 
            "london king's cross": "KGX",
            "kings cross": "KGX",
            "king's cross": "KGX",
            "london paddington": "PAD",
            "paddington": "PAD",
            "london victoria": "VIC",
            "victoria": "VIC",
            "london waterloo": "WAT",
            "waterloo": "WAT",
            "london euston": "EUS",
            "euston": "EUS",
            "london liverpool street": "LST",
            "liverpool street": "LST",
            "manchester": "MAN",
            "manchester piccadilly": "MAN",
            "birmingham": "BHM",
            "birmingham new street": "BHM",
            "edinburgh": "EDB",
            "edinburgh waverley": "EDB",
            "glasgow": "GLC",
            "glasgow central": "GLC",
            "liverpool": "LIV",
            "liverpool lime street": "LIV",
            "leeds": "LDS",
            "bristol": "BRI",
            "bristol temple meads": "BRI",
            "cardiff": "CDF",
            "cardiff central": "CDF",
            "newcastle": "NCL",
            "newcastle central": "NCL",
            "sheffield": "SHF",
            "nottingham": "NOT",
            "oxford": "OXF",
            "cambridge": "CBG",
            "brighton": "BTN",
            "portsmouth": "PMS",
            "southampton": "SOU",
            # Add more specific mappings
            "york": "YRK",
            "bath": "BTH",
            "exeter": "EXD",
            "plymouth": "PLY",
            "reading": "RDG",
            "coventry": "COV",
            "derby": "DBY",
            "leicester": "LEI",
            "peterborough": "PBO",
            "doncaster": "DON",
            "wakefield": "WKF"
        }
        
        return station_codes.get(station_name.lower(), station_name.upper()[:3])

    def search_live_trains(self, from_station: str, to_station: str, date: str, time: Optional[str] = None) -> str:
        """Search for live train times using Transport API"""
        try:
            from_code = self.get_station_code(from_station)
            to_code = self.get_station_code(to_station)
            
            # Check if API keys are configured
            if self.transport_api_key == "YOUR_TRANSPORT_API_KEY" or self.transport_api_key == "1":
                return self._get_demo_search_results(from_station, to_station, date, time)
            
            # Format time for API
            if not time:
                time = "09:00"
            
            # Transport API endpoint
            url = f"{self.transport_api_base}/train/station/{from_code}/{date}/{time}/timetable.json"
            
            params = {
                "app_id": self.transport_app_id,
                "app_key": self.transport_api_key,
                "destination": to_code,
                "train_status": "passenger"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_live_results(data, from_station, to_station, date)
            else:
                return f"API Error: {response.status_code} - {response.text}"
                
        except requests.RequestException as e:
            return f"Network error: {str(e)}"
        except Exception as e:
            return f"Error searching trains: {str(e)}"

    def get_live_departures(self, station_code: str, destination: Optional[str] = None) -> str:
        """Get live departure board"""
        try:
            # Check if API keys are configured
            if self.transport_api_key == "YOUR_TRANSPORT_API_KEY" or self.transport_api_key == "1":
                return self._get_demo_departures(station_code, destination)
            
            url = f"{self.transport_api_base}/train/station/{station_code}/live.json"
            
            params = {
                "app_id": self.transport_app_id,
                "app_key": self.transport_api_key
            }
            
            if destination:
                params["destination"] = self.get_station_code(destination)
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_departures(data, station_code)
            else:
                return f"API Error: {response.status_code}"
                
        except Exception as e:
            return f"Error getting departures: {str(e)}"

    def find_station_codes(self, search_term: str) -> str:
        """Find station codes for a search term"""
        try:
            # Use a comprehensive station list
            stations_found = []
            
            # Search in our known stations
            station_codes = {
                "London King's Cross": "KGX",
                "London Paddington": "PAD", 
                "London Victoria": "VIC",
                "London Waterloo": "WAT",
                "London Euston": "EUS",
                "London Liverpool Street": "LST",
                "Manchester Piccadilly": "MAN",
                "Birmingham New Street": "BHM",
                "Edinburgh Waverley": "EDB",
                "Glasgow Central": "GLC",
                "Liverpool Lime Street": "LIV",
                "Leeds": "LDS",
                "Bristol Temple Meads": "BRI",
                "Cardiff Central": "CDF",
                "Newcastle Central": "NCL",
                "Sheffield": "SHF",
                "Nottingham": "NOT",
                "Oxford": "OXF",
                "Cambridge": "CBG",
                "Brighton": "BTN",
                "Portsmouth & Southsea": "PMS",
                "Southampton Central": "SOU"
            }
            
            search_lower = search_term.lower()
            
            for station_name, code in station_codes.items():
                if search_lower in station_name.lower():
                    stations_found.append(f"{station_name} ({code})")
            
            if stations_found:
                result = f"🔍 Stations matching '{search_term}':\n\n"
                for station in stations_found:
                    result += f"• {station}\n"
                
                result += f"\n💡 Use the 3-letter codes for more accurate searches"
                return result
            else:
                return f"No stations found matching '{search_term}'. Try searching for major cities like London, Manchester, Birmingham, etc."
                
        except Exception as e:
            return f"Error finding stations: {str(e)}"

    def get_journey_details(self, from_code: str, to_code: str, date: str, time: str) -> str:
        """Get detailed journey information"""
        try:
            # Check if API keys are configured
            if self.transport_api_key == "YOUR_TRANSPORT_API_KEY" or self.transport_api_key == "1":
                return self._get_demo_journey_details(from_code, to_code, date, time)
            
            url = f"{self.transport_api_base}/train/station/{from_code}/{date}/{time}/timetable.json"
            
            params = {
                "app_id": self.transport_app_id,
                "app_key": self.transport_api_key,
                "destination": to_code,
                "train_status": "passenger"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_journey_details(data, from_code, to_code)
            else:
                return f"API Error: {response.status_code}"
                
        except Exception as e:
            return f"Error getting journey details: {str(e)}"

    def _get_demo_search_results(self, from_station: str, to_station: str, date: str, time: Optional[str] = None) -> str:
        """Demo results when API keys are not configured"""
        current_time = datetime.now()
        
        result = f"""🚂 LIVE Train Search Results (Demo Mode)
{'='*50}
Route: {from_station} → {to_station}
Date: {date}
{f'Departure after: {time}' if time else ''}

⚠️  API CONFIGURATION NEEDED
To get real live data, please:
1. Register at https://transportapi.com (free tier available)
2. Get your API key and App ID
3. Update the configuration in the server

📋 Sample Live Results (what you'd see with real API):

🕐 09:15 → 13:45 (4h 30m) | Direct | £45.50
   Operator: LNER
   Platform: 4
   Status: On time

🕐 10:00 → 14:20 (4h 20m) | Direct | £52.00  
   Operator: LNER
   Platform: 3
   Status: On time

🕐 10:30 → 15:15 (4h 45m) | 1 change | £38.90
   Operator: CrossCountry
   Change at: Birmingham New Street
   Status: On time

💡 REAL API FEATURES:
• Live departure times
• Real-time delays and cancellations  
• Actual ticket prices
• Platform information
• Seat availability
• Journey planning with changes

🔗 For immediate booking: https://www.trainline.com
📞 National Rail Enquiries: 03457 48 49 50
        """
        
        return result.strip()

    def _get_demo_departures(self, station_code: str, destination: Optional[str] = None) -> str:
        """Demo departure board"""
        current_time = datetime.now()
        
        result = f"""🚉 LIVE Departures from {station_code} (Demo Mode)
{'='*50}
Updated: {current_time.strftime('%H:%M:%S')}

⚠️  Configure Transport API for real live data

📋 Sample Live Departures:

🕐 14:15 → London Paddington | Platform 1 | On time
   14:45 → Birmingham New Street | Platform 3 | Delayed 5 min
   15:00 → Edinburgh Waverley | Platform 2 | On time  
   15:30 → Manchester Piccadilly | Platform 4 | On time
   16:00 → Cardiff Central | Platform 1 | Cancelled

💡 REAL FEATURES WITH API:
• Live platform updates
• Real delay information
• Cancellation alerts
• Expected arrival times
• Service disruption notices

🔧 TO GET LIVE DATA:
1. Visit: https://transportapi.com
2. Register for free API access
3. Update server configuration
4. Get real-time UK rail data!
        """
        
        return result.strip()

    def _get_demo_journey_details(self, from_code: str, to_code: str, date: str, time: str) -> str:
        """Demo journey details"""
        result = f"""🚂 Journey Details: {from_code} → {to_code} (Demo Mode)
{'='*50}
Date: {date} | Departure: {time}

⚠️  Configure Transport API for detailed journey planning

📋 Sample Journey Details:

🚂 DIRECT SERVICE
Departure: {time} from {from_code}
Arrival: {(datetime.strptime(time, '%H:%M') + timedelta(hours=4)).strftime('%H:%M')} at {to_code}
Duration: 4h 0m
Operator: LNER
Train: 1E05

🎫 PRICING (Sample):
• Advance Single: £35.00
• Off-Peak Single: £89.50  
• Anytime Single: £142.00
• First Class: £195.00

🔄 ALTERNATIVE WITH CHANGE
Departure: {time} from {from_code}
Change: Birmingham New Street (15 min connection)
Arrival: {(datetime.strptime(time, '%H:%M') + timedelta(hours=5)).strftime('%H:%M')} at {to_code}
Duration: 5h 0m
Price: £28.50

💡 REAL API PROVIDES:
• Live journey times
• Real pricing
• Seat reservations
• Accessibility info
• Disruption updates
        """
        
        return result.strip()

    def _format_live_results(self, data: dict, from_station: str, to_station: str, date: str) -> str:
        """Format real API results"""
        try:
            # The API returns departures under 'departures.all'
            departures_data = data.get('departures', {})
            departures = departures_data.get('all', []) if isinstance(departures_data, dict) else []
            
            if not departures:
                return f"No trains found from {from_station} to {to_station} on {date}"
            
            result = f"🚂 LIVE Train Times: {from_station} → {to_station}\n"
            result += f"Date: {date}\n"
            result += "="*50 + "\n\n"
            
            # Show first 5 results
            departures_to_show = departures[:5]
            
            for i, dep in enumerate(departures_to_show):
                if not isinstance(dep, dict):
                    continue
                    
                scheduled = dep.get('aimed_departure_time', 'N/A')
                expected = dep.get('expected_departure_time', scheduled)
                destination = dep.get('destination_name', to_station)
                operator = dep.get('operator_name', 'Unknown')
                platform = dep.get('platform', 'TBC')
                status = dep.get('status', 'On time')  # Default to on time if no status
                
                result += f"🕐 {scheduled}"
                if expected and expected != scheduled:
                    result += f" (Expected: {expected})"
                result += f" → {destination}\n"
                result += f"   Operator: {operator} | Platform: {platform} | {status}\n\n"
            
            result += "✅ Live data from Transport API\n"
            result += "💡 For booking visit: https://www.trainline.com"
            return result
            
        except Exception as e:
            import traceback
            return f"Error formatting results: {str(e)}\nTraceback: {traceback.format_exc()}"

    def _format_departures(self, data: dict, station_code: str) -> str:
        """Format departure board"""
        try:
            # The API returns departures under 'departures.all'
            departures_data = data.get('departures', {})
            departures = departures_data.get('all', []) if isinstance(departures_data, dict) else []
            
            result = f"🚉 LIVE Departures from {station_code}\n"
            result += f"Updated: {datetime.now().strftime('%H:%M:%S')}\n"
            result += "="*50 + "\n\n"
            
            for dep in departures[:10]:  # Show first 10 departures
                scheduled = dep.get('aimed_departure_time', 'N/A')
                expected = dep.get('expected_departure_time', scheduled)
                destination = dep.get('destination_name', 'Unknown')
                platform = dep.get('platform', 'TBC')
                status = dep.get('status', 'On time')
                
                result += f"🕐 {scheduled}"
                if expected and expected != scheduled:
                    result += f" (Exp: {expected})"
                result += f" → {destination}\n"
                result += f"   Platform: {platform} | {status}\n\n"
            
            result += "✅ Live data from Transport API"
            return result
            
        except Exception as e:
            return f"Error formatting departures: {str(e)}"

    def _format_journey_details(self, data: dict, from_code: str, to_code: str) -> str:
        """Format detailed journey information"""
        try:
            # The API returns departures under 'departures.all'
            departures_data = data.get('departures', {})
            departures = departures_data.get('all', []) if isinstance(departures_data, dict) else []
            
            if not departures:
                return f"No journey details found for {from_code} → {to_code}"
            
            result = f"🚂 Journey Details: {from_code} → {to_code}\n"
            result += "="*50 + "\n\n"
            
            for i, dep in enumerate(departures[:3], 1):  # Show first 3 options
                scheduled_dep = dep.get('aimed_departure_time', 'N/A')
                scheduled_arr = dep.get('aimed_arrival_time', 'N/A')
                operator = dep.get('operator_name', 'Unknown')
                platform = dep.get('platform', 'TBC')
                
                result += f"Option {i}:\n"
                result += f"🕐 Depart: {scheduled_dep} | Arrive: {scheduled_arr}\n"
                result += f"🚂 Operator: {operator} | Platform: {platform}\n"
                
                # Add service timetable link if available
                service_timetable = dep.get('service_timetable', {})
                if service_timetable:
                    result += "📋 Full timetable available\n"
                
                result += "\n"
            
            result += "✅ Live data from Transport API"
            return result
            
        except Exception as e:
            return f"Error formatting journey details: {str(e)}"

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "real-trainline-connector",
                        "version": "2.0.0"
                    }
                }
            }
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [tool["schema"] for tool in self.tools.values()]
                }
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name in self.tools:
                try:
                    result = self.tools[tool_name]["func"](**arguments)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": result
                                }
                            ]
                        }
                    }
                except Exception as e:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32603,
                            "message": f"Internal error: {str(e)}"
                        }
                    }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool not found: {tool_name}"
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

    def run(self):
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = self.handle_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError:
                continue
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()

if __name__ == "__main__":
    server = RealTrainlineMCPServer()
    server.run()