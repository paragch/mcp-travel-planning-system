#!/usr/bin/env python3
"""
Enhanced Hotel MCP Server - Better sample data with real-looking results
"""
import json
import sys
import requests
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
import random

class EnhancedHotelMCPServer:
    def __init__(self):
        self.tools = {}
        
        # Register tools
        self.register_tool("search_hotels_enhanced", self.search_hotels, {
            "type": "function",
            "function": {
                "name": "search_hotels_enhanced",
                "description": "Search for hotels with enhanced realistic data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "destination": {"type": "string", "description": "City or area to search"},
                        "checkin_date": {"type": "string", "description": "Check-in date (YYYY-MM-DD)"},
                        "checkout_date": {"type": "string", "description": "Check-out date (YYYY-MM-DD)"},
                        "guests": {"type": "integer", "description": "Number of guests", "default": 2}
                    },
                    "required": ["destination", "checkin_date", "checkout_date"]
                }
            }
        })
    
    def register_tool(self, name: str, func, schema: Dict[str, Any]):
        self.tools[name] = {"func": func, "schema": schema}
    
    def get_realistic_hotels(self, destination: str) -> list:
        """Get realistic hotel data for any UK location"""
        
        # Base hotel chains that exist everywhere in UK
        hotel_templates = [
            {
                "chain": "Premier Inn",
                "base_price": 89,
                "rating": 8.7,
                "amenities": ["Free WiFi", "Restaurant", "Parking", "24h Reception"],
                "description": "Modern budget hotel with comfortable rooms"
            },
            {
                "chain": "Travelodge", 
                "base_price": 65,
                "rating": 8.2,
                "amenities": ["Free WiFi", "24h Reception", "Vending Machines"],
                "description": "Budget accommodation with essential amenities"
            },
            {
                "chain": "Holiday Inn Express",
                "base_price": 95,
                "rating": 8.5,
                "amenities": ["Free WiFi", "Gym", "Breakfast included", "Business Center"],
                "description": "Business-friendly hotel with modern facilities"
            },
            {
                "chain": "Ibis",
                "base_price": 78,
                "rating": 8.3,
                "amenities": ["Free WiFi", "Restaurant", "Bar", "24h Reception"],
                "description": "Contemporary hotel with French hospitality"
            },
            {
                "chain": "Best Western",
                "base_price": 110,
                "rating": 8.6,
                "amenities": ["Free WiFi", "Restaurant", "Parking", "Room Service"],
                "description": "Traditional hotel with personal service"
            }
        ]
        
        # Generate location-specific hotels
        hotels = []
        for template in hotel_templates:
            hotel = {
                "name": f"{template['chain']} {destination}",
                "price": template["base_price"] + random.randint(-15, 25),
                "rating": template["rating"] + random.uniform(-0.3, 0.4),
                "amenities": template["amenities"],
                "description": template["description"],
                "distance": round(random.uniform(0.2, 2.5), 1),
                "reviews": random.randint(450, 1200)
            }
            hotels.append(hotel)
        
        # Add some local/independent hotels
        local_hotels = [
            {
                "name": f"The {destination} Hotel",
                "price": random.randint(120, 180),
                "rating": random.uniform(8.4, 9.1),
                "amenities": ["Free WiFi", "Restaurant", "Bar", "Concierge"],
                "description": "Boutique hotel in the heart of the area",
                "distance": round(random.uniform(0.1, 1.0), 1),
                "reviews": random.randint(200, 800)
            },
            {
                "name": f"{destination} Lodge",
                "price": random.randint(85, 130),
                "rating": random.uniform(8.0, 8.7),
                "amenities": ["Free WiFi", "Parking", "Garden", "Pet-friendly"],
                "description": "Comfortable accommodation with local charm",
                "distance": round(random.uniform(0.5, 3.0), 1),
                "reviews": random.randint(150, 600)
            }
        ]
        
        hotels.extend(local_hotels)
        
        # Sort by rating (best first)
        hotels.sort(key=lambda x: x["rating"], reverse=True)
        
        return hotels
    
    def search_hotels(self, destination: str, checkin_date: str, checkout_date: str, guests: int = 2) -> str:
        """Search for hotels with enhanced realistic data"""
        try:
            # Calculate nights
            checkin = datetime.strptime(checkin_date, "%Y-%m-%d")
            checkout = datetime.strptime(checkout_date, "%Y-%m-%d")
            nights = (checkout - checkin).days
            
            if nights <= 0:
                return "❌ Check-out date must be after check-in date"
            
            # Get realistic hotel data
            hotels = self.get_realistic_hotels(destination)
            
            result = f"""🏨 Hotel Search Results - {destination}
📅 {checkin_date} → {checkout_date} ({nights} night{'s' if nights != 1 else ''})
👥 {guests} guest{'s' if guests != 1 else ''}
{'='*60}

⚠️  ENHANCED SAMPLE DATA
These are realistic sample results. For real bookings:
• Use RapidAPI for live hotel data
• Visit booking websites directly
• Call hotels for availability

"""
            
            for i, hotel in enumerate(hotels, 1):
                total_price = hotel["price"] * nights
                
                result += f"""🏨 {hotel['name']}
⭐ {hotel['rating']:.1f}/10 ({hotel['reviews']} reviews)
📍 {hotel['distance']}km from {destination} center
💰 £{hotel['price']}/night | Total: £{total_price}
✅ {' | '.join(hotel['amenities'][:3])}
📝 {hotel['description']}

"""
            
            result += f"""💡 BOOKING OPTIONS:
🌐 Visit hotel websites directly
📞 Call hotels for real availability
🔗 Use booking platforms (Booking.com, Expedia)

🔧 FOR REAL API DATA:
Run: python setup_rapidapi_hotels.py
Get live hotel data from multiple sources!

✅ Sample data based on typical UK hotel availability"""
            
            return result
            
        except Exception as e:
            return f"Error searching hotels: {str(e)}"

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
                        "name": "enhanced-hotel-connector",
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
    server = EnhancedHotelMCPServer()
    server.run()