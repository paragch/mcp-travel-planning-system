# 🤖 MCP Strand Agent System

The MCP Strand Agent is an intelligent orchestrator that coordinates calls across multiple MCP servers, providing a unified interface for complex multi-server operations.

## 🎯 What is a Strand Agent?

A **Strand Agent** is an AI orchestrator that:
- **Discovers** available tools across multiple MCP servers
- **Analyzes** user requests to find relevant capabilities  
- **Extracts** parameters from natural language input
- **Routes** requests to the appropriate MCP servers
- **Coordinates** multi-step operations across servers
- **Provides** unified responses from distributed services

## 🏗️ Architecture

```
User Input → Strand Agent → MCP Client → Multiple MCP Servers
                ↓              ↓              ↓
            Intelligence   Communication   Specialized Tools
            - NLP parsing  - JSON-RPC     - Greetings
            - Tool routing - Error handling- Calculations  
            - Parameter    - Response      - Train data
              extraction     formatting    - Station info
```

## 📁 Files Overview

### Core Components
- **`mcp_strand_agent.py`** - Main strand agent with orchestration logic
- **`strand_agent_web.py`** - Flask web interface for the agent
- **`templates/strand_agent.html`** - Web UI template
- **`test_strand_agent.py`** - Comprehensive test suite

### MCP Servers (Orchestrated by Agent)
- **`mcp_server.py`** - Basic greeting and calculation server
- **`trainline_mcp_server.py`** - Demo train information server  
- **`real_trainline_mcp_server.py`** - Live train API integration (Transport API)
- **`multi_hotel_api_server.py`** - Multi-API hotel search server (UK hotel chains)

## 🚀 Quick Start

### 1. Start the Strand Agent (Command Line)
```bash
./venv/bin/python mcp_strand_agent.py
```

### 2. Start the Web Interface
```bash
./venv/bin/python strand_agent_web.py
```
Then open: http://localhost:5002

### 3. Run Tests
```bash
./venv/bin/python test_strand_agent.py
```

## 🎮 Usage Examples

### Natural Language Requests
The agent understands natural language and routes to appropriate servers:

```bash
# Greeting requests → Greeter server
"Hello, my name is Alice"
"Greet John"

# Math requests → Calculator server  
"Calculate 15 * 7 + 3"
"What is 100 divided by 4?"

# Train requests → Trainline server
"Find trains from London to Manchester today"
"Show departures from Birmingham"
"Get station info for King's Cross"

# Hotel requests → Hotel server
"Find hotels in <Location B> for December 15-16 for 1 guest"
"Show me hotels near King's Cross station"

# Multi-intent requests (Train + Hotel)
"I want to catch a train from <Location A> at 17:40 for London Kings Cross and stay at Travelodge in <Location B>"

# Round trip requests (Complete travel planning)
"Plan a complete round trip from <Location A> to <Location B> on 15/12/2025, returning 16/12/2025 for 1 person"
```

### Web Interface Features
- **Real-time chat** with the strand agent
- **Capability discovery** showing all available tools
- **Suggestion prompts** for common requests
- **Conversation history** with tool usage tracking
- **Multi-server coordination** in a single interface

## 🧠 Intelligence Features

### 1. Automatic Tool Discovery
```python
# Agent automatically discovers tools from all connected servers
all_tools = agent.get_all_tools()
# Returns: {
#   "greeter.greet": {...},
#   "trainline.search_trains": {...},
#   "real_trainline.get_live_departures": {...},
#   "multi_hotels.search_hotels_multi": {...}
# }
```

### 2. Advanced Natural Language Processing
```python
# Extracts complex parameters from natural language
user_input = "I want to catch a train from <Location A> at 17:40 for London Kings Cross"
parameters = agent.extract_parameters(user_input, tool_info)
# Returns: {
#   "from_station": "<Location A>", 
#   "to_station": "London Kings Cross",
#   "time": "17:40"
# }
```

### 3. Multi-Intent Detection
```python
# Detects when users ask for multiple services in one request
user_input = "Find trains from <Location A> to London and hotels in <Location B>"
is_multi_intent = agent.detect_multi_intent(user_input)  # Returns: True
```

### 4. Round Trip Planning
```python
# Handles complete travel planning with outbound/return journeys
user_input = "Plan a round trip from <Location A> to <Location B> on 15/12/2025, returning 16/12/2025"
is_round_trip = agent.detect_round_trip(user_input)  # Returns: True
```

### 5. Intelligent Routing & Prioritization
```python
# Finds most relevant tools and prioritizes live data
relevant_tools = agent.find_relevant_tools("Find trains to Manchester")
# Automatically prefers "real_trainline" over "trainline" for live data
```

### 6. Multi-Server Coordination
The agent can coordinate complex operations across servers:
```python
# Example: Complete travel planning across multiple servers
"Plan a trip from <Location A> to <Location B> with trains and hotels"
# → Routes to train server for <Location A>→London, adds connection info, finds hotels
```

## 🔧 Configuration

### Adding New MCP Servers
Edit `mcp_strand_agent.py`:
```python
def setup_clients(self):
    servers = {
        "greeter": "mcp_server.py",
        "trainline": "trainline_mcp_server.py",
        "real_trainline": "real_trainline_mcp_server.py",
        "your_new_server": "your_server.py"  # Add here
    }
```

### Customizing Intelligence
The agent's intelligence can be enhanced by modifying:

**Keyword Matching:**
```python
# In find_relevant_tools()
train_keywords = ["train", "railway", "station", "journey", "travel"]
your_keywords = ["weather", "forecast", "temperature"]  # Add domain keywords
```

**Parameter Extraction:**
```python
# In extract_parameters()
# Add custom parameter extraction logic for your domain
```

## 🌟 Advanced Features

### 1. Conversation History
```python
# Agent maintains conversation context
agent.conversation_history  # List of all interactions
```

### 2. Error Handling
- Graceful fallbacks when servers are unavailable
- Parameter validation and user prompting
- Network error recovery

### 3. Tool Metadata
```python
# Rich tool information for intelligent routing
{
    "name": "search_trains",
    "description": "Search for trains between stations",
    "parameters": {...},
    "server": "trainline",
    "relevance_keywords": ["train", "travel", "journey"]
}
```

### 4. Multi-Step Operations
The agent can chain operations:
1. Extract user intent
2. Route to appropriate server
3. Handle missing parameters
4. Execute tool
5. Format response
6. Update conversation context

## 🎯 Use Cases

### 1. Complete Travel Planning
```bash
"Plan a complete round trip from <Location A> to <Location B> on 15/12/2025, 
returning 16/12/2025 for 1 person. I need trains to London Kings Cross 
and hotels in <Location B>."
```
→ Provides outbound trains, connection info, return trains, and hotels in one response

### 2. Multi-Intent Travel Queries
```bash
"I want to catch a train from <Location A> at 17:40 for London Kings Cross 
and want to stay at Travelodge in <Location B>. Show me options."
```
→ Coordinates train search and hotel search simultaneously

### 3. Live Travel Information
```bash
"Find trains from London to Manchester on 15/12/2025 at 17:40"
```
→ Routes to live Transport API, gets real LNER trains with platforms and times

### 4. Hotel Search & Comparison
```bash
"Find hotels in <Location B> for December 15-16 for 1 guest"
```
→ Searches UK hotel chains, provides pricing and contact information

### 5. Personal Assistant
```bash
"Hello, I'm John. Calculate how much I'll spend on 3 train tickets 
at £45.50 each, then greet me with the total."
```
→ Coordinates greeting, calculation, and response formatting

### 6. Information Hub
```bash
"What stations are available in Birmingham and what are the 
current departures?"
```
→ Finds stations, gets live departures, formats comprehensive response

## 🔄 API Endpoints (Web Interface)

### `/api/capabilities`
Get all available tools and servers
```json
{
  "success": true,
  "servers": {...},
  "total_tools": 8,
  "total_servers": 3
}
```

### `/api/process` (POST)
Process user request through strand agent
```json
{
  "message": "Hello, my name is Alice"
}
```

### `/api/history`
Get conversation history
```json
{
  "success": true,
  "history": [...]
}
```

### `/api/suggest`
Get suggestion prompts
```json
{
  "success": true,
  "suggestions": [...]
}
```

## 🧪 Testing

### Automated Tests
```bash
./venv/bin/python test_strand_agent.py
# Choose option 1 for automated tests
```

### Interactive Testing
```bash
./venv/bin/python test_strand_agent.py  
# Choose option 3 for interactive mode
```

### Capability Discovery
```bash
./venv/bin/python test_strand_agent.py
# Choose option 2 to see all available tools
```

## 🚀 Extending the Agent

### 1. Add New Domains
Create new MCP servers for different domains:
- Weather services
- Calendar management  
- Email operations
- File management
- Database queries

### 2. Enhance Intelligence
- Add machine learning for better intent recognition
- Implement context awareness across conversations
- Add multi-language support
- Implement learning from user feedback

### 3. Advanced Orchestration
- Implement workflow chains
- Add conditional logic
- Support parallel operations
- Add transaction management

## 🎉 Benefits

### For Users
- **Single Interface** for multiple services
- **Natural Language** interaction
- **Intelligent Routing** to right tools
- **Unified Experience** across different domains

### For Developers  
- **Modular Architecture** with independent MCP servers
- **Easy Extension** by adding new servers
- **Centralized Intelligence** for routing and coordination
- **Reusable Components** across different applications

## 📞 Support & Troubleshooting

### Common Issues

**No servers connected:**
```bash
# Check if MCP servers are working individually
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | ./venv/bin/python mcp_server.py
```

**Agent not understanding requests:**
- Check keyword matching in `find_relevant_tools()`
- Verify parameter extraction logic
- Add more training examples

**Web interface not loading:**
- Ensure Flask is installed: `./venv/bin/pip install flask`
- Check port 5002 is available
- Verify templates directory exists

---

🤖 **The MCP Strand Agent brings intelligence and coordination to your MCP ecosystem!** 🎯