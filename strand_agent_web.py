#!/usr/bin/env python3
"""
MCP Strand Agent Web Interface - Web UI for the orchestrating agent
"""
from flask import Flask, render_template, request, jsonify, session
import json
from datetime import datetime
import os
from mcp_strand_agent import MCPStrandAgent

app = Flask(__name__)
app.secret_key = 'mcp_strand_agent_secret_key_2024'

# Initialize the strand agent
agent = MCPStrandAgent()

@app.route('/')
def index():
    """Main page for the strand agent"""
    return render_template('strand_agent.html')

@app.route('/api/capabilities')
def api_capabilities():
    """Get agent capabilities"""
    try:
        capabilities = agent.get_capabilities()
        all_tools = agent.get_all_tools()
        
        # Format for web display
        servers = {}
        for tool_name, tool_info in all_tools.items():
            server = tool_info["client"]
            if server not in servers:
                servers[server] = []
            servers[server].append({
                "name": tool_info["original_name"],
                "description": tool_info["description"],
                "full_name": tool_name
            })
        
        return jsonify({
            "success": True,
            "capabilities": capabilities,
            "servers": servers,
            "total_tools": len(all_tools),
            "total_servers": len(agent.clients)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/process', methods=['POST'])
def api_process():
    """Process user request through the strand agent"""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({
                "success": False,
                "error": "Please provide a message"
            })
        
        # Debug: Check agent state
        print(f"🔍 Processing: '{user_input}'")
        print(f"🔧 Agent has {len(agent.clients)} servers")
        print(f"🔧 Total tools: {len(agent.get_all_tools())}")
        
        # Process through strand agent
        response = agent.process_request(user_input)
        
        # Debug: Check response
        print(f"📤 Response length: {len(response)}")
        print(f"📤 Contains 'relevant tools': {'could not find any relevant tools' in response}")
        
        # Get conversation history
        history = agent.conversation_history[-10:]  # Last 10 entries
        
        return jsonify({
            "success": True,
            "response": response,
            "history": history,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/history')
def api_history():
    """Get conversation history"""
    try:
        history = agent.conversation_history[-20:]  # Last 20 entries
        return jsonify({
            "success": True,
            "history": history
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/clear_history', methods=['POST'])
def api_clear_history():
    """Clear conversation history"""
    try:
        agent.conversation_history = []
        return jsonify({
            "success": True,
            "message": "History cleared"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/suggest')
def api_suggest():
    """Get suggestion prompts"""
    suggestions = {
        "travel": [
            "Plan a trip from London to Edinburgh on December 20, returning December 22",
            "Find trains from London to Manchester today and hotels there for tonight",
            "Compare hotel prices in Paris, London, and Berlin for December 20-22",
            "Find hotels near King's Cross station for December 20-21"
        ],
        "trains": [
            "Find trains from London to Manchester today",
            "Show departures from Birmingham",
            "Get station info for King's Cross",
            "Find stations in Edinburgh",
            "Popular UK train routes"
        ],
        "hotels": [
            "Find hotels in London for December 20-22 for 2 guests",
            "Search hotels in Paris for next weekend",
            "Show me hotels near Eiffel Tower for December 25-27",
            "Compare hotel prices in Rome and Florence",
            "Find budget hotels in Berlin for 3 nights"
        ],
        "general": [
            "Hello, my name is Alice",
            "Calculate 15 * 7 + 3",
            "What time is it?",
            "Greet John"
        ]
    }
    
    return jsonify({
        "success": True,
        "suggestions": suggestions
    })

@app.route('/api/quick_search', methods=['POST'])
def api_quick_search():
    """Quick search for trains or hotels using strand agent"""
    try:
        data = request.get_json()
        search_type = data.get('type')  # 'train' or 'hotel'
        
        if search_type == 'train':
            query = f"Find trains from {data.get('from')} to {data.get('to')} on {data.get('date')}"
            if data.get('time'):
                query += f" at {data.get('time')}"
        elif search_type == 'hotel':
            # Format the hotel query to match what the strand agent expects
            checkin = data.get('checkin')
            checkout = data.get('checkout')
            destination = data.get('destination')
            guests = data.get('guests', 2)
            
            # Convert dates to a format the agent can understand
            if checkin and checkout:
                # Try to extract month and day for natural language
                try:
                    from datetime import datetime as dt
                    checkin_date = dt.strptime(checkin, '%Y-%m-%d')
                    checkout_date = dt.strptime(checkout, '%Y-%m-%d')
                    
                    checkin_formatted = checkin_date.strftime('%B %d')  # e.g., "December 20"
                    checkout_formatted = checkout_date.strftime('%B %d')  # e.g., "December 22"
                    
                    query = f"Find hotels in {destination} for {checkin_formatted} to {checkout_formatted}"
                    if guests != 2:
                        query += f" for {guests} guests"
                except:
                    # Fallback to original format
                    query = f"Find hotels in {destination} for {checkin} to {checkout}"
                    if guests != 2:
                        query += f" for {guests} guests"
            else:
                query = f"Find hotels in {destination}"
        else:
            return jsonify({
                "success": False,
                "error": "Invalid search type"
            })
        
        # Debug: Log the query being processed
        print(f"🔍 Quick search query: '{query}'")
        print(f"🔧 Agent servers: {list(agent.clients.keys())}")
        
        # Process through strand agent (same as regular chat)
        response = agent.process_request(query)
        
        # Debug: Check response
        print(f"📤 Quick search response length: {len(response)}")
        print(f"📤 Response preview: {response[:100]}")
        
        # Get the latest conversation entry for metadata
        history = agent.conversation_history[-5:] if agent.conversation_history else []
        
        return jsonify({
            "success": True,
            "response": response,
            "query": query,
            "history": history,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/travel_plan', methods=['POST'])
def api_travel_plan():
    """Complete travel planning using strand agent"""
    try:
        data = request.get_json()
        
        from_city = data.get('from_city')
        to_city = data.get('to_city')
        travel_date = data.get('travel_date')
        return_date = data.get('return_date')
        guests = data.get('guests', 2)
        
        # Format dates for better natural language processing
        try:
            from datetime import datetime as dt
            travel_dt = dt.strptime(travel_date, '%Y-%m-%d')
            travel_formatted = travel_dt.strftime('%B %d')  # e.g., "December 20"
            
            if return_date:
                return_dt = dt.strptime(return_date, '%Y-%m-%d')
                return_formatted = return_dt.strftime('%B %d')
                query = f"Plan a complete trip from {from_city} to {to_city} on {travel_formatted}, returning {return_formatted} for {guests} people"
            else:
                query = f"Plan a one-way trip from {from_city} to {to_city} on {travel_formatted} for {guests} people"
        except:
            # Fallback to original format
            if return_date:
                query = f"Plan a complete trip from {from_city} to {to_city} on {travel_date}, returning {return_date} for {guests} guests"
            else:
                query = f"Plan a one-way trip from {from_city} to {to_city} on {travel_date} for {guests} guests"
        
        # Process through strand agent (same as regular chat)
        response = agent.process_request(query)
        
        # Get conversation history for metadata
        history = agent.conversation_history[-5:] if agent.conversation_history else []
        
        return jsonify({
            "success": True,
            "response": response,
            "query": query,
            "history": history,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("🤖 Starting MCP Strand Agent Web Interface...")
    print("📱 Open your browser to: http://localhost:5002")
    print(f"🔗 Connected to {len(agent.clients)} MCP servers")
    
    if agent.clients:
        print("✅ Available servers:")
        for name, client in agent.clients.items():
            print(f"   • {name}: {len(client.tools)} tools")
    else:
        print("⚠️  No MCP servers connected")
    
    app.run(debug=True, host='0.0.0.0', port=5002)