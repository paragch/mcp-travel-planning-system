# 🧳 MCP Travel Planning System

A comprehensive travel planning system using **Model Context Protocol (MCP)** servers orchestrated by an intelligent strand agent. This system integrates **UK Rail Network** for trains and **UK Hotel Chains** for hotels, providing end-to-end travel planning capabilities with natural language processing.

## 🎯 Key Features

- **🤖 Intelligent Strand Agent** - Natural language processing for complex travel queries
- **🚂 Real Train Data** - Live UK train information via Transport API
- **🏨 Hotel Search** - UK hotel chains with realistic pricing and contact info
- **🔄 Round Trip Planning** - Complete travel coordination in single requests
- **🌐 Web Interface** - Modern chat interface at http://localhost:5002
- **🔧 MCP Architecture** - Modular, extensible server-based design

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone the repository
git clone <your-repo-url>
cd KiroPythonProject

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install requests flask
```

### 2. Start the System
```bash
# Start the web interface (recommended)
./venv/bin/python strand_agent_web.py
```
Open: **http://localhost:5002**

### 3. Try Example Queries
```bash
# Round trip planning
"Plan a complete round trip from Leeds to East Croydon on 15/12/2025, returning 16/12/2025"

# Hotel search
"Find hotels in East Croydon for December 15-16, 2025 for 1 guest"

# Train search
"Find trains from London to Manchester today"

# Complex multi-intent
"I want to catch a train from Leeds at 17:40 for London Kings Cross and stay at Travelodge in East Croydon"
```

## 📁 Project Structure

```
KiroPythonProject/
├── 🤖 Core System
│   ├── mcp_strand_agent.py          # Main intelligent orchestrator
│   ├── strand_agent_web.py          # Web interface
│   └── templates/strand_agent.html  # Modern web UI
├── 🚂 Train Services
│   ├── real_trainline_mcp_server.py # Live Transport API
│   ├── trainline_mcp_server.py      # Demo train server
│   ├── trainline_client.py          # Interactive client
│   └── quick_train_search.py        # Command-line search
├── 🏨 Hotel Services
│   ├── multi_hotel_api_server.py    # Multi-API hotel server
│   ├── demo_hotel_search.py         # Hotel search demo
│   └── travel_planner_client.py     # Complete travel client
├── 🔧 Configuration
│   ├── .kiro/settings/mcp.json      # MCP server config
│   ├── setup_real_apis.py           # API setup
│   └── setup_rapidapi_hotels.py     # Hotel API setup
├── 🧪 Testing
│   ├── test_strand_agent.py         # Comprehensive tests
│   ├── test_multi_hotel_integration.py
│   └── test_web_interface.py
└── 📚 Documentation
    ├── STRAND_AGENT_README.md       # Detailed agent docs
    ├── COMPLETE_TRAVEL_SYSTEM_README.md
    ├── MULTI_API_HOTEL_SUMMARY.md
    └── README_MCP_Clients.md
```

## 🎮 Usage Examples

### Web Interface (Recommended)
1. Start: `./venv/bin/python strand_agent_web.py`
2. Open: http://localhost:5002
3. Chat naturally: *"Plan a round trip from Leeds to East Croydon"*

### Command Line
```bash
# Interactive strand agent
./venv/bin/python mcp_strand_agent.py

# Direct hotel search
./venv/bin/python demo_hotel_search.py

# Train client
./venv/bin/python trainline_client.py
```

## 🔧 API Configuration

### For Live Train Data (Optional)
1. Register at [Transport API](https://transportapi.com) (free tier available)
2. Run: `./venv/bin/python setup_real_apis.py`
3. Enter your API credentials

### For Live Hotel Data (Optional)
1. Register at RapidAPI for Hotels.com access
2. Run: `./venv/bin/python setup_rapidapi_hotels.py`
3. Configure your API key

## 🧠 System Capabilities

### Natural Language Processing
- **Multi-intent detection** - Handles train + hotel requests
- **Parameter extraction** - Dates, locations, guest counts
- **Round trip planning** - Complete travel coordination
- **Flexible date parsing** - "December 15-16", "tomorrow", "next week"

### Travel Services
- **Live train data** - Real UK train times and prices
- **Hotel search** - UK chains with realistic pricing
- **Station information** - Facilities and connections
- **Popular routes** - Pre-defined UK travel routes

### Web Features
- **Real-time chat** with intelligent routing
- **Suggestion prompts** for common requests
- **Conversation history** with tool usage tracking
- **Error handling** and graceful fallbacks

## 🎯 Example Results

### East Croydon Hotels (December 15-16, 2025)
- **Premier Inn East Croydon** - £97/night ⭐ 8.5/10
- **Holiday Inn Express** - £103/night ⭐ 8.3/10  
- **Ibis East Croydon** - £86/night ⭐ 8.1/10
- **Travelodge East Croydon** - £73/night ⭐ 8.0/10

### Live Train Data
- Real LNER, CrossCountry, and regional services
- Live departure times and platform information
- Journey planning with connections
- Delay and disruption information

## 🧪 Testing

```bash
# Run comprehensive tests
./venv/bin/python test_strand_agent.py

# Test hotel integration
./venv/bin/python test_multi_hotel_integration.py

# Test web interface
./venv/bin/python test_web_interface.py
```

## 🔄 Architecture Benefits

### For Users
- **Single interface** for complete travel planning
- **Natural language** interaction
- **Real-time data** when APIs are configured
- **Unified experience** across trains and hotels

### For Developers
- **Modular MCP architecture** with independent servers
- **Easy extension** by adding new travel services
- **Centralized intelligence** in strand agent
- **Standard protocols** for interoperability

## 🚀 Future Enhancements

- **Flight booking** integration (Skyscanner, Expedia)
- **Car rental** services (Hertz, Avis)
- **Activity booking** (GetYourGuide, Viator)
- **Restaurant reservations** (OpenTable)
- **Multi-language support**
- **Mobile app** development

## 📞 Support

### Common Issues
- **No servers connected**: Check MCP configuration in `.kiro/settings/mcp.json`
- **API errors**: Verify API keys in setup scripts
- **Web interface not loading**: Ensure Flask is installed and port 5002 is available

### Getting Help
- Check individual README files for detailed documentation
- Review test scripts for usage examples
- Use interactive mode for debugging: `./venv/bin/python mcp_strand_agent.py`

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🎉 Acknowledgments

- **Transport API** for UK rail data
- **UK Hotel Chains** for accommodation data
- **Model Context Protocol** for the architecture framework
- **Kiro IDE** for development environment

---

🧳 **Your complete travel planning companion - from trains to hotels, all orchestrated intelligently!** ✈️🏨🚂