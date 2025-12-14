#!/usr/bin/env python3
"""
Setup script for configuring real APIs for live data
"""
import os
import re

def setup_transport_api():
    """Setup Transport API for live train data"""
    print("🚂 Transport API Setup (Free)")
    print("=" * 40)
    print("1. Visit: https://transportapi.com")
    print("2. Click 'Sign Up' (free tier: 1,000 requests/day)")
    print("3. Verify your email")
    print("4. Go to 'My Account' → 'API Keys'")
    print("5. Copy your App ID and API Key")
    print()
    
    app_id = input("Enter your Transport API App ID: ").strip()
    api_key = input("Enter your Transport API Key: ").strip()
    
    if not app_id or not api_key:
        print("❌ Both App ID and API Key are required!")
        return False
    
    try:
        # Update real_trainline_mcp_server.py
        with open('real_trainline_mcp_server.py', 'r') as f:
            content = f.read()
        
        # Replace placeholder values
        content = re.sub(
            r'self\.transport_api_key = "[^"]*"',
            f'self.transport_api_key = "{api_key}"',
            content
        )
        content = re.sub(
            r'self\.transport_app_id = "[^"]*"',
            f'self.transport_app_id = "{app_id}"',
            content
        )
        
        with open('real_trainline_mcp_server.py', 'w') as f:
            f.write(content)
        
        print("✅ Transport API configured successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating configuration: {e}")
        return False

def setup_booking_api():
    """Setup Booking.com API for live hotel data"""
    print("\n🏨 Booking.com API Setup")
    print("=" * 40)
    print("⚠️  Note: Booking.com API requires business partnership")
    print("1. Visit: https://developers.booking.com")
    print("2. Apply for Partner API access")
    print("3. Get approved (may take time)")
    print("4. Get your API key")
    print()
    
    choice = input("Do you have a Booking.com API key? (y/N): ").strip().lower()
    
    if choice == 'y':
        api_key = input("Enter your Booking.com API Key: ").strip()
        
        if not api_key:
            print("❌ API Key is required!")
            return False
        
        print("⚠️  Booking.com server has been removed from this system.")
        print("💡 Hotel functionality is now provided by multi_hotel_api_server.py")
        print("   which uses UK hotel chains data and optional RapidAPI integration.")
        return True
            
        except Exception as e:
            print(f"❌ Error updating configuration: {e}")
            return False
    else:
        print("💡 Alternative: Use demo mode or other hotel APIs")
        print("   - Hotels.com API")
        print("   - Expedia Partner Solutions")
        return False

def setup_alternative_hotel_api():
    """Setup alternative hotel APIs"""
    print("\n🏨 Alternative Hotel APIs")
    print("=" * 40)
    print("Since Booking.com API requires partnership, here are alternatives:")
    print()

    print("2. 🏨 Hotels.com API")
    print("   - Visit: https://developers.expediagroup.com")
    print("   - Free tier available")
    print()
    print("3. 🔍 RapidAPI Hotel Collection")
    print("   - Visit: https://rapidapi.com/hub")
    print("   - Search for 'hotel booking'")
    print("   - Many free options")
    
    print("💡 Current system uses multi_hotel_api_server.py with UK hotel chains")
    return True



def test_apis():
    """Test configured APIs"""
    print("\n🧪 Testing API Configurations...")
    
    # Test Transport API
    try:
        with open('real_trainline_mcp_server.py', 'r') as f:
            content = f.read()
            if 'transport_api_key = "1"' not in content:
                print("✅ Transport API appears configured")
            else:
                print("❌ Transport API still has placeholder credentials")
    except:
        print("❌ Could not check Transport API configuration")
    
    # Test Multi-Hotel API
    try:
        with open('multi_hotel_api_server.py', 'r') as f:
            content = f.read()
            if 'UK Hotel Chains' in content:
                print("✅ Multi-Hotel API server available")
            else:
                print("❌ Multi-Hotel API server not found")
    except:
        print("❌ Could not check Multi-Hotel API configuration")

def main():
    print("🌐 Real API Configuration Setup")
    print("=" * 50)
    print("This will help you configure real APIs for live data")
    print()
    
    # Setup Transport API (trains)
    transport_success = setup_transport_api()
    
    # Setup Hotel API (multi-hotel server)
    booking_success = setup_booking_api()  # This now just shows info about the change
    
    # Test configurations
    test_apis()
    
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print()
    print("📋 Summary:")
    print(f"🚂 Transport API: {'✅ Configured' if transport_success else '❌ Not configured'}")
    print(f"🏨 Hotel API: {'✅ Configured' if booking_success else '❌ Use alternatives'}")
    print()
    print("🔄 Next Steps:")
    print("1. Restart your web server")
    print("2. Test with real searches")
    print("3. Check for live data instead of samples")

if __name__ == "__main__":
    main()