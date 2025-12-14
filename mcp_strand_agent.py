#!/usr/bin/env python3
"""
MCP Strand Agent - Orchestrates calls across multiple MCP servers
"""
import json
import subprocess
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re

class MCPClient:
    """Client for communicating with individual MCP servers"""
    
    def __init__(self, server_name: str, server_script: str, python_path: str = "./venv/bin/python"):
        self.server_name = server_name
        self.server_script = server_script
        self.python_path = python_path
        self.tools = {}
        self._load_tools()
    
    def _load_tools(self):
        """Load available tools from the MCP server"""
        try:
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            
            result = self._call_server(request)
            if result and "result" in result:
                tools_list = result["result"].get("tools", [])
                for tool in tools_list:
                    if "function" in tool:
                        func_info = tool["function"]
                        self.tools[func_info["name"]] = {
                            "description": func_info.get("description", ""),
                            "parameters": func_info.get("parameters", {}),
                            "server": self.server_name
                        }
        except Exception as e:
            print(f"Warning: Could not load tools from {self.server_name}: {e}")
    
    def _call_server(self, request: dict) -> Optional[dict]:
        """Make a call to the MCP server"""
        try:
            process = subprocess.Popen(
                [self.python_path, self.server_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = process.communicate(input=json.dumps(request).encode())
            
            if process.returncode == 0:
                stdout_str = stdout.decode().strip()
                if stdout_str:
                    try:
                        return json.loads(stdout_str)
                    except json.JSONDecodeError as je:
                        print(f"JSON decode error for {self.server_name}: {je}")
                        print(f"Raw output: {stdout_str[:200]}...")
                        return None
                else:
                    print(f"Empty response from {self.server_name}")
                    return None
            else:
                error_msg = stderr.decode()
                print(f"Server error from {self.server_name}: {error_msg}")
                return None
                
        except Exception as e:
            print(f"Client error for {self.server_name}: {e}")
            return None
    
    def call_tool(self, tool_name: str, arguments: dict) -> Optional[str]:
        """Call a specific tool on this server"""
        if tool_name not in self.tools:
            return None
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        result = self._call_server(request)
        if result and "result" in result:
            content = result["result"].get("content", [])
            if content and len(content) > 0:
                return content[0].get("text", "")
        elif result and "error" in result:
            return f"Error: {result['error'].get('message', 'Unknown error')}"
        
        return None

class MCPStrandAgent:
    """Strand Agent that orchestrates multiple MCP servers"""
    
    def __init__(self):
        self.clients = {}
        self.conversation_history = []
        self.setup_clients()
    
    def setup_clients(self):
        """Initialize all MCP clients"""
        # Define your MCP servers
        servers = {
            "greeter": "mcp_server.py",
            "trainline": "trainline_mcp_server.py", 
            "real_trainline": "real_trainline_mcp_server.py",
            "multi_hotels": "multi_hotel_api_server.py"
        }
        
        for name, script in servers.items():
            try:
                client = MCPClient(name, script)
                if client.tools:  # Only add if tools were loaded successfully
                    self.clients[name] = client
                    print(f"✅ Connected to {name} server ({len(client.tools)} tools)")
                else:
                    print(f"⚠️  {name} server has no tools available")
            except Exception as e:
                print(f"❌ Failed to connect to {name} server: {e}")
    
    def get_all_tools(self) -> Dict[str, Dict]:
        """Get all available tools across all servers"""
        all_tools = {}
        for client_name, client in self.clients.items():
            for tool_name, tool_info in client.tools.items():
                # Prefix tool name with server name to avoid conflicts
                prefixed_name = f"{client_name}.{tool_name}"
                all_tools[prefixed_name] = {
                    **tool_info,
                    "client": client_name,
                    "original_name": tool_name
                }
        return all_tools
    
    def find_relevant_tools(self, user_input: str) -> List[Dict]:
        """Find tools relevant to user input using keyword matching"""
        relevant_tools = []
        all_tools = self.get_all_tools()
        
        # Keywords for different domains
        train_keywords = ["train", "railway", "station", "journey", "travel", "departure", "arrival", "ticket", "rail"]
        hotel_keywords = ["hotel", "accommodation", "stay", "room", "booking", "checkin", "checkout", "lodge", "resort"]
        greeting_keywords = ["hello", "hi", "greet", "welcome", "name"]
        math_keywords = ["calculate", "math", "add", "subtract", "multiply", "divide", "equation"]
        
        user_lower = user_input.lower()
        
        for tool_name, tool_info in all_tools.items():
            relevance_score = 0
            
            # Check if user input matches tool domain
            if any(keyword in user_lower for keyword in train_keywords):
                if "train" in tool_info["description"].lower() or "station" in tool_info["description"].lower():
                    relevance_score += 10
            
            if any(keyword in user_lower for keyword in hotel_keywords):
                if "hotel" in tool_info["description"].lower() or "accommodation" in tool_info["description"].lower():
                    relevance_score += 10
            
            if any(keyword in user_lower for keyword in greeting_keywords):
                if "greet" in tool_info["description"].lower():
                    relevance_score += 10
            
            if any(keyword in user_lower for keyword in math_keywords):
                if "calculate" in tool_info["description"].lower():
                    relevance_score += 10
            
            # Prefer live/real data tools
            if "live" in tool_info["description"].lower() or "real" in tool_info["description"].lower():
                relevance_score += 15  # Higher priority for live data
            
            # Prefer real_trainline over trainline for train searches
            if any(keyword in user_lower for keyword in train_keywords):
                if "real_trainline" in tool_name:
                    relevance_score += 20  # Highest priority for real train data
                elif "trainline" in tool_name and "real_trainline" not in tool_name:
                    relevance_score += 5   # Lower priority for demo train data
            
            # Check description similarity
            description_words = tool_info["description"].lower().split()
            input_words = user_lower.split()
            
            for word in input_words:
                if word in description_words:
                    relevance_score += 2
            
            if relevance_score > 0:
                relevant_tools.append({
                    "name": tool_name,
                    "info": tool_info,
                    "score": relevance_score
                })
        
        # Sort by relevance score
        relevant_tools.sort(key=lambda x: x["score"], reverse=True)
        return relevant_tools[:5]  # Return top 5 most relevant
    
    def extract_parameters(self, user_input: str, tool_info: Dict) -> Dict:
        """Extract parameters from user input based on tool requirements"""
        parameters = {}
        required_params = tool_info.get("parameters", {}).get("required", [])
        properties = tool_info.get("parameters", {}).get("properties", {})
        
        user_lower = user_input.lower()
        
        # Extract common parameters
        for param_name, param_info in properties.items():
            param_type = param_info.get("type", "string")
            param_desc = param_info.get("description", "").lower()
            
            # Extract names for greeting
            if param_name == "name" and "name" in param_desc:
                # Look for patterns like "my name is X" or "I'm X" or "call me X"
                name_patterns = [
                    r"my name is (\w+)",
                    r"i'm (\w+)",
                    r"call me (\w+)",
                    r"greet (\w+)",
                    r"hello (\w+)"
                ]
                for pattern in name_patterns:
                    match = re.search(pattern, user_lower)
                    if match:
                        parameters[param_name] = match.group(1).title()
                        break
            
            # Extract math expressions
            elif param_name == "expression" and "math" in param_desc:
                # Look for mathematical expressions
                math_pattern = r"calculate\s+(.+?)(?:\s|$)"
                match = re.search(math_pattern, user_lower)
                if match:
                    parameters[param_name] = match.group(1).strip()
                else:
                    # Try to find numbers and operators
                    expr_match = re.search(r"[\d\+\-\*\/\(\)\s\.]+", user_input)
                    if expr_match:
                        parameters[param_name] = expr_match.group(0).strip()
            
            # Extract station names (specific for from/to)
            elif "from_station" in param_name:
                # Extract departure station
                from_patterns = [
                    r"from\s+([a-zA-Z\s]+?)\s+to",  # "from Leeds to London"
                    r"from\s+([a-zA-Z\s]+?)\s+for",  # "from Leeds for London"  
                    r"from\s+([a-zA-Z\s]+?)\s+at",  # "from Leeds at 17:40"
                    r"trains?\s+from\s+([a-zA-Z\s]+?)\s+to",  # "trains from Leeds to London"
                    r"trains?\s+from\s+([a-zA-Z\s]+?)\s+for",  # "trains from Leeds for London"
                    r"between\s+([a-zA-Z\s]+?)\s+and",  # "between Leeds and London"
                    r"catch.*?train\s+from\s+([a-zA-Z\s]+?)\s+at",  # "catch a train from Leeds at"
                    r"train\s+from\s+([a-zA-Z\s]+?)\s+at",  # "train from Leeds at"
                ]
                
                for pattern in from_patterns:
                    match = re.search(pattern, user_input, re.IGNORECASE)
                    if match:
                        station = match.group(1).strip()
                        station = re.sub(r'\s+', ' ', station)  # normalize spaces
                        parameters[param_name] = station.title()
                        break
            
            elif "to_station" in param_name:
                # Extract arrival station
                to_patterns = [
                    r"for\s+([a-zA-Z\s\-]+?)(?:\s+and|\s+want|\s*$)",  # "for London Kings Cross and want" - MOST SPECIFIC FIRST
                    r"from\s+[a-zA-Z\s]+?\s+to\s+([a-zA-Z\s]+?)(?:\s+on|\s+at|\s+after|\s*$)",  # "from Leeds to London on"
                    r"between\s+[a-zA-Z\s]+?\s+and\s+([a-zA-Z\s]+?)(?:\s+on|\s+at|\s+after|\s*$)",  # "between Leeds and London Kings Cross"
                    r"to\s+([a-zA-Z\s]+?)(?:\s+on|\s+at|\s+after|\s+and|\s*$)",  # "to London on" - LEAST SPECIFIC LAST
                ]
                
                for pattern in to_patterns:
                    match = re.search(pattern, user_input, re.IGNORECASE)
                    if match:
                        station = match.group(1).strip()
                        station = re.sub(r'\s+', ' ', station)  # normalize spaces
                        parameters[param_name] = station.title()
                        break
            
            # Generic station extraction (fallback)
            elif "station" in param_name or "station" in param_desc:
                # Try patterns to extract station names
                station_patterns = [
                    r"from\s+([a-zA-Z\s]+?)(?:\s+to|\s+station|\s*$)",  # "from East Croydon"
                    r"to\s+([a-zA-Z\s]+?)(?:\s+on|\s+station|\s*$)",    # "to East Croydon"
                    r"trains?\s+from\s+([a-zA-Z\s]+?)(?:\s+to|\s*$)",   # "trains from East Croydon"
                    r"trains?\s+to\s+([a-zA-Z\s]+?)(?:\s+on|\s*$)",     # "trains to East Croydon"
                ]
                
                for pattern in station_patterns:
                    match = re.search(pattern, user_input, re.IGNORECASE)
                    if match:
                        station = match.group(1).strip()
                        station = re.sub(r'\s+', ' ', station)  # normalize spaces
                        parameters[param_name] = station.title()
                        break
                
                # Fallback: check common stations if pattern matching failed
                if param_name not in parameters:
                    uk_stations = [
                        "london", "manchester", "birmingham", "liverpool", "edinburgh",
                        "glasgow", "bristol", "leeds", "sheffield", "newcastle",
                        "cardiff", "nottingham", "oxford", "cambridge", "brighton",
                        "croydon", "east croydon", "south croydon", "west croydon"
                    ]
                    
                    for station in uk_stations:
                        if station in user_lower:
                            parameters[param_name] = station.title()
                            break
            
            # Extract destinations for hotels
            elif param_name == "destination" or "destination" in param_desc:
                # Try multiple patterns to extract destination
                destination_patterns = [
                    r"hotels?\s+in\s+([a-zA-Z\s]+?)(?:\s+for|\s+on|\s*$)",  # "hotels in East Croydon"
                    r"find\s+hotels?\s+in\s+([a-zA-Z\s]+?)(?:\s+for|\s+on|\s*$)",  # "find hotels in East Croydon"
                    r"search\s+hotels?\s+in\s+([a-zA-Z\s]+?)(?:\s+for|\s+on|\s*$)",  # "search hotels in East Croydon"
                    r"accommodation\s+in\s+([a-zA-Z\s]+?)(?:\s+for|\s+on|\s*$)",  # "accommodation in East Croydon"
                    r"stay\s+in\s+([a-zA-Z\s]+?)(?:\s+for|\s+on|\s*$)",  # "stay in East Croydon"
                    r"stay\s+at\s+\w+\s+in\s+([a-zA-Z\s]+?)(?:\.|$)",  # "stay at Travelodge in East Croydon"
                    r"travelodge\s+in\s+([a-zA-Z\s]+?)(?:\.|$)",  # "Travelodge in East Croydon"
                ]
                
                for pattern in destination_patterns:
                    match = re.search(pattern, user_input, re.IGNORECASE)
                    if match:
                        destination = match.group(1).strip()
                        # Clean up the destination (remove extra words)
                        destination = re.sub(r'\s+', ' ', destination)  # normalize spaces
                        parameters[param_name] = destination.title()
                        break
                
                # Fallback: check common destinations if pattern matching failed
                if param_name not in parameters:
                    common_destinations = [
                        "london", "paris", "berlin", "rome", "madrid", "amsterdam",
                        "barcelona", "vienna", "prague", "budapest", "manchester",
                        "birmingham", "edinburgh", "glasgow", "bristol", "leeds",
                        "croydon", "east croydon", "south croydon", "new york", 
                        "tokyo", "sydney", "dubai", "singapore", "brighton",
                        "cambridge", "oxford", "nottingham", "sheffield", "cardiff"
                    ]
                    
                    for dest in common_destinations:
                        if dest in user_lower:
                            parameters[param_name] = dest.title()
                            break
            
            # Extract location for hotels
            elif param_name == "location" and ("hotel" in user_lower or "accommodation" in user_lower or "stay" in user_lower or "travelodge" in user_lower):
                # Look for patterns like "hotels in X" or "accommodation in X"
                location_patterns = [
                    r"hotels?\s+in\s+([a-zA-Z\s]+?)(?:\s+for|\s+on|\s*$)",
                    r"accommodation\s+in\s+([a-zA-Z\s]+?)(?:\s+for|\s+on|\s*$)",
                    r"stay\s+in\s+([a-zA-Z\s]+?)(?:\s+for|\s+on|\s*$)",
                    r"stay\s+at\s+\w+\s+in\s+([a-zA-Z\s]+?)(?:\.|$)",  # "stay at Travelodge in East Croydon"
                    r"travelodge\s+in\s+([a-zA-Z\s]+?)(?:\.|$)",  # "Travelodge in East Croydon"
                    r"book\s+([a-zA-Z\s]+?)(?:\s+hotel|\s+for|\s*$)",
                    r"in\s+([a-zA-Z\s]+?)(?:\s+for|\s+hotel|\s*$)"
                ]
                
                for pattern in location_patterns:
                    match = re.search(pattern, user_input, re.IGNORECASE)
                    if match:
                        location = match.group(1).strip()
                        location = re.sub(r'\s+', ' ', location)  # normalize spaces
                        parameters[param_name] = location.title()
                        break
                
                # Fallback: check common locations if pattern matching failed
                if param_name not in parameters:
                    common_locations = [
                        "london", "paris", "berlin", "rome", "madrid", "amsterdam",
                        "barcelona", "vienna", "prague", "budapest", "manchester",
                        "birmingham", "edinburgh", "glasgow", "bristol", "leeds",
                        "croydon", "east croydon", "south croydon", "new york", 
                        "tokyo", "sydney", "dubai", "singapore", "brighton",
                        "cambridge", "oxford", "nottingham", "sheffield", "cardiff"
                    ]
                    
                    for location in common_locations:
                        if location in user_lower:
                            parameters[param_name] = location.title()
                            break
            
            # Extract hotel names
            elif param_name == "hotel_name" or "hotel" in param_desc:
                # Look for patterns like "hotel X" or "X hotel"
                hotel_patterns = [
                    r"hotel\s+(\w+(?:\s+\w+)*)",
                    r"(\w+(?:\s+\w+)*)\s+hotel",
                    r"the\s+(\w+(?:\s+\w+)*)\s+hotel"
                ]
                for pattern in hotel_patterns:
                    match = re.search(pattern, user_lower)
                    if match:
                        parameters[param_name] = match.group(1).title()
                        break
            
            # Extract number of guests
            elif param_name == "guests" or "guest" in param_desc:
                guest_patterns = [
                    r"(\d+)\s+guests?",
                    r"for\s+(\d+)\s+people",
                    r"(\d+)\s+people"
                ]
                for pattern in guest_patterns:
                    match = re.search(pattern, user_lower)
                    if match:
                        parameters[param_name] = int(match.group(1))
                        break
            
            # Extract number of rooms
            elif param_name == "rooms" or "room" in param_desc:
                room_patterns = [
                    r"(\d+)\s+rooms?",
                    r"(\d+)\s+room"
                ]
                for pattern in room_patterns:
                    match = re.search(pattern, user_lower)
                    if match:
                        parameters[param_name] = int(match.group(1))
                        break
            
            # Extract check-in/check-out dates
            elif "checkin" in param_name or "checkout" in param_name:
                # Look for date patterns including ranges like "December 20-22"
                date_patterns = [
                    r"(\d{4}-\d{2}-\d{2})",  # YYYY-MM-DD
                    r"december\s+(\d{1,2})-(\d{1,2})",  # December 20-22
                    r"(\w+)\s+(\d{1,2})-(\d{1,2})",  # Month DD-DD
                    r"for\s+(\w+\s+\d{1,2}-\d{1,2})",  # for December 20-22
                    r"checkin?\s+(\d{4}-\d{2}-\d{2})",
                    r"checkout?\s+(\d{4}-\d{2}-\d{2})",
                    r"from\s+(\d{4}-\d{2}-\d{2})",
                    r"to\s+(\d{4}-\d{2}-\d{2})"
                ]
                
                # Handle date ranges like "December 20-22" or "December 20 to December 22"
                range_patterns = [
                    r"(\w+)\s+(\d{1,2})-(\d{1,2})",  # December 20-22
                    r"(\w+)\s+(\d{1,2})\s+to\s+(\w+)\s+(\d{1,2})",  # December 20 to December 22
                    r"for\s+(\w+)\s+(\d{1,2})-(\d{1,2})",  # for December 20-22
                    r"for\s+(\w+)\s+(\d{1,2})\s+to\s+(\w+)\s+(\d{1,2})"  # for December 20 to December 22
                ]
                
                for pattern in range_patterns:
                    range_match = re.search(pattern, user_lower)
                    if range_match:
                        groups = range_match.groups()
                        
                        if len(groups) == 3:  # Format: December 20-22
                            month_name = groups[0]
                            start_day = int(groups[1])
                            end_day = int(groups[2])
                        elif len(groups) == 4:  # Format: December 20 to December 22
                            month_name = groups[0]  # Use first month
                            start_day = int(groups[1])
                            end_day = int(groups[3])
                        else:
                            continue
                        
                        # Convert month name to number
                        month_map = {
                            "january": 1, "february": 2, "march": 3, "april": 4,
                            "may": 5, "june": 6, "july": 7, "august": 8,
                            "september": 9, "october": 10, "november": 11, "december": 12
                        }
                        
                        if month_name in month_map:
                            current_year = datetime.now().year
                            month_num = month_map[month_name]
                            
                            if "checkin" in param_name:
                                parameters[param_name] = f"{current_year}-{month_num:02d}-{start_day:02d}"
                            elif "checkout" in param_name:
                                parameters[param_name] = f"{current_year}-{month_num:02d}-{end_day:02d}"
                            break
                
                # Try other patterns if range didn't match
                if param_name not in parameters:
                    for pattern in date_patterns:
                        match = re.search(pattern, user_lower)
                        if match:
                            parameters[param_name] = match.group(1)
                            break
                
                # Handle relative dates
                if param_name not in parameters:
                    if "checkin" in param_name:
                        if "today" in user_lower:
                            parameters[param_name] = datetime.now().strftime("%Y-%m-%d")
                        elif "tomorrow" in user_lower:
                            parameters[param_name] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                        elif "tonight" in user_lower:
                            parameters[param_name] = datetime.now().strftime("%Y-%m-%d")
                        elif "next week" in user_lower:
                            parameters[param_name] = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
                    elif "checkout" in param_name:
                        # Try to infer checkout from checkin if available
                        checkin_key = "checkin" if "checkin" in parameters else "checkin_date" if "checkin_date" in parameters else None
                        
                        if checkin_key and checkin_key in parameters:
                            checkin_date = datetime.strptime(parameters[checkin_key], "%Y-%m-%d")
                            # Default to 1 night stay
                            parameters[param_name] = (checkin_date + timedelta(days=1)).strftime("%Y-%m-%d")
                        elif "tomorrow" in user_lower:
                            # If they mention tomorrow for checkin, checkout is day after
                            parameters[param_name] = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
                        elif "tonight" in user_lower:
                            # If they say "tonight", assume 1 night stay
                            parameters[param_name] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                        elif "2 nights" in user_lower and checkin_key in parameters:
                            # Handle "2 nights" duration
                            checkin = datetime.strptime(parameters[checkin_key], "%Y-%m-%d")
                            parameters[param_name] = (checkin + timedelta(days=2)).strftime("%Y-%m-%d")
                        elif "3 nights" in user_lower and checkin_key in parameters:
                            # Handle "3 nights" duration
                            checkin = datetime.strptime(parameters[checkin_key], "%Y-%m-%d")
                            parameters[param_name] = (checkin + timedelta(days=3)).strftime("%Y-%m-%d")
            
            # Extract dates
            elif param_name == "date" or "date" in param_desc:
                # Look for date patterns
                date_patterns = [
                    r"(\d{4}-\d{2}-\d{2})",  # YYYY-MM-DD
                    r"(\d{1,2}/\d{1,2}/\d{4})",  # DD/MM/YYYY
                    r"today",
                    r"tomorrow"
                ]
                
                for pattern in date_patterns:
                    match = re.search(pattern, user_input)  # Use original case for date matching
                    if match:
                        if match.group(0) == "today":
                            parameters[param_name] = datetime.now().strftime("%Y-%m-%d")
                        elif match.group(0) == "tomorrow":
                            parameters[param_name] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                        else:
                            date_str = match.group(1)
                            # Convert DD/MM/YYYY to YYYY-MM-DD
                            if "/" in date_str:
                                try:
                                    day, month, year = date_str.split("/")
                                    parameters[param_name] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                                except:
                                    parameters[param_name] = date_str
                            else:
                                parameters[param_name] = date_str
                        break
            
            # Extract times
            elif param_name == "time" or "time" in param_desc:
                # Look for time patterns including AM/PM
                time_patterns = [
                    r"(\d{1,2}:\d{2})\s*(am|pm)",  # 3:30 pm
                    r"after\s+(\d{1,2}:\d{2})\s*(am|pm)",  # after 3:30 pm
                    r"(\d{1,2}:\d{2})"  # 15:30
                ]
                
                for pattern in time_patterns:
                    match = re.search(pattern, user_input.lower())
                    if match:
                        time_str = match.group(1)
                        am_pm = match.group(2) if len(match.groups()) > 1 else None
                        
                        # Convert 12-hour to 24-hour format
                        if am_pm:
                            hour, minute = time_str.split(":")
                            hour = int(hour)
                            if am_pm == "pm" and hour != 12:
                                hour += 12
                            elif am_pm == "am" and hour == 12:
                                hour = 0
                            parameters[param_name] = f"{hour:02d}:{minute}"
                        else:
                            parameters[param_name] = time_str
                        break
        
        return parameters
    
    def execute_tool(self, tool_name: str, parameters: Dict) -> str:
        """Execute a tool with given parameters"""
        all_tools = self.get_all_tools()
        
        if tool_name not in all_tools:
            return f"Tool '{tool_name}' not found"
        
        tool_info = all_tools[tool_name]
        client_name = tool_info["client"]
        original_tool_name = tool_info["original_name"]
        
        if client_name not in self.clients:
            return f"Client '{client_name}' not available"
        
        client = self.clients[client_name]
        result = client.call_tool(original_tool_name, parameters)
        
        if result:
            return result
        else:
            return f"Failed to execute {tool_name}"
    
    def detect_round_trip(self, user_input: str) -> bool:
        """Detect if the user input is asking for a round trip"""
        user_lower = user_input.lower()
        round_trip_keywords = ["round trip", "return", "returning", "complete trip", "plan.*trip"]
        return any(keyword in user_lower for keyword in round_trip_keywords)
    
    def detect_multi_intent(self, user_input: str) -> bool:
        """Detect if the user input contains multiple intents (train + hotel)"""
        user_lower = user_input.lower()
        
        # Check for train keywords
        train_keywords = ["train", "railway", "station", "departure", "arrival", "catch", "travel"]
        has_train_intent = any(keyword in user_lower for keyword in train_keywords)
        
        # Check for hotel keywords  
        hotel_keywords = ["hotel", "stay", "accommodation", "travelodge", "premier inn", "room"]
        has_hotel_intent = any(keyword in user_lower for keyword in hotel_keywords)
        
        return has_train_intent and has_hotel_intent
    
    def process_round_trip_request(self, user_input: str) -> str:
        """Process a round trip travel request"""
        print("🎯 Round trip detected: Processing complete travel plan")
        
        results = []
        user_lower = user_input.lower()
        
        # Extract key information for round trip
        outbound_date = None
        return_date = None
        from_city = None
        to_city = None
        
        # Extract dates
        date_patterns = [
            r"on\s+(\d{1,2}/\d{1,2}/\d{4})",  # "on 15/12/2025"
            r"(\d{1,2}/\d{1,2}/\d{4})",      # "15/12/2025"
            r"december\s+(\d{1,2})",          # "December 15"
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, user_input, re.IGNORECASE)
            if matches:
                if len(matches) >= 1:
                    if "/" in matches[0]:
                        outbound_date = matches[0]
                        # Convert to YYYY-MM-DD
                        day, month, year = outbound_date.split("/")
                        outbound_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    else:
                        # Handle "December 15" format
                        day = matches[0]
                        outbound_date = f"2025-12-{day.zfill(2)}"
                
                if len(matches) >= 2:
                    if "/" in matches[1]:
                        return_date = matches[1]
                        # Convert to YYYY-MM-DD
                        day, month, year = return_date.split("/")
                        return_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                break
        
        # If no return date found, try to extract from "returning" patterns
        if not return_date and outbound_date:
            return_patterns = [
                r"returning\s+(\d{1,2}/\d{1,2}/\d{4})",
                r"returning\s+december\s+(\d{1,2})",
            ]
            for pattern in return_patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    if "/" in match.group(1):
                        return_date = match.group(1)
                        day, month, year = return_date.split("/")
                        return_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    else:
                        day = match.group(1)
                        return_date = f"2025-12-{day.zfill(2)}"
                    break
        
        # Extract cities
        city_patterns = [
            r"from\s+([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+?)(?:\s+on|\s+for|\s*$)",
            r"trip\s+from\s+([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+?)(?:\s+on|\s*$)",
        ]
        
        for pattern in city_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                from_city = match.group(1).strip().title()
                to_city = match.group(2).strip().title()
                break
        
        # Process outbound journey (with connection logic for Leeds->East Croydon)
        if from_city and to_city and outbound_date:
            # Handle Leeds to East Croydon via London Kings Cross
            if "leeds" in from_city.lower() and "croydon" in to_city.lower():
                # Get Leeds to London Kings Cross
                outbound_query = f"Find trains from Leeds to London Kings Cross on {outbound_date.replace('-', '/')}"
                train_tools = [tool for tool in self.find_relevant_tools(outbound_query) 
                              if "train" in tool["name"].lower()]
                if train_tools:
                    train_tool = train_tools[0]
                    train_params = {
                        "from_station": "Leeds",
                        "to_station": "London Kings Cross", 
                        "date": outbound_date
                    }
                    train_result = self.execute_tool(train_tool["name"], train_params)
                    results.append(f"🚂 OUTBOUND JOURNEY ({outbound_date}):\nLeeds → London Kings Cross\n{train_result}")
                    
                    # Add connection info
                    results.append("🚇 CONNECTION:\nLondon Kings Cross → East Croydon\n• Take Northern line to London Bridge\n• Change to Southern Rail to East Croydon\n• Journey time: 45-60 minutes")
            
            # Handle return journey (East Croydon to Leeds via London Kings Cross)
            if return_date:
                return_query = f"Find trains from London Kings Cross to Leeds on {return_date.replace('-', '/')}"
                train_tools = [tool for tool in self.find_relevant_tools(return_query) 
                              if "train" in tool["name"].lower()]
                if train_tools:
                    train_tool = train_tools[0]
                    return_params = {
                        "from_station": "London Kings Cross",
                        "to_station": "Leeds",
                        "date": return_date
                    }
                    return_result = self.execute_tool(train_tool["name"], return_params)
                    results.append(f"🚂 RETURN JOURNEY ({return_date}):\nLondon Kings Cross → Leeds\n{return_result}")
        
        # Process hotel request
        if "hotel" in user_lower or "stay" in user_lower or "accommodation" in user_lower:
            hotel_tools = [tool for tool in self.find_relevant_tools(user_input) 
                          if "hotel" in tool["name"].lower()]
            if hotel_tools and outbound_date and return_date:
                hotel_tool = hotel_tools[0]
                hotel_params = {
                    "location": to_city if to_city else "East Croydon",
                    "checkin": outbound_date,
                    "checkout": return_date,
                    "guests": 1  # Default for round trip queries
                }
                hotel_result = self.execute_tool(hotel_tool["name"], hotel_params)
                results.append(f"🏨 ACCOMMODATION:\n{hotel_result}")
        
        if results:
            return "\n\n" + "="*80 + "\n\n".join(results)
        else:
            return "I couldn't extract all the necessary information for your round trip. Please provide: departure city, destination city, outbound date, and return date."

    def process_multi_intent_request(self, user_input: str) -> str:
        """Process a request that contains both train and hotel intents"""
        print("🎯 Multi-intent detected: Processing train and hotel requests")
        
        results = []
        
        # Process train request first
        train_keywords = ["train", "from", "to", "departure", "catch"]
        if any(keyword in user_input.lower() for keyword in train_keywords):
            train_tools = [tool for tool in self.find_relevant_tools(user_input) 
                          if "train" in tool["name"].lower()]
            if train_tools:
                train_tool = train_tools[0]
                train_params = self.extract_parameters(user_input, train_tool["info"])
                required_params = train_tool["info"].get("parameters", {}).get("required", [])
                missing_params = [param for param in required_params if param not in train_params]
                
                if not missing_params:
                    train_result = self.execute_tool(train_tool["name"], train_params)
                    results.append(f"🚂 TRAIN OPTIONS:\n{train_result}")
                else:
                    results.append(f"🚂 TRAIN OPTIONS:\nMissing required information: {', '.join(missing_params)}")
        
        # Process hotel request
        hotel_keywords = ["hotel", "stay", "accommodation", "travelodge"]
        if any(keyword in user_input.lower() for keyword in hotel_keywords):
            hotel_tools = [tool for tool in self.find_relevant_tools(user_input) 
                          if "hotel" in tool["name"].lower()]
            if hotel_tools:
                hotel_tool = hotel_tools[0]
                hotel_params = self.extract_parameters(user_input, hotel_tool["info"])
                required_params = hotel_tool["info"].get("parameters", {}).get("required", [])
                missing_params = [param for param in required_params if param not in hotel_params]
                
                if not missing_params:
                    hotel_result = self.execute_tool(hotel_tool["name"], hotel_params)
                    results.append(f"🏨 HOTEL OPTIONS:\n{hotel_result}")
                else:
                    results.append(f"🏨 HOTEL OPTIONS:\nMissing required information: {', '.join(missing_params)}")
        
        if results:
            return "\n\n" + "="*60 + "\n\n".join(results)
        else:
            return "I found multiple intents in your request but couldn't extract all required parameters. Please try asking for trains and hotels separately."

    def process_request(self, user_input: str) -> str:
        """Process a user request and orchestrate MCP calls"""
        print(f"\n🤖 Processing: '{user_input}'")
        
        # Add to conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "type": "user"
        })
        
        # Check for round trip queries first (more specific)
        if self.detect_round_trip(user_input):
            result = self.process_round_trip_request(user_input)
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "response": result,
                "type": "agent",
                "round_trip": True
            })
            return result
        
        # Check for multi-intent queries
        elif self.detect_multi_intent(user_input):
            result = self.process_multi_intent_request(user_input)
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "response": result,
                "type": "agent",
                "multi_intent": True
            })
            return result
        
        # Find relevant tools
        relevant_tools = self.find_relevant_tools(user_input)
        
        if not relevant_tools:
            response = "I couldn't find any relevant tools for your request. Available capabilities include greeting, calculations, and train information."
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "response": response,
                "type": "agent"
            })
            return response
        
        # Try to execute the most relevant tool
        best_tool = relevant_tools[0]
        tool_name = best_tool["name"]
        tool_info = best_tool["info"]
        
        print(f"🎯 Selected tool: {tool_name}")
        
        # Extract parameters
        parameters = self.extract_parameters(user_input, tool_info)
        
        # Check for missing required parameters
        required_params = tool_info.get("parameters", {}).get("required", [])
        missing_params = [param for param in required_params if param not in parameters]
        
        if missing_params:
            response = f"I need more information. Please provide: {', '.join(missing_params)}"
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "response": response,
                "type": "agent",
                "missing_params": missing_params
            })
            return response
        
        print(f"📋 Parameters: {parameters}")
        
        # Execute the tool
        result = self.execute_tool(tool_name, parameters)
        
        # Add result to conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "response": result,
            "type": "agent",
            "tool_used": tool_name,
            "parameters": parameters
        })
        
        return result
    
    def get_capabilities(self) -> str:
        """Get a summary of all available capabilities"""
        all_tools = self.get_all_tools()
        
        capabilities = "🤖 MCP Strand Agent Capabilities:\n"
        capabilities += "=" * 40 + "\n\n"
        
        # Group by server
        by_server = {}
        for tool_name, tool_info in all_tools.items():
            server = tool_info["client"]
            if server not in by_server:
                by_server[server] = []
            by_server[server].append({
                "name": tool_info["original_name"],
                "description": tool_info["description"]
            })
        
        for server, tools in by_server.items():
            capabilities += f"📡 {server.upper()} Server:\n"
            for tool in tools:
                capabilities += f"  • {tool['name']}: {tool['description']}\n"
            capabilities += "\n"
        
        capabilities += "💡 Usage Examples:\n"
        capabilities += "  • 'Hello, my name is Alice'\n"
        capabilities += "  • 'Calculate 15 * 7 + 3'\n"
        capabilities += "  • 'Find trains from London to Manchester today'\n"
        capabilities += "  • 'Search hotels in Paris for December 20-22'\n"
        capabilities += "  • 'Show departures from Birmingham'\n"
        capabilities += "  • 'Find hotels near King's Cross station'\n"
        
        return capabilities
    
    def interactive_mode(self):
        """Run the agent in interactive mode"""
        print("🚂 MCP Strand Agent - Interactive Mode")
        print("=" * 50)
        print("Type 'help' for capabilities, 'quit' to exit")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() in ['help', 'capabilities']:
                    print(self.get_capabilities())
                elif user_input:
                    response = self.process_request(user_input)
                    print(f"\nAgent: {response}\n")
                    print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function to run the strand agent"""
    agent = MCPStrandAgent()
    
    if not agent.clients:
        print("❌ No MCP servers available. Please check your server configurations.")
        return
    
    print(f"✅ Strand Agent initialized with {len(agent.clients)} servers")
    
    # Show capabilities
    print(agent.get_capabilities())
    
    # Start interactive mode
    agent.interactive_mode()

if __name__ == "__main__":
    main()