#!/usr/bin/env python3
"""
UK Popular Routes - Pre-defined searches for common UK train routes
"""
import sys
from quick_train_search import QuickTrainSearch
from datetime import datetime

def main():
    searcher = QuickTrainSearch()
    
    # Popular UK routes
    routes = {
        "1": ("London", "Edinburgh", "London to Edinburgh (East Coast)"),
        "2": ("London", "Manchester", "London to Manchester (West Coast)"),
        "3": ("London", "Birmingham", "London to Birmingham"),
        "4": ("Manchester", "Liverpool", "Manchester to Liverpool"),
        "5": ("London", "Bristol", "London to Bristol"),
        "6": ("Birmingham", "Leeds", "Birmingham to Leeds"),
        "7": ("London", "Glasgow", "London to Glasgow"),
        "8": ("Newcastle", "London", "Newcastle to London"),
        "9": ("Cardiff", "London", "Cardiff to London"),
        "10": ("Edinburgh", "Glasgow", "Edinburgh to Glasgow")
    }
    
    if len(sys.argv) > 1 and sys.argv[1] in routes:
        # Direct route selection
        route_num = sys.argv[1]
        from_station, to_station, description = routes[route_num]
        date = sys.argv[2] if len(sys.argv) > 2 else datetime.now().strftime("%Y-%m-%d")
        
        print(f"🚂 {description}")
        print(f"📅 Date: {date}")
        print("-" * 50)
        
        result = searcher.search_trains(from_station, to_station, date)
        print(result)
        return
    
    # Interactive menu
    print("🚂 UK Popular Train Routes")
    print("=" * 30)
    
    for num, (from_station, to_station, description) in routes.items():
        print(f"{num:2}. {description}")
    
    print("\nUsage:")
    print("  python uk_routes.py [route_number] [date]")
    print("  python uk_routes.py 1 2024-12-25")
    print("\nOr run interactively and choose a route number.")
    
    if len(sys.argv) == 1:
        try:
            choice = input("\nEnter route number (1-10): ").strip()
            
            if choice in routes:
                from_station, to_station, description = routes[choice]
                
                date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                date = date_input if date_input else datetime.now().strftime("%Y-%m-%d")
                
                print(f"\n🚂 {description}")
                print(f"📅 Date: {date}")
                print("-" * 50)
                
                result = searcher.search_trains(from_station, to_station, date)
                print(result)
            else:
                print("❌ Invalid route number.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()