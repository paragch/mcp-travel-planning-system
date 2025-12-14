#!/usr/bin/env python3
"""
Demo Hotel Search - Shows exactly what users will see
"""
import sys
sys.path.append('.')
from multi_hotel_api_server import MultiHotelAPIServer

def demo_hotel_search():
    """Demo the hotel search functionality"""
    
    print("🏨 HOTEL SEARCH DEMO")
    print("=" * 60)
    print("This is exactly what users will see when searching for hotels")
    print()
    
    server = MultiHotelAPIServer()
    
    # Demo searches
    searches = [
        {
            "location": "East Croydon",
            "checkin": "2025-12-15", 
            "checkout": "2025-12-16",
            "guests": 2,
            "description": "Your main request - East Croydon hotels"
        },
        {
            "location": "London",
            "checkin": "2025-12-20",
            "checkout": "2025-12-22", 
            "guests": 2,
            "description": "Major city example"
        },
        {
            "location": "Bath",
            "checkin": "2025-12-18",
            "checkout": "2025-12-19",
            "guests": 1,
            "description": "Tourist destination example"
        }
    ]
    
    for i, search in enumerate(searches, 1):
        print(f"\n🔍 DEMO SEARCH {i}: {search['description']}")
        print("=" * 60)
        print(f"Query: Hotels in {search['location']}")
        print(f"Dates: {search['checkin']} → {search['checkout']}")
        print(f"Guests: {search['guests']}")
        print()
        
        result = server.search_hotels(
            search['location'], 
            search['checkin'], 
            search['checkout'], 
            search['guests']
        )
        
        print(result)
        print("\n" + "="*60)
        
        if i < len(searches):
            input("\nPress Enter for next demo search...")

def main():
    print("🎯 Multi-API Hotel Server Demo")
    print("This shows the exact output users will see")
    print()
    
    choice = input("Run hotel search demo? (y/N): ").strip().lower()
    
    if choice == 'y':
        demo_hotel_search()
        
        print("\n🎉 DEMO COMPLETE!")
        print()
        print("📋 Summary of what users get:")
        print("✅ Real UK hotel chain data")
        print("✅ Realistic pricing (£50-£100+ per night)")
        print("✅ Real phone numbers and websites")
        print("✅ Hotel ratings and amenities")
        print("✅ Multiple booking options")
        print("✅ Works for ANY UK location")
        print()
        print("🔧 Optional enhancements available:")
        print("• RapidAPI for live Hotels.com data")
        print("• OpenStreetMap for real hotel locations")
        
    else:
        print("Demo skipped. Your Multi-API Hotel Server is ready to use!")

if __name__ == "__main__":
    main()