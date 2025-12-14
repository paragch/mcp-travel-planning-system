#!/usr/bin/env python3
"""
RapidAPI Hotel Setup - Alternative to Amadeus when it's down
"""
import webbrowser
import re

def setup_rapidapi_hotels():
    """Setup RapidAPI for real hotel data"""
    
    print("🏨 RapidAPI Hotel Setup (Alternative to Amadeus)")
    print("=" * 60)
    print("Free tier: 100 requests/month")
    print("Perfect backup when Amadeus is down!")
    print()
    
    print("📋 Step-by-step setup:")
    print()
    
    # Step 1: Registration
    print("STEP 1: Create RapidAPI Account")
    print("-" * 40)
    
    try:
        webbrowser.open("https://rapidapi.com/auth/sign-up")
        print("✅ Opened: https://rapidapi.com/auth/sign-up")
    except:
        print("⚠️  Please visit: https://rapidapi.com/auth/sign-up")
    
    print()
    print("📝 Create your account:")
    print("   • Use your email")
    print("   • Choose a password")
    print("   • Verify email")
    print()
    
    input("Press Enter after creating your account...")
    
    # Step 2: Subscribe to Booking.com API
    print()
    print("STEP 2: Subscribe to Booking.com API")
    print("-" * 40)
    
    try:
        webbrowser.open("https://rapidapi.com/apidojo/api/booking")
        print("✅ Opened: https://rapidapi.com/apidojo/api/booking")
    except:
        print("⚠️  Please visit: https://rapidapi.com/apidojo/api/booking")
    
    print()
    print("📝 Subscribe to the API:")
    print("   1. Click 'Subscribe to Test'")
    print("   2. Choose 'Basic' plan (FREE)")
    print("   3. Click 'Subscribe'")
    print()
    
    input("Press Enter after subscribing...")
    
    # Step 3: Get API Key
    print()
    print("STEP 3: Get Your API Key")
    print("-" * 40)
    print("📋 In the API dashboard:")
    print("   • Look for 'X-RapidAPI-Key' in the code examples")
    print("   • Copy the key (starts with something like 'abc123...')")
    print()
    
    api_key = input("📝 Enter your RapidAPI Key: ").strip()
    
    if not api_key:
        print("❌ API Key is required!")
        return False
    
    # Update the multi-hotel server
    try:
        with open('multi_hotel_api_server.py', 'r') as f:
            content = f.read()
        
        # Enable RapidAPI
        content = re.sub(
            r'"enabled": False  # Free tier available',
            '"enabled": True',
            content
        )
        
        # Update API key
        content = re.sub(
            r'"X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY"',
            f'"X-RapidAPI-Key": "{api_key}"',
            content
        )
        
        with open('multi_hotel_api_server.py', 'w') as f:
            f.write(content)
        
        print()
        print("✅ RapidAPI configured successfully!")
        print()
        print("🎉 You now have REAL hotel data from:")
        print("   ✅ OpenStreetMap (Free)")
        print("   ✅ UK Hotel Chains (Database)")
        print("   ✅ RapidAPI Booking.com (100 calls/month)")
        print()
        print("🔄 Restart your web server to use the new API!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating configuration: {e}")
        return False

def main():
    print("🏨 Alternative Hotel API Setup")
    print("=" * 50)
    print("Since Amadeus is down, let's use RapidAPI!")
    print()
    
    choice = input("Set up RapidAPI for real hotel data? (y/N): ").strip().lower()
    
    if choice == 'y':
        success = setup_rapidapi_hotels()
        
        if success:
            print()
            print("🎯 READY!")
            print("Your hotel search now uses multiple real APIs")
            print("Perfect backup solution when Amadeus is unavailable")
        else:
            print()
            print("❌ Setup incomplete")
    else:
        print()
        print("💡 No problem! Your system already works with:")
        print("   ✅ OpenStreetMap data (real hotel locations)")
        print("   ✅ UK hotel chains (realistic data)")
        print("   ✅ Enhanced sample data")
        print()
        print("🔄 You can set up RapidAPI later when needed")

if __name__ == "__main__":
    main()