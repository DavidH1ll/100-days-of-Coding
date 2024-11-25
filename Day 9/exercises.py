import os

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

travel_log = {
    "France": {
        "capital": "Paris",
        "visited_cities": ["Lyon", "Marseille", "Nice"]
    },
    "Germany": {
        "capital": "Berlin",
        "visited_cities": ["Munich", "Hamburg", "Frankfurt"]
    },
    "Italy": {
        "capital": "Rome",
        "visited_cities": ["Milan", "Venice", "Florence"]
    },
    "Spain": {
        "capital": "Madrid",
        "visited_cities": ["Barcelona", "Seville", "Valencia"]
    },
    "Japan": {
        "capital": "Tokyo",
        "visited_cities": ["Osaka", "Kyoto", "Hiroshima"]
    }
}

# Clear screen before output
clear_screen()
print(travel_log["Japan"]["visited_cities"][1])