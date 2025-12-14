# 🚂 Trainline MCP Clients

This directory contains MCP clients that connect to your Trainline MCP server to help you query for trains between UK destinations.

## 📁 Files Overview

### MCP Server
- `trainline_mcp_server.py` - The MCP server that provides train search functionality
- `mcp_server.py` - Original demo MCP server with greet/calculate functions

### MCP Clients
- `trainline_client.py` - **Interactive GUI client** with full menu system
- `quick_train_search.py` - **Command-line client** for quick searches
- `uk_routes.py` - **Pre-defined routes** for popular UK destinations

### Test Scripts
- `test_trainline.py` - Test script for the MCP server
- `test_mcp.py` - Test script for the original MCP server

### Configuration
- `.kiro/settings/mcp.json` - MCP server configuration for Kiro IDE

## 🚀 Quick Start

### 1. Strand Agent Web Interface (Recommended - NEW!)
```bash
./venv/bin/python strand_agent_web.py
```
Open: http://localhost:5002

Features:
- **Natural language processing** for complex travel queries
- **Round trip planning** with complete travel coordination
- **Multi-intent detection** (trains + hotels in one request)
- **Real-time chat interface** with intelligent routing
- **All MCP servers integrated** in one interface

### 2. Interactive Client (Direct MCP access)
```bash
./venv/bin/python trainline_client.py
```
Features:
- Full interactive menu
- Date picker (today/tomorrow/custom)
- Station search and information
- Popular routes display
- Error handling and validation

### 2. Command Line Client (Quick searches)
```bash
# Basic search (uses today's date)
./venv/bin/python quick_train_search.py London Manchester

# With specific date
./venv/bin/python quick_train_search.py London Edinburgh 2024-12-25

# With date and time
./venv/bin/python quick_train_search.py Birmingham Liverpool 2024-12-20 09:30

# Show help
./venv/bin/python quick_train_search.py --help

# Show popular routes
./venv/bin/python quick_train_search.py --popular
```

### 3. UK Popular Routes (Pre-defined searches)
```bash
# Interactive menu
./venv/bin/python uk_routes.py

# Direct route selection
./venv/bin/python uk_routes.py 1          # London to Edinburgh
./venv/bin/python uk_routes.py 2 2024-12-25  # London to Manchester on Christmas
```

## 🎯 Available Functions

All clients can access these MCP server functions:

### 🔍 `search_trains`
Search for trains between two stations
- **Parameters**: from_station, to_station, date, time (optional)
- **Example**: London → Manchester on 2024-12-25 at 10:30

### 🚉 `get_station_info`
Get detailed information about a train station
- **Parameters**: station_name
- **Returns**: Facilities, accessibility, operating hours, etc.

### 🗺️ `find_stations`
Find stations in a city or area
- **Parameters**: search_term
- **Returns**: List of stations matching the search

### 🌟 `get_popular_routes`
Get popular train routes by country
- **Parameters**: country (optional, defaults to UK)
- **Returns**: Popular routes with travel tips

## 📋 Popular UK Routes

The clients include these pre-defined popular routes:

1. **London ↔ Edinburgh** (East Coast Main Line)
2. **London ↔ Manchester** (West Coast Main Line)
3. **London ↔ Birmingham** (Frequent services)
4. **Manchester ↔ Liverpool** (Short journey)
5. **London ↔ Bristol** (South West)
6. **Birmingham ↔ <Location A>** (Cross-country)
7. **London ↔ Glasgow** (West Coast to Scotland)
8. **Newcastle ↔ London** (East Coast)
9. **Cardiff ↔ London** (Wales to England)
10. **Edinburgh ↔ Glasgow** (Scottish Central Belt)

## 🛠️ Technical Details

### Requirements
- Python 3.6+
- Virtual environment with `requests` library
- Running Trainline MCP server

### MCP Communication
The clients communicate with the MCP server using JSON-RPC 2.0 protocol:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_trains",
    "arguments": {
      "from_station": "London",
      "to_station": "Manchester",
      "date": "2024-12-25"
    }
  }
}
```

### Error Handling
All clients include comprehensive error handling for:
- Invalid date/time formats
- Server connection issues
- Missing parameters
- JSON parsing errors

## 🔧 Configuration

### MCP Server Configuration
The server is configured in `.kiro/settings/mcp.json`:
```json
{
  "mcpServers": {
    "trainline-connector": {
      "command": "./venv/bin/python",
      "args": ["trainline_mcp_server.py"],
      "disabled": false
    }
  }
}
```

### Customization
You can customize the clients by:
- Adding more UK stations to the lists
- Modifying the popular routes
- Adding new MCP server functions
- Enhancing the UI/UX

## 🚀 Next Steps

### For Production Use
To make this production-ready:
1. **Real API Integration**: Connect to actual Trainline API
2. **Live Data**: Get real-time prices and availability
3. **Booking System**: Add ticket purchasing functionality
4. **Authentication**: Implement user accounts
5. **More Networks**: Add European rail networks
6. **Mobile App**: Create mobile interface

### Development
- Add unit tests
- Implement logging
- Add configuration files
- Create Docker containers
- Add CI/CD pipeline

## 📞 Usage Examples

### Scenario 1: Planning a weekend trip
```bash
# Check trains for weekend travel
./venv/bin/python quick_train_search.py London Edinburgh 2024-12-21
./venv/bin/python quick_train_search.py Edinburgh London 2024-12-23
```

### Scenario 2: Business travel with specific times
```bash
# Morning departure for business meeting
./venv/bin/python quick_train_search.py Manchester London 2024-12-18 08:00
```

### Scenario 3: Exploring station facilities
```bash
# Interactive client for detailed station info
./venv/bin/python trainline_client.py
# Then choose option 2 and enter "London King's Cross"
```

## 🎉 Enjoy Your Journey Planning!

These MCP clients provide a comprehensive interface to plan your UK train journeys. The **Strand Agent Web Interface** is now the recommended way to access all travel services with natural language processing and round trip planning capabilities.

Whether you prefer:
- **Web interface** with intelligent coordination (strand agent)
- **Interactive menus** (trainline client)  
- **Quick command-line searches** (quick search tools)

You have the tools to find the perfect train for your trip!

For real bookings and live prices, remember to visit [trainline.com](https://www.trainline.com) directly.