#!/usr/bin/env python3
"""
Free Hotel MCP Server - Uses free APIs for real hotel data
"""
import json
import sys
import requests
from datetime import datetime
from typing import Any, Dict, Optional
import urllib.parse

class FreeHotelMCPServer:
    def __init__(self):
        self.tools = {}
        
        # Using free APIs that don't require authentication
        self.nominatim_base = "https://nominatim.openstreetmap.org"
        self.overpass_base = "https://overpass-api.de/api/interpreter"
        
        # Register tools
        self.register_tool("search_hotels_free", self.search_hotels, {
            "type": "function",
            "function": {
                "name": "search_hotels_free",
                "description": "Search for hotels using free OpenStreetMap data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "Location to search (e.g., 'East Croydon', 'London')"},
                        "checkin": {"type": "string", "description": "Check-in date (YYYY-MM-DD)"},
                        "checkout": {"type": "string", "description": "Check-out date (YYYY-MM-DD)"},
                        "radius": {"type": "integer", "description": "Search radius in meters", "default": 5000}
                    },
                    "required": ["location", "checkin", "checkout"]
                }
            }
        })
    
    def register_tool(self, name: str, func, schema: Dict[str, Any]):
        self.tools[name] = {"func": func, "schema": schema}
    
    def get_coordinates(self, location: str) -> tuple:
        """Get coordinates for a location using Nominatim"""
        try:
            url = f"{self.nominatim_base}/search"
            params = {
                "q": location,
                "format": "json",
                "limit": 1,
                "countrycodes": "gb"  # UK only
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return float(data[0]["lat"]), float(data[0]["lon"])
        except Exception as e:
            print(f"Geocoding error: {e}")
        
        return None, None
    
    def search_hotels_osm(self, lat: float, lon: float, radius: int = 5000) -> list:
        """Search for hotels using OpenStreetMap Overpass API"""
        try:
            # Overpass query to find hotels
            query = f"""
            [out:json][timeout:25];
            (
              node["tourism"="hotel"](around:{radius},{lat},{lon});
              way["tourism"="hotel"](around:{radius},{lat},{lon});
              relation["tourism"="hotel"](around:{radius},{lat},{lon});
            );
            out center meta;
            """
            
            response = requests.post(
                self.overpass_base,
                data=query,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("elements", [])
        except Exception as e:
            print(f"OSM search error: {e}")
        
        return []
    
    def search_hotels(self, location: str, checkin: str, checkout: str, radius: int = 5000) -> str:
        """Search for hotels using free APIs"""
        try:
            # Get coordinates for the location
            lat, lon = self.get_coordinates(location)
            
            if not lat or not lon:
                return f"""🏨 Hotel Search - {location}
❌ Could not find coordinates for {location}

💡 Try these alternatives:
• Use full area names (e.g., "East Croydon, London")
• Check spelling
• Use nearby major cities

🔍 Supported locations: UK cities and areas
"""
            
            # Search for hotels using OpenStreetMap
            hotels = self.search_hotels_osm(lat, lon, radius)
            
            if not hotels:
                return f"""🏨 Hotel Search - {location}
📍 Location found: {lat:.4f}, {lon:.4f}
❌ No hotels found in OpenStreetMap data within {radius}m

💡 This uses free OpenStreetMap data which may be incomplete.
For comprehensive results, consider:
• Hotels.com API (via RapidAPI)
• Expedia API

🔍 Try expanding search radius or nearby areas.
"""
            
            # Format results
            result = f"""🏨 Real Hotel Data - {location}
📍 Found {len(hotels)} hotels from OpenStreetMap
📅 {checkin} → {checkout}
{'='*50}

"""
            
            for i, hotel in enumerate(hotels[:10], 1):  # Show first 10
                tags = hotel.get("tags", {})
                name = tags.get("name", f"Hotel {i}")
                
                # Get coordinates
                if hotel["type"] == "node":
                    h_lat, h_lon = hotel["lat"], hotel["lon"]
                else:
                    center = hotel.get("center", {})
                    h_lat, h_lon = center.get("lat", lat), center.get("lon", lon)
                
                # Calculate distance
                distance = self.calculate_distance(lat, lon, h_lat, h_lon)
                
                # Get additional info
                phone = tags.get("phone", "Not available")
                website = tags.get("website", "Not available")
                stars = tags.get("stars", "Not rated")
                
                result += f"""🏨 {name}
📍 {distance:.1f}km from search center
⭐ Rating: {stars}
📞 Phone: {phone}
🌐 Website: {website}

"""
            
            result += """✅ Data from OpenStreetMap (free)
💡 For booking and prices, visit hotel websites directly
🔗 More comprehensive data available with paid APIs"""
            
            return result
            
        except Exception as e:
            return f"Error searching hotels: {str(e)}"
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers"""
        import math
        
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c

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
                        "name": "free-hotel-connector",
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
    server = FreeHotelMCPServer()
    server.run()