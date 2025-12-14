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
│   ├── multi_hotel_api_server.py    # Main hotel server (UK chains + OpenStreetMap)
│   ├── demo_hotel_search.py         # Hotel search demo and testing
│   ├── enhanced_hotel_mcp_server.py # Enhanced hotel features
│   └── travel_planner_client.py     # Complete travel client
├── 🔧 Configuration
│   ├── .kiro/settings/mcp.json      # MCP server config
│   ├── setup_real_apis.py           # Transport API setup
│   └── setup_rapidapi_hotels.py     # Optional hotel API enhancement
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

## 🔧 API Configuration & Credentials

The system works with **demo data** out of the box, but you can configure **real APIs** for live data:

### 🚂 Live Train Data - Transport API (Recommended)

**Free Tier:** 1,000 requests/day

#### Setup Steps:
1. **Register:** Visit [transportapi.com](https://transportapi.com)
2. **Sign Up:** Click "Sign Up" (completely free)
3. **Verify Email:** Check your inbox and verify
4. **Get Credentials:** Go to "My Account" → "API Keys"
5. **Copy:** Your App ID and API Key

#### Required Credentials:
- **App ID:** Format like `d948d452` 
- **API Key:** Format like `55xxxxxxxxxxxxxxxxxxxxxxxxxxxxb2`

#### Configuration:
```bash
# Run the setup script
./venv/bin/python setup_real_apis.py

# Enter your credentials when prompted:
# App ID: d948d452
# API Key: 55xxxxxxxxxxxxxxxxxxxxxxxxxxxxb2
```

#### What You Get:
- ✅ **Real train times** and delays
- ✅ **Live departure boards** 
- ✅ **Actual pricing** information
- ✅ **Platform numbers** and operators
- ✅ **Journey planning** with connections

---

### 🏨 Hotel Data - Multi-Hotel API Server

**Built-in System:** No external API required

#### What's Included:
The `multi_hotel_api_server.py` provides comprehensive hotel data using:

1. **UK Hotel Chains Database** (Primary)
   - ✅ **Real hotel brands** (Premier Inn, Holiday Inn Express, Ibis, Travelodge)
   - ✅ **Realistic pricing** (£50-£150/night based on location)
   - ✅ **Real contact information** (phone numbers, websites)
   - ✅ **Accurate locations** for all UK cities
   - ✅ **Hotel amenities** and ratings

2. **OpenStreetMap Integration** (Backup)
   - ✅ **Real hotel locations** and coordinates
   - ✅ **Geographic accuracy** for mapping
   - ✅ **Location-based search** capabilities

#### No Setup Required:
```bash
# Hotel server works immediately
./venv/bin/python multi_hotel_api_server.py

# Test hotel search
./venv/bin/python demo_hotel_search.py
```

#### What You Get:
- ✅ **Immediate functionality** - no API keys needed
- ✅ **Real UK hotel chains** with accurate data
- ✅ **Realistic pricing** based on location and dates
- ✅ **Direct booking information** (phone/website)
- ✅ **Comprehensive coverage** of all UK locations

---

### 🆓 No API Keys? No Problem!

The system provides **excellent functionality** without any API setup:

#### Train Data (Demo Mode):
- ✅ **Realistic UK routes** and timetables
- ✅ **Popular destinations** and journey planning
- ✅ **Station information** and facilities
- ✅ **Sample pricing** based on real routes

#### Hotel Data (Multi-Hotel API Server):
- ✅ **Real UK hotel chains** (Premier Inn, Holiday Inn Express, Ibis, Travelodge)
- ✅ **Realistic pricing** (£50-£150/night based on location)
- ✅ **Real contact information** (phone numbers, websites)
- ✅ **Accurate locations** for all UK cities including East Croydon
- ✅ **Hotel amenities** and ratings (8.0-9.0/10)

---

### 🔐 API Key Security

#### Best Practices:
- **Never commit** API keys to version control
- **Use environment variables** for production
- **Rotate keys** regularly
- **Monitor usage** to avoid rate limits

#### Environment Variables (Production):
```bash
# Add to your .env file (not committed to Git)
TRANSPORT_API_KEY=your_transport_api_key
TRANSPORT_APP_ID=your_transport_app_id
RAPIDAPI_KEY=your_rapidapi_key
```

#### Rate Limits:
- **Transport API:** 1,000 requests/day (free)
- **RapidAPI Hotels:** 100 requests/month (free)
- **System caching:** Reduces API calls automatically

---

### 🧪 Testing Your API Setup

#### Verify Transport API:
```bash
# Test live train data
./venv/bin/python -c "
from real_trainline_mcp_server import RealTrainlineMCPServer
server = RealTrainlineMCPServer()
print('Transport API:', 'Configured' if server.transport_api_key != '1' else 'Demo Mode')
"
```

#### Verify Multi-Hotel API:
```bash
# Test hotel API server
./venv/bin/python demo_hotel_search.py
# Look for "UK Hotel Chains: ✅ Loading major chains..." in output

# Test specific location
./venv/bin/python -c "
from multi_hotel_api_server import MultiHotelAPIServer
server = MultiHotelAPIServer()
result = server.search_hotels_multi('East Croydon', '2025-12-15', '2025-12-16', 1)
print('Hotel search working:', 'Premier Inn' in result)
"
```

#### Web Interface Test:
1. Start: `./venv/bin/python strand_agent_web.py`
2. Open: http://localhost:5002
3. Try: *"Find trains from London to Manchester today"*
4. Look for **real times** vs **demo data**

---

### 💡 API Alternatives

If the recommended APIs are unavailable:

#### Train Data Alternatives:
- **National Rail Enquiries API** (UK official)
- **Trainline Partner API** (requires partnership)
- **OpenRailData** (real-time feeds)

#### Hotel Data Enhancement Options:
- **Additional hotel chains** can be added to the database
- **OpenStreetMap** provides real location coordinates
- **Custom pricing algorithms** can be implemented
- **Real-time availability** could be added via hotel websites

---

### 🚀 Production Deployment

For production use with APIs:

1. **Set up monitoring** for API usage
2. **Implement caching** to reduce API calls
3. **Add fallback** to demo data if APIs fail
4. **Use load balancing** for high traffic
5. **Monitor rate limits** and upgrade plans as needed

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

## 🔑 Quick API Reference

### Transport API (Trains)
- **Website:** https://transportapi.com
- **Free Tier:** 1,000 requests/day
- **Setup:** `./venv/bin/python setup_real_apis.py`
- **Credentials:** App ID + API Key

### Multi-Hotel API Server
- **File:** `multi_hotel_api_server.py`
- **Data Sources:** UK Hotel Chains + OpenStreetMap
- **Setup:** None required - works immediately
- **Coverage:** All UK locations with realistic data

### Demo Mode (No APIs)
- **Trains:** Realistic UK routes and timetables
- **Hotels:** Real UK hotel chains with contact info
- **Setup:** None required - works immediately!

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🎉 Acknowledgments

- **Transport API** for UK rail data
- **UK Hotel Chains** for accommodation data
- **Model Context Protocol** for the architecture framework
- **Kiro IDE** for development environment

---

🧳 **Your complete travel planning companion - from trains to hotels, all orchestrated intelligently!** ✈️🏨🚂