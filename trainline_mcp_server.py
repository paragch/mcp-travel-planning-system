#!/usr/bin/env python3
"""
Trainline MCP Server - Connect to Trainline.com for train travel information
"""
import json
import sys
import requests
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
import urllib.parse

class TrainlineMCPServer:
    def __init__(self):
        self.tools = {}
        self.base_url = "https://www.trainline.com"
        
        # Register all available tools
        self.register_tool("search_trains", self.search_trains, {
            "type": "function",
            "function": {
                "name": "search_trains",
                "description": "Search for train tickets between two stations on a specific date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from_station": {
                            "type": "string",
                            "description": "Departure station (e.g., 'London', 'Paris', 'Manchester')"
                        },
                        "to_station": {
                            "type": "string",
                            "description": "Arrival station (e.g., 'Edinburgh', 'Brussels', 'Liverpool')"
                        },
                        "date": {
                            "type": "string",
                            "description": "Travel date in YYYY-MM-DD format (e.g., '2024-12-20')"
                        },
                        "time": {
                            "type": "string",
                            "description": "Preferred departure time in HH:MM format (optional, e.g., '09:30')"
                        }
                    },
                    "required": ["from_station", "to_station", "date"]
                }
            }
        })
        
        self.register_tool("get_station_info", self.get_station_info, {
            "type": "function",
            "function": {
                "name": "get_station_info",
                "description": "Get information about a specific train station.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "station_name": {
                            "type": "string",
                            "description": "Name of the station to get information about"
                        }
                    },
                    "required": ["station_name"]
                }
            }
        })
        
        self.register_tool("find_stations", self.find_stations, {
            "type": "function",
            "function": {
                "name": "find_stations",
                "description": "Find stations matching a search term or in a specific city/area.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_term": {
                            "type": "string",
                            "description": "City name or station name to search for"
                        }
                    },
                    "required": ["search_term"]
                }
            }
        })
        
        self.register_tool("get_popular_routes", self.get_popular_routes, {
            "type": "function",
            "function": {
                "name": "get_popular_routes",
                "description": "Get popular train routes and destinations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "country": {
                            "type": "string",
                            "description": "Country code (e.g., 'UK', 'FR', 'DE') - optional"
                        }
                    },
                    "required": []
                }
            }
        })

    def register_tool(self, name: str, func, schema: Dict[str, Any]):
        self.tools[name] = {"func": func, "schema": schema}

    def search_trains(self, from_station: str, to_station: str, date: str, time: Optional[str] = None) -> str:
        """Search for train tickets between two stations."""
        try:
            # Format the search URL (this is a simplified approach)
            # In a real implementation, you'd use Trainline's API or web scraping
            search_url = f"{self.base_url}/search"
            
            # Simulate a search result (in reality, you'd make API calls or scrape)
            result = f"""
🚂 Train Search Results
======================
Route: {from_station} → {to_station}
Date: {date}
{f'Preferred time: {time}' if time else ''}

📍 To get real-time results, visit:
{self.base_url}/search/{urllib.parse.quote(from_station)}/{urllib.parse.quote(to_station)}/{date}

💡 Popular routes from {from_station}:
• {from_station} to London (frequent services)
• {from_station} to Manchester (direct routes available)
• {from_station} to Edinburgh (scenic route)

⚠️  Note: This is a demo MCP server. For actual bookings and real-time prices, 
please visit trainline.com directly or use their official API.

🔗 Direct link: https://www.trainline.com
            """
            
            return result.strip()
            
        except Exception as e:
            return f"Error searching for trains: {str(e)}"

    def get_station_info(self, station_name: str) -> str:
        """Get information about a specific train station."""
        try:
            # Simulate station information
            station_info = f"""
🚉 Station Information: {station_name}
=====================================

📍 Location: {station_name}
🚇 Station Type: Major Railway Station
🅿️  Parking: Available (charges apply)
♿ Accessibility: Wheelchair accessible
🏪 Facilities: Shops, restaurants, waiting areas
📱 WiFi: Free WiFi available

🚂 Typical Services:
• High-speed trains
• Regional services  
• International connections (if applicable)

⏰ Operating Hours: 
• Ticket office: 06:00 - 22:00
• Station access: 24 hours

💡 Tip: Arrive 15-30 minutes before departure for domestic trains,
45-60 minutes for international services.

🔗 For real-time departures and detailed info:
https://www.trainline.com/stations/{urllib.parse.quote(station_name.lower())}
            """
            
            return station_info.strip()
            
        except Exception as e:
            return f"Error getting station info: {str(e)}"

    def find_stations(self, search_term: str) -> str:
        """Find stations matching a search term."""
        try:
            # Simulate station search results
            stations = f"""
🔍 Station Search Results for: "{search_term}"
===========================================

Found stations matching "{search_term}":

🚉 Major Stations:
• {search_term} Central Station
• {search_term} Piccadilly (if applicable)
• {search_term} Victoria (if applicable)
• {search_term} King's Cross (if in London area)

🚇 Regional Stations:
• {search_term} North
• {search_term} South  
• {search_term} East
• {search_term} West

💡 Popular destinations from {search_term}:
• London (multiple daily services)
• Manchester (direct routes)
• Birmingham (frequent connections)
• Edinburgh (scenic routes)

🔗 Search all stations: 
https://www.trainline.com/stations?search={urllib.parse.quote(search_term)}
            """
            
            return stations.strip()
            
        except Exception as e:
            return f"Error finding stations: {str(e)}"

    def get_popular_routes(self, country: Optional[str] = None) -> str:
        """Get popular train routes."""
        try:
            country_filter = f" in {country}" if country else ""
            
            routes = f"""
🌟 Popular Train Routes{country_filter}
================================

🇬🇧 UK Popular Routes:
• London ↔ Edinburgh (East Coast Main Line)
• London ↔ Manchester (West Coast Main Line)  
• London ↔ Birmingham (frequent services)
• London ↔ Liverpool (direct routes)
• Manchester ↔ Liverpool (short journey)

🇫🇷 France Popular Routes:
• Paris ↔ Lyon (TGV high-speed)
• Paris ↔ Marseille (TGV Mediterranean)
• Paris ↔ Bordeaux (TGV Atlantic)

🇩🇪 Germany Popular Routes:
• Berlin ↔ Munich (ICE high-speed)
• Hamburg ↔ Frankfurt (ICE services)
• Cologne ↔ Berlin (direct ICE)

🌍 International Routes:
• London ↔ Paris (Eurostar via Channel Tunnel)
• London ↔ Brussels (Eurostar)
• Paris ↔ Amsterdam (Thalys)
• Paris ↔ Frankfurt (TGV/ICE)

💰 Money-saving tips:
• Book in advance for better prices
• Consider off-peak travel times
• Look for split ticketing options
• Check for railcard discounts

🔗 Explore all routes: https://www.trainline.com
            """
            
            return routes.strip()
            
        except Exception as e:
            return f"Error getting popular routes: {str(e)}"

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
                        "name": "trainline-connector",
                        "version": "1.0.0"
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
    server = TrainlineMCPServer()
    server.run()