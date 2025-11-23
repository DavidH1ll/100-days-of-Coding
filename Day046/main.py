"""
Day 46 - Musical Time Machine with Spotify

Create a playlist of the top 100 songs from any date in the past by:
1. Scraping Billboard Hot 100 chart data using Beautiful Soup
2. Extracting song titles and artists
3. Using Spotify API to create a playlist
4. Searching Spotify for each song and adding to the playlist

Project Goals:
1. Scrape Billboard Hot 100 chart for a specific date
2. Extract all song titles and artists
3. Authenticate with Spotify API
4. Create a new playlist for the chosen date
5. Search for each song on Spotify
6. Add songs to the newly created playlist
7. Display confirmation with playlist link

The result is a personalized playlist that can transport you back to any
moment in the past 20 years through music!
"""

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from datetime import datetime

# ============================================================================
# Configuration
# ============================================================================

# Spotify API Credentials
# Get these from: https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', 'YOUR_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', 'YOUR_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')

# Billboard URL - will construct with the date
BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================================
# Billboard Scraper
# ============================================================================

def scrape_billboard_hot_100(date_string):
    """
    Scrape the Billboard Hot 100 chart for a specific date.
    
    Args:
        date_string: Date in format "YYYY-MM-DD" (e.g., "2000-12-30")
    
    Returns:
        List of tuples (song_title, artist_name) or None if scraping fails
    """
    print("=" * 70)
    print(f"[MUSIC] Musical Time Machine - Scraping Billboard Hot 100")
    print("=" * 70)
    print()
    
    try:
        # Construct the URL with the date
        url = f"{BILLBOARD_URL}{date_string}"
        print(f"[DATE] Target Date: {date_string}")
        print(f"[URL] URL: {url}\n")
        
        print("[DOWNLOAD] Fetching Billboard Hot 100 chart...")
        
        # Fetch the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print("[OK] Page fetched successfully!\n")
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("[SEARCH] Parsing HTML structure...")
        
        # Find all song containers
        # Billboard uses specific class names for the chart entries
        song_containers = soup.find_all('li', class_='o-chart-results-list__item')
        
        if not song_containers:
            print("[WARNING]  No songs found. The website structure may have changed.")
            print("Billboard frequently updates their HTML structure.")
            print("Please verify the URL and HTML selectors.\n")
            return None
        
        print(f"[OK] Found {len(song_containers)} songs on the chart!\n")
        
        # Extract song titles and artists
        songs = []
        
        print("[MUSIC] Extracting song data...")
        print("-" * 70)
        
        for index, container in enumerate(song_containers, 1):
            try:
                # Extract song title
                title_element = container.find('h3', class_='c-title')
                if not title_element:
                    continue
                    
                song_title = title_element.get_text(strip=True)
                
                # Extract artist name
                artist_element = container.find('span', class_='c-label')
                if not artist_element:
                    # Try alternative selector
                    artist_element = container.find('p', class_='c-tagline')
                
                if artist_element:
                    artist_name = artist_element.get_text(strip=True)
                else:
                    artist_name = "Unknown Artist"
                
                songs.append((song_title, artist_name))
                
                # Print first 10 songs as preview
                if index <= 10:
                    print(f"{index:3d}. {song_title}")
                    print(f"      by {artist_name}")
                    
            except Exception as e:
                print(f"[WARNING]  Error parsing song {index}: {e}")
                continue
        
        print("-" * 70)
        print(f"[OK] Successfully extracted {len(songs)} songs!\n")
        
        return songs
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error fetching the website: {e}\n")
        return None
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}\n")
        return None


# ============================================================================
# Spotify Playlist Creator
# ============================================================================

def create_spotify_playlist(date_string, songs):
    """
    Create a Spotify playlist and add songs to it.
    
    Args:
        date_string: Date in format "YYYY-MM-DD"
        songs: List of tuples (song_title, artist_name)
    
    Returns:
        Playlist URL or None if creation fails
    """
    print("=" * 70)
    print("[MUSIC] Setting up Spotify Integration")
    print("=" * 70)
    print()
    
    try:
        # Check if credentials are configured
        if SPOTIFY_CLIENT_ID == 'YOUR_CLIENT_ID' or SPOTIFY_CLIENT_SECRET == 'YOUR_CLIENT_SECRET':
            print("[WARNING]  Spotify credentials not configured!")
            print("\nTo use the Spotify integration, you need to:")
            print("1. Go to https://developer.spotify.com/dashboard")
            print("2. Create a new app to get Client ID and Client Secret")
            print("3. Set environment variables:")
            print("   - SPOTIFY_CLIENT_ID")
            print("   - SPOTIFY_CLIENT_SECRET")
            print("   - SPOTIFY_REDIRECT_URI (default: http://localhost:8888/callback)")
            print("\nFor now, we can still display the song list!\n")
            return None
        
        print("🔐 Authenticating with Spotify...")
        
        # Authenticate with Spotify
        sp_oauth = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="playlist-modify-public playlist-modify-private"
        )
        
        sp = spotipy.Spotify(auth_manager=sp_oauth)
        
        print("[OK] Successfully authenticated!\n")
        
        # Get current user
        user = sp.current_user()
        user_id = user['id']
        print(f"[USER] Logged in as: {user['display_name']}\n")
        
        # Create playlist name with date
        playlist_name = f"[MUSIC] Time Machine: {date_string}"
        playlist_description = (
            f"Top 100 songs from Billboard Hot 100 on {date_string}. "
            f"Created by Musical Time Machine project."
        )
        
        print(f"[WRITE] Creating playlist: {playlist_name}...")
        
        # Create the playlist
        playlist = sp.user_playlist_create(
            user_id,
            playlist_name,
            public=True,
            description=playlist_description
        )
        
        playlist_id = playlist['id']
        playlist_url = playlist['external_urls']['spotify']
        
        print(f"[OK] Playlist created: {playlist_url}\n")
        
        # Search for and add songs
        print("=" * 70)
        print("[SEARCH] Searching Spotify for songs")
        print("=" * 70)
        print()
        
        found_songs = []
        not_found = []
        
        for index, (title, artist) in enumerate(songs, 1):
            try:
                # Search for the song
                search_query = f"track:{title} artist:{artist}"
                results = sp.search(q=search_query, type='track', limit=1)
                
                if results['tracks']['items']:
                    track = results['tracks']['items'][0]
                    track_id = track['id']
                    found_songs.append(track_id)
                    
                    # Print progress for every 10 songs
                    if index % 10 == 0 or index <= 5 or index == len(songs):
                        print(f"[OK] [{index:3d}/{len(songs)}] Found: {title} - {artist}")
                else:
                    not_found.append((title, artist))
                    print(f"[ERROR] [{index:3d}/{len(songs)}] Not found: {title} - {artist}")
                    
            except Exception as e:
                print(f"[WARNING]  Error searching for {title}: {e}")
                not_found.append((title, artist))
                continue
        
        print()
        print("-" * 70)
        print(f"Found: {len(found_songs)}/{len(songs)} songs")
        print(f"Not found: {len(not_found)}/{len(songs)} songs")
        print("-" * 70)
        print()
        
        # Add found songs to playlist (in batches of 100)
        if found_songs:
            print("[WRITE] Adding songs to playlist...")
            
            for i in range(0, len(found_songs), 100):
                batch = found_songs[i:i+100]
                sp.playlist_add_items(playlist_id, batch)
                print(f"[OK] Added {len(batch)} songs (batch {i//100 + 1})")
            
            print()
            print("=" * 70)
            print("[CELEBRATE] Playlist Created Successfully!")
            print("=" * 70)
            print(f"\n[MUSIC] Playlist: {playlist_name}")
            print(f"[CHART] Songs added: {len(found_songs)}")
            print(f"[URL] Link: {playlist_url}")
            print()
            
            return playlist_url
        else:
            print("[ERROR] No songs were found on Spotify.\n")
            return None
            
    except spotipy.exceptions.SpotifyException as e:
        print(f"[ERROR] Spotify API error: {e}\n")
        return None
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}\n")
        return None


# ============================================================================
# Display and Save Results
# ============================================================================

def display_song_list(songs, date_string):
    """
    Display the song list and optionally save to file.
    
    Args:
        songs: List of tuples (song_title, artist_name)
        date_string: Date in format "YYYY-MM-DD"
    """
    print("=" * 70)
    print("[CHART] Top 100 Songs from Billboard Hot 100")
    print("=" * 70)
    print()
    
    for index, (title, artist) in enumerate(songs, 1):
        print(f"{index:3d}. {title}")
        print(f"      by {artist}")
        if index % 5 == 0:
            print()
    
    # Save to file
    filename = f"billboard_hot_100_{date_string}.txt"
    filepath = os.path.join(SCRIPT_DIR, filename)
    
    print(f"[SAVE] Saving song list to {filename}...")
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Billboard Hot 100 - {date_string}\n")
            f.write("=" * 70 + "\n\n")
            
            for index, (title, artist) in enumerate(songs, 1):
                f.write(f"{index:3d}. {title}\n")
                f.write(f"      by {artist}\n\n")
        
        print(f"[OK] Saved to: {filepath}\n")
    except Exception as e:
        print(f"[WARNING]  Could not save file: {e}\n")


# ============================================================================
# Main Program
# ============================================================================

def main():
    """
    Main program to run the Musical Time Machine.
    """
    print("\n")
    print("=" * 70)
    print("Day 46 - Musical Time Machine with Spotify".center(70))
    print("=" * 70)
    print()
    
    # Get date from user
    print("[MUSIC] Let's create a playlist from the past!\n")
    
    # Example date (you can modify this or accept user input)
    date_input = input("Enter a date (YYYY-MM-DD) or press Enter for 2000-12-30: ").strip()
    
    if not date_input:
        date_input = "2000-12-30"
    
    # Validate date format
    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print("[ERROR] Invalid date format. Please use YYYY-MM-DD")
        return
    
    # Scrape Billboard Hot 100
    songs = scrape_billboard_hot_100(date_input)
    
    if not songs:
        print("[ERROR] Failed to scrape Billboard. Exiting.\n")
        return
    
    print()
    
    # Display the song list
    display_song_list(songs, date_input)
    
    print()
    
    # Create Spotify playlist
    playlist_url = create_spotify_playlist(date_input, songs)
    
    print()
    print("=" * 70)
    print("Project Summary")
    print("=" * 70)
    print()
    print("[OK] Successfully scraped Billboard Hot 100 chart")
    print(f"[OK] Extracted {len(songs)} songs with titles and artists")
    
    if playlist_url:
        print("[OK] Created Spotify playlist with found songs")
        print(f"\n[MUSIC] Open your playlist: {playlist_url}")
    else:
        print("[INFO] Spotify credentials not configured")
        print("   You can still view the songs in the text file")
    
    print()
    print("=" * 70)
    print("Key Concepts Demonstrated:")
    print("=" * 70)
    print("""
    1. Beautiful Soup HTML Parsing
       - Finding specific elements by class
       - Extracting text from multiple containers
       - Handling variable HTML structures

    2. Web Scraping Best Practices
       - User-Agent headers for realistic requests
       - Error handling for missing elements
       - Respecting website structure changes

    3. Spotify API Integration
       - OAuth 2.0 authentication
       - Playlist creation and management
       - Searching for tracks
       - Adding tracks to playlists

    4. Data Processing
       - Extracting and transforming data
       - Batch operations for API limits
       - File I/O and data persistence

    5. Error Handling
       - Graceful degradation when services unavailable
       - Informative error messages
       - User guidance for setup

    Music is a time machine that can transport us back to any moment.
    With this project, you've learned to combine web scraping and APIs
    to create meaningful experiences from data!
    """)
    
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
