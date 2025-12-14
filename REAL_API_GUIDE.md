# 🚂 Real Train API Integration Guide

This guide will help you integrate your MCP server with real UK train APIs to get live data, prices, and booking information.

## 🎯 What You'll Get

With real API integration, your MCP server will provide:

✅ **Live departure times**  
✅ **Real-time delays and cancellations**  
✅ **Actual ticket prices**  
✅ **Platform information**  
✅ **Journey planning with connections**  
✅ **Service disruption alerts**  
✅ **Station departure boards**  

## 🔧 Quick Setup (Recommended)

### Step 1: Run the Setup Script
```bash
./venv/bin/python setup_real_api.py
```

The script will guide you through:
1. Getting Transport API credentials
2. Configuring the server
3. Testing the connection
4. Updating MCP configuration

### Step 2: Get API Access

**Transport API (Free Tier Available)**
1. Visit: https://transportapi.com
2. Click "Sign Up" 
3. Verify your email
4. Go to "My Account" → "API Keys"
5. Copy your App ID and API Key
6. Enter them in the setup script

**Free Tier Includes:**
- 1,000 requests per day
- All UK rail data
- Real-time updates
- No credit card required

## 🛠️ Manual Setup

If you prefer manual configuration:

### 1. Edit `real_trainline_mcp_server.py`

Replace these lines:
```python
self.transport_api_key = "YOUR_TRANSPORT_API_KEY"
self.transport_app_id = "YOUR_TRANSPORT_APP_ID"
```

With your actual credentials:
```python
self.transport_api_key = "your_actual_api_key_here"
self.transport_app_id = "your_actual_app_id_here"
```

### 2. Update MCP Configuration

Add to `.kiro/settings/mcp.json`:
```json
{
  "mcpServers": {
    "real-trainline": {
      "command": "./venv/bin/python",
      "args": ["real_trainline_mcp_server.py"],
      "disabled": false
    }
  }
}
```

### 3. Test the Connection

```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "find_station_codes", "arguments": {"search_term": "London"}}}' | ./venv/bin/python real_trainline_mcp_server.py
```

## 🎮 Available API Functions

### 1. `search_live_trains`
Get live train times and prices between stations.

**Example:**
```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_live_trains", "arguments": {"from_station": "London", "to_station": "Manchester", "date": "2024-12-20", "time": "09:00"}}}' | ./venv/bin/python real_trainline_mcp_server.py
```

### 2. `get_live_departures`
Get live departure board for any UK station.

**Example:**
```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_live_departures", "arguments": {"station_code": "KGX"}}}' | ./venv/bin/python real_trainline_mcp_server.py
```

### 3. `find_station_codes`
Find 3-letter codes for stations.

**Example:**
```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "find_station_codes", "arguments": {"search_term": "Birmingham"}}}' | ./venv/bin/python real_trainline_mcp_server.py
```

### 4. `get_journey_details`
Get detailed journey information with connections.

**Example:**
```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_journey_details", "arguments": {"from_code": "KGX", "to_code": "EDB", "date": "2024-12-20", "time": "10:00"}}}' | ./venv/bin/python real_trainline_mcp_server.py
```

## 🏷️ Common UK Station Codes

| Station | Code | Station | Code |
|---------|------|---------|------|
| London King's Cross | KGX | Manchester Piccadilly | MAN |
| London Paddington | PAD | Birmingham New Street | BHM |
| London Victoria | VIC | Edinburgh Waverley | EDB |
| London Waterloo | WAT | Glasgow Central | GLC |
| London Euston | EUS | Liverpool Lime Street | LIV |
| London Liverpool St | LST | Leeds | LDS |

## 🌐 Alternative APIs

### National Rail Enquiries API
- **URL:** https://www.nationalrail.co.uk/developers
- **Features:** Official UK rail data
- **Cost:** Free with registration
- **Data:** Timetables, live running info

### Trainline Partner API
- **URL:** https://trainline.com/partners
- **Features:** Booking integration, prices
- **Cost:** Commercial partnership required
- **Data:** Full booking capability

### Rail Data Marketplace
- **URL:** https://raildata.org.uk
- **Features:** Comprehensive rail data
- **Cost:** Various pricing tiers
- **Data:** Schedules, fares, disruptions

## 🔄 Web UI Integration

Your existing web UI will automatically work with the real API! Just:

1. Update your `trainline_web_ui.py` to use `real_trainline_mcp_server.py`
2. Or update the server script path in the web UI configuration

```python
# In trainline_web_ui.py, change:
self.server_script = "real_trainline_mcp_server.py"
```

## 📊 API Limits and Pricing

### Transport API Free Tier
- **Requests:** 1,000 per day
- **Rate limit:** No specific limit
- **Data:** All UK rail networks
- **Support:** Community forum

### Transport API Paid Plans
- **Starter:** £20/month (10,000 requests)
- **Professional:** £100/month (100,000 requests)
- **Enterprise:** Custom pricing

## 🛡️ Best Practices

### 1. Error Handling
The server includes comprehensive error handling for:
- Network timeouts
- API rate limits
- Invalid station codes
- Service disruptions

### 2. Caching
Consider implementing caching for:
- Station code lookups
- Timetable data (cache for 1-2 minutes)
- Popular route information

### 3. Fallback Strategy
The server automatically falls back to demo mode if:
- API keys are not configured
- API is unavailable
- Rate limits are exceeded

## 🚀 Advanced Features

### Real-Time Updates
```python
# Get live updates every 30 seconds
import time
while True:
    departures = get_live_departures("KGX")
    print(departures)
    time.sleep(30)
```

### Price Monitoring
```python
# Monitor price changes for specific routes
def monitor_prices(from_station, to_station, date):
    # Implementation for price tracking
    pass
```

### Disruption Alerts
```python
# Get service disruption notifications
def get_disruptions(station_code):
    # Implementation for disruption monitoring
    pass
```

## 🎉 Next Steps

1. **Run the setup script:** `./venv/bin/python setup_real_api.py`
2. **Test with your web UI:** Start the web interface and try searches
3. **Explore advanced features:** Add price monitoring, alerts, etc.
4. **Scale up:** Consider paid API tiers for production use

## 📞 Support

- **Transport API:** https://transportapi.com/support
- **National Rail:** https://www.nationalrail.co.uk/contact
- **This Project:** Check the README files for troubleshooting

---

🚂 **Happy train journey planning with live data!** 🎯