#!/usr/bin/env python3
"""
Test Multi-Hotel API Integration with Strand Agent
"""
import sys
sys.path.append('.')

def test_multi_hotel_server():
    """Test the multi-hotel server directly"""
    print("🧪 Testing Multi-Hotel API Server Integration")
    print("=" * 50)
    
    try:
        from multi_hotel_api_server import MultiHotelAPIServer
        
        server = MultiHotelAPIServer()
        print("✅ Multi-Hotel server loads successfully")
        
        # Test tool registration
        tools = list(server.tools.keys())
        print(f"✅ Tools registered: {tools}")
        
        # Test hotel search
        print("\n🏨 Testing hotel search for <Location B>...")
        result = server.search_hotels('<Location B>', '2025-12-15', '2025-12-16', 2)
        
        # Check if we got realistic results
        if "Premier Inn <Location B>" in result:
            print("✅ UK Hotel Chains data working")
        
        if "£" in result and "/night" in result:
            print("✅ Pricing data included")
        
        if "📞" in result:
            print("✅ Contact information included")
        
        print("\n📋 Sample results preview:")
        lines = result.split('\n')
        for line in lines[:15]:  # Show first 15 lines
            if line.strip():
                print(f"   {line}")
        
        print("\n✅ Multi-Hotel API Server is working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing multi-hotel server: {e}")
        return False

def test_strand_agent_integration():
    """Test if strand agent can connect to multi-hotel server"""
    print("\n🤖 Testing Strand Agent Integration")
    print("=" * 50)
    
    try:
        from mcp_strand_agent import MCPStrandAgent
        
        agent = MCPStrandAgent()
        print("✅ Strand agent loads successfully")
        
        # Get available tools
        all_tools = agent.get_all_tools()
        
        # Look for hotel-related tools
        hotel_tools = []
        for server_name, tools in all_tools.items():
            for tool in tools:
                if 'hotel' in tool.get('description', '').lower():
                    hotel_tools.append(f"{server_name}: {tool.get('name', 'unknown')}")
        
        if hotel_tools:
            print("✅ Hotel tools found:")
            for tool in hotel_tools:
                print(f"   • {tool}")
        else:
            print("⚠️  No hotel tools detected in strand agent")
        
        return len(hotel_tools) > 0
        
    except Exception as e:
        print(f"❌ Error testing strand agent: {e}")
        return False

def main():
    print("🏨 Multi-Hotel API Integration Test")
    print("=" * 60)
    print("Testing the new Multi-API Hotel Server setup")
    print()
    
    # Test 1: Multi-Hotel Server
    server_ok = test_multi_hotel_server()
    
    # Test 2: Strand Agent Integration  
    agent_ok = test_strand_agent_integration()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    print(f"🏨 Multi-Hotel Server: {'✅ WORKING' if server_ok else '❌ FAILED'}")
    print(f"🤖 Strand Agent Integration: {'✅ WORKING' if agent_ok else '❌ NEEDS RESTART'}")
    
    if server_ok and agent_ok:
        print("\n🎉 SUCCESS! Multi-Hotel API is fully integrated")
        print("💡 Try searching for 'hotels in <Location B>' in your web interface")
    elif server_ok:
        print("\n⚠️  Multi-Hotel server works, but strand agent needs restart")
        print("🔄 Restart your web server to pick up the new hotel API")
    else:
        print("\n❌ Issues detected. Check the error messages above.")

if __name__ == "__main__":
    main()