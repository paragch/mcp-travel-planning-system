#!/usr/bin/env python3
"""
Test script for MCP Strand Agent
"""
from mcp_strand_agent import MCPStrandAgent

def test_strand_agent():
    """Test the strand agent with various requests"""
    print("🤖 Testing MCP Strand Agent")
    print("=" * 50)
    
    # Initialize agent
    agent = MCPStrandAgent()
    
    if not agent.clients:
        print("❌ No MCP servers available for testing")
        return
    
    print(f"✅ Agent initialized with {len(agent.clients)} servers")
    print()
    
    # Test cases
    test_cases = [
        "Hello, my name is Alice",
        "Calculate 15 * 7 + 3", 
        "Find trains from London to Manchester today",
        "Show departures from Birmingham",
        "Get station info for King's Cross",
        "What is 100 divided by 4?",
        "Greet John",
        "Find stations in Edinburgh"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"Test {i}: '{test_input}'")
        print("-" * 30)
        
        try:
            response = agent.process_request(test_input)
            print(f"Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        print("=" * 50)
        print()

def test_capabilities():
    """Test capabilities discovery"""
    print("🔍 Testing Capabilities Discovery")
    print("=" * 40)
    
    agent = MCPStrandAgent()
    
    # Show all tools
    all_tools = agent.get_all_tools()
    print(f"📊 Total tools available: {len(all_tools)}")
    
    for tool_name, tool_info in all_tools.items():
        print(f"🔧 {tool_name}")
        print(f"   Server: {tool_info['client']}")
        print(f"   Description: {tool_info['description']}")
        print()
    
    # Show capabilities summary
    print("📋 Capabilities Summary:")
    print(agent.get_capabilities())

def interactive_test():
    """Run interactive test session"""
    print("🎮 Interactive Test Mode")
    print("=" * 30)
    print("Type your requests (or 'quit' to exit):")
    print()
    
    agent = MCPStrandAgent()
    
    while True:
        try:
            user_input = input("Test: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                break
            elif user_input.lower() == 'capabilities':
                print(agent.get_capabilities())
            elif user_input:
                response = agent.process_request(user_input)
                print(f"Agent: {response}")
                print()
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚂 MCP Strand Agent Test Suite")
    print("=" * 40)
    
    choice = input("""
Choose test mode:
1. Automated tests
2. Capabilities discovery  
3. Interactive mode
4. All tests

Enter choice (1-4): """).strip()
    
    if choice == "1":
        test_strand_agent()
    elif choice == "2":
        test_capabilities()
    elif choice == "3":
        interactive_test()
    elif choice == "4":
        test_capabilities()
        print("\n" + "="*60 + "\n")
        test_strand_agent()
        print("\n" + "="*60 + "\n")
        interactive_test()
    else:
        print("Invalid choice. Running all tests...")
        test_capabilities()
        test_strand_agent()

if __name__ == "__main__":
    main()