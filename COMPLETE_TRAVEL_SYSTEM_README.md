# 🧳 Complete Travel Planning System

A comprehensive travel planning system using MCP (Model Context Protocol) servers orchestrated by an intelligent strand agent. This system integrates **UK Rail Network** for trains and **UK Hotel Chains** for hotels, providing end-to-end travel planning capabilities.

## 🎯 System Overview

```
User Request → Strand Agent → MCP Clients → Specialized Servers
                    ↓              ↓              ↓
               Intelligence   Communication   Travel Services
               - NLP parsing  - JSON-RPC     - Train booking (Trainline)
               - Multi-server - Error handling- Hotel search (UK Chains)
               - Coordination - Response      - Greetings & calculations
               - Parameter      formatting    - Live data integration
                 extraction
```

## 🏗️ Architecture Components

### 🤖 Strand Agent (Orchestrator)
- **`mcp_strand_agent.py`** - Main intelligent orchestrator
- **`strand_agent_web.py`** - Web interface for the agent
- **`templates/strand_agent.html`** - Modern web UI

### 🚂 Train Services (Trainline.com)
- **`trainline_mcp_server.py`** - Demo train information server
- **`real_trainline_mcp_server.py`** - Live train API integration
- **`trainline_client.py`** - Interactive train client
- **`quick_train_search.py`** - Command-line train search

### 🏨 Hotel Services (UK Hotel Chains)
- **`multi_hotel_api_server.py`** - Multi-API hotel search server
- **`travel_planner_client.py`** - Complete travel planning client

### 🔧 Supporting Services
- **`mcp_server.py`** - Basic greeting and calculation server
- **Test Scripts** - Comprehensive testing suite

## 🚀 Quick Start

### 1. Start the Complete System

**Option A: Web Interface (Recommended)**
```bash
# Start the strand agent web interface
./venv/bin/python strand_agent_web.py
```
Open: http://localhost:5002

**Option B: Command Line**
```bash
# Interactive strand agent
./venv/bin/python mcp_strand_agent.py
```

**Option C: Travel Planner**
```bash
# Comprehensive travel planning
./venv/bin/python travel_planner_client.py
```

### 2. Test Individual Components
```bash
# Test all servers
./venv/bin/python test_strand_agent.py

# Test travel planner
./venv/bin/python travel_planner_client.py
```

## 🎮 Usage Examples

### Natural Language Travel Planning

The strand agent understands natural language and routes to appropriate services:

```bash
# Hotel searches → Multi-hotel server
"Find hotels in London for December 20-22 for 2 guests"
"Show me hotels near King's Cross station"
"Find hotels in East Croydon for December 15-16 for 1 guest"

# Train searches → Trainline server  
"Find trains from London to Manchester today"
"Show departures from Birmingham"
"Get live train times to Edinburgh"
"I want to catch a train from Leeds at 17:40 for London Kings Cross"

# Round trip travel planning (NEW!)
"Plan a complete round trip from Leeds to East Croydon on 15/12/2025, returning 16/12/2025 for 1 person"
"Plan a complete trip including both train and hotel from Leeds to East Croydon on December 15, returning December 16"
"Complete round trip from Manchester to London on December 20, returning December 22"

# Complex multi-intent requests
"I want to catch a train from Leeds at 17:40 for London Kings Cross and want to stay at Travelodge in East Croydon"
"Find morning trains to Manchester and hotels near the station for tonight"

# Mixed requests (uses multiple servers)
"Hello Alice, find trains to Manchester and hotels there for tonight"
"Calculate the cost of 3 train tickets at £45 each, then find hotels in Edinburgh"
```

### Web Interface Features

The web interface provides:
- **Real-time chat** with intelligent routing
- **Multi-server coordination** in one interface
- **Travel planning suggestions** 
- **Capability discovery** showing all available tools
- **Conversation history** with tool usage tracking
- **Error handling** and graceful fallbacks

## 🌟 Key Features

### 🧠 Intelligent Orchestration
- **Automatic tool discovery** across all MCP servers
- **Natural language processing** for parameter extraction
- **Smart routing** based on keywords and context
- **Multi-step coordination** across different services
- **Error handling** and graceful degradation

### 🚂 Train Services (Trainline Integration)
- **Live departure times** and delays
- **Real-time pricing** and availability
- **Journey planning** with connections
- **Station information** and facilities
- **Popular routes** and travel tips

### 🏨 Hotel Services (UK Hotel Chains Integration)
- **Hotel search** by destination and dates
- **Location-based search** near landmarks/stations
- **Price comparison** across destinations
- **Hotel details** and amenities
- **Popular destinations** and recommendations

### 🔄 Complete Travel Planning
- **Round trip planning** with outbound and return journeys
- **End-to-end trip planning** (trains + hotels + connections)
- **Complex query processing** in single natural language requests
- **Multi-intent detection** for train and hotel combinations
- **Cost comparison** across multiple destinations
- **Integrated booking links** to official sites
- **Travel tips** and recommendations
- **Flexible date handling** and suggestions

## 🎯 Available Tools

### Strand Agent Tools (16 total across 4 servers)

**Greeting & Calculations:**
- `greet` - Personal greetings
- `calculate` - Mathematical calculations  
- `get_time` - Current date/time

**Train Services:**
- `search_trains` - Train ticket search
- `search_live_trains` - Live train times
- `get_station_info` - Station details
- `get_live_departures` - Live departure boards
- `find_station_codes` - Station code lookup
- `get_journey_details` - Detailed journey planning
- `find_stations` - Station search
- `get_popular_routes` - Popular train routes

**Hotel Services:**
- `search_hotels` - Hotel search by destination
- `get_hotel_details` - Detailed hotel information
- `find_hotels_near` - Hotels near landmarks
- `get_popular_destinations` - Travel recommendations
- `compare_hotel_prices` - Price comparison

## 🔧 Configuration

### MCP Server Configuration
All servers are configured in `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "workspace-greeter": {
      "command": "./venv/bin/python",
      "args": ["mcp_server.py"],
      "disabled": false
    },
    "real-trainline": {
      "command": "./venv/bin/python", 
      "args": ["real_trainline_mcp_server.py"],
      "disabled": false
    },
    "multi-hotels": {
      "command": "./venv/bin/python",
      "args": ["multi_hotel_api_server.py"], 
      "disabled": false
    }
  }
}
```

### API Integration Setup

**For Live Train Data:**
1. Register at https://transportapi.com (free tier available)
2. Run: `./venv/bin/python setup_real_api.py`
3. Enter your API credentials

**For Live Hotel Data:**
1. Register at RapidAPI for Hotels.com access
2. Get API access credentials
3. Update `multi_hotel_api_server.py` with your API key

## 🎨 Web Interface

### Features
- **Modern responsive design** with gradient backgrounds
- **Real-time chat interface** with the strand agent
- **Capability sidebar** showing all available tools
- **Suggestion prompts** for common travel requests
- **Conversation history** with tool usage metadata
- **Error handling** with user-friendly messages

### Endpoints
- `/` - Main chat interface
- `/api/capabilities` - Get all available tools
- `/api/process` - Process user requests
- `/api/history` - Get conversation history
- `/api/suggest` - Get suggestion prompts

## 🧪 Testing

### Comprehensive Test Suite
```bash
./venv/bin/python test_strand_agent.py
```

**Test Options:**
1. **Automated tests** - Pre-defined test cases
2. **Capabilities discovery** - Show all available tools
3. **Interactive mode** - Manual testing
4. **All tests** - Complete test suite

### Example Test Cases
```bash
# Greeting tests
"Hello, my name is Alice"
"Greet John"

# Calculation tests  
"Calculate 15 * 7 + 3"
"What is 100 divided by 4?"

# Travel tests
"Find trains from London to Manchester today"
"Search hotels in Paris for December 20-22"
"Show departures from Birmingham"
"Find hotels near King's Cross station"
```

## 🌍 Travel Planning Workflows

### 1. Complete Round Trip Planning (NEW!)
```bash
# Comprehensive round trip with all components
"Plan a complete round trip from Leeds to East Croydon on 15/12/2025, returning 16/12/2025 for 1 person"

# Business round trip with specific requirements
"Plan a complete trip including both train and hotel from Leeds to East Croydon on December 15, returning December 16"

# Using travel planner client
./venv/bin/python travel_planner_client.py
```

### 2. Complex Multi-Intent Queries
```bash
# Train + Hotel in single request
"I want to catch a train from Leeds at 17:40 for London Kings Cross and want to stay at Travelodge in East Croydon"

# Business travel with timing
"Find morning trains to Manchester and hotels near the station for tonight"
```

### 3. Leisure Travel
```bash
"Compare hotel prices in Paris, Rome, and Barcelona for a week in March"
"Find weekend trains to Edinburgh and hotels near the castle"
```

### 4. Last-Minute Booking
```bash
"Find trains to Edinburgh today and hotels for tonight"
"Show me options for East Croydon hotels tonight"
```

## 🔄 Integration Benefits

### For Users
- **Single interface** for complete travel planning
- **Natural language** interaction across all services
- **Intelligent routing** to appropriate tools
- **Unified experience** for trains and hotels
- **Real-time data** when APIs are configured

### For Developers
- **Modular architecture** with independent MCP servers
- **Easy extension** by adding new travel services
- **Centralized intelligence** in the strand agent
- **Reusable components** across different applications
- **Standard MCP protocol** for interoperability

## 🚀 Future Enhancements

### Additional Travel Services
- **Flight booking** integration (Skyscanner, Expedia)
- **Car rental** services (Hertz, Avis)
- **Activity booking** (GetYourGuide, Viator)
- **Restaurant reservations** (OpenTable)
- **Local transport** (Uber, local transit APIs)

### Enhanced Intelligence
- **Machine learning** for better intent recognition
- **Context awareness** across conversations
- **Personalization** based on user preferences
- **Predictive suggestions** for travel planning
- **Multi-language support**

### Advanced Features
- **Workflow automation** for complex trips
- **Budget optimization** across all services
- **Calendar integration** for date suggestions
- **Weather integration** for travel recommendations
- **Real-time notifications** for delays/changes

## 📞 Support & Troubleshooting

### Common Issues

**Strand agent not finding tools:**
- Check MCP server configurations
- Verify servers are running individually
- Review keyword matching in agent code

**API integration issues:**
- Ensure API keys are configured correctly
- Check network connectivity
- Verify API rate limits

**Web interface not loading:**
- Ensure Flask is installed
- Check port availability (5002)
- Verify templates directory exists

### Getting Help
- Check individual server README files
- Review test scripts for examples
- Use interactive mode for debugging
- Check MCP server logs for errors

## 🎉 Success Stories

This system enables:
- **Complete travel planning** in one interface
- **Real-time travel information** when APIs are configured
- **Intelligent coordination** between different travel services
- **Natural language interaction** for non-technical users
- **Extensible architecture** for adding new services

---

🧳 **Your complete travel planning companion - from trains to hotels, all orchestrated intelligently!** ✈️🏨🚂