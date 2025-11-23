# Day 046 - Musical Time Machine with Spotify

## Project Overview
Create a personalized Spotify playlist of the top 100 songs from any date in the past 20 years by scraping Billboard's Hot 100 chart and integrating with the Spotify API. This project combines web scraping, data extraction, and API integration to create a nostalgic musical experience.

## Learning Objectives
- Advanced web scraping with Beautiful Soup
- Working with the Spotify Web API
- OAuth 2.0 authentication
- Playlist creation and management
- API rate limiting and batch operations
- Data transformation and processing

## Project Features

### 1. Billboard Hot 100 Scraper
- Fetch chart data for any specific date in the past
- Extract song titles and artist names
- Handle dynamic HTML structures
- Validate data extraction

### 2. Spotify API Integration
- OAuth 2.0 user authentication
- Create personalized playlists
- Search for tracks across Spotify's library
- Add multiple tracks to playlists (batch operations)

### 3. Data Management
- Save song lists to text files
- Display formatted results
- Track success/failure rates
- Provide meaningful user feedback

## Technical Architecture

### Dependencies
```
requests - HTTP library for web scraping
beautifulsoup4 - HTML parsing and extraction
spotipy - Spotify Web API Python library
python-dotenv - Environment variable management (optional)
```

### Installation
```bash
pip install requests beautifulsoup4 spotipy python-dotenv
```

## Key Concepts

### 1. Advanced Web Scraping
**Billboard HTML Structure Analysis:**
```python
# Billboard uses specific class names for chart elements
song_containers = soup.find_all('li', class_='o-chart-results-list__item')

# Extract nested elements
title_element = container.find('h3', class_='c-title')
artist_element = container.find('span', class_='c-label')
```

**Why It Matters**: Websites frequently update their HTML structure. Understanding how to find elements by class and handle failures is crucial for robust scrapers.

**Key Techniques**:
- Find containers first, then extract data within
- Use specific class selectors to target elements
- Implement fallback selectors for alternative HTML structures
- Handle missing elements gracefully

### 2. OAuth 2.0 Authentication
**Understanding the Flow:**
```python
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri='http://localhost:8888/callback',
    scope='playlist-modify-public playlist-modify-private'
)
sp = spotipy.Spotify(auth_manager=sp_oauth)
```

**Why It Matters**: OAuth protects user credentials by using authorization tokens instead of storing passwords. Spotipy handles the complex OAuth flow automatically.

**Key Components**:
- **Client ID/Secret**: App credentials from Spotify Developer Dashboard
- **Redirect URI**: Where Spotify redirects after user approves
- **Scopes**: Permissions your app is requesting (playlist modification, etc.)
- **Access Token**: Used for authenticated API requests

### 3. Spotify API Usage

**Search Functionality:**
```python
# Search with track and artist filters
search_query = f"track:{title} artist:{artist}"
results = sp.search(q=search_query, type='track', limit=1)

if results['tracks']['items']:
    track = results['tracks']['items'][0]
    track_id = track['id']
```

**Why It Matters**: Specific search queries return more accurate results than generic searches.

**Playlist Management:**
```python
# Create playlist
playlist = sp.user_playlist_create(user_id, name, public=True)

# Add tracks (batch operation - max 100 at a time)
sp.playlist_add_items(playlist_id, track_ids)
```

### 4. Batch Operations
**Why Batch**: Spotify API has limits on items per request. Batch operation pattern:
```python
for i in range(0, len(items), 100):
    batch = items[i:i+100]  # Get 100 items
    sp.playlist_add_items(playlist_id, batch)
```

**Benefits**:
- Efficiently handle large datasets
- Respect API rate limits
- Reduce total number of requests
- Better error handling at batch level

### 5. Error Handling Strategy

**Multi-level Error Handling:**
```python
# Level 1: Network errors
except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")

# Level 2: API errors
except spotipy.exceptions.SpotifyException as e:
    print(f"Spotify API error: {e}")

# Level 3: Data parsing errors
except Exception as e:
    print(f"Unexpected error: {e}")
    continue  # Continue with next item
```

**Best Practices**:
- Catch specific exceptions before general ones
- Provide meaningful error messages
- Continue processing when possible
- Log partial successes

## Setup Instructions

### 1. Get Spotify API Credentials
1. Visit https://developer.spotify.com/dashboard
2. Create a new app
3. Accept terms and create app
4. Copy Client ID and Client Secret
5. Set Redirect URI to `http://localhost:8888/callback`

### 2. Configure Environment Variables
**Option A: Set system environment variables**
```powershell
# PowerShell
$env:SPOTIFY_CLIENT_ID = "your_client_id"
$env:SPOTIFY_CLIENT_SECRET = "your_client_secret"
$env:SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
```

**Option B: Use .env file (with python-dotenv)**
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

Then load in Python:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 3. Run the Script
```bash
python main.py
```

## Project Workflow

### Step 1: Scrape Billboard
- User provides a date (or uses default: 2000-12-30)
- Script fetches Billboard chart for that date
- Extracts all 100 songs and artists
- Displays first 10 for preview

### Step 2: Authenticate with Spotify
- Script initiates OAuth flow
- User logs into Spotify in browser
- App receives authorization token
- User profile is loaded

### Step 3: Create Playlist
- New playlist created with date in name
- Playlist description set with date
- Playlist URL retrieved

### Step 4: Search and Add Songs
- Script searches for each song on Spotify
- Track IDs collected for found songs
- Songs added to playlist in batches
- Results summarized (found vs not found)

### Step 5: Save and Share
- Song list saved to text file
- Playlist link displayed
- User can open and share playlist

## Output Example

**Console Output:**
```
🎵 Musical Time Machine - Scraping Billboard Hot 100

📅 Target Date: 2000-12-30
🔗 URL: https://www.billboard.com/charts/hot-100/2000-12-30

📥 Fetching Billboard Hot 100 chart...
✅ Page fetched successfully!

🎵 Top 100 Songs from Billboard Hot 100

  1. Smooth
      by Santana Featuring Rob Thomas
  2. What Makes You Beautiful
      by One Direction
  ...

🎉 Playlist Created Successfully!
🎵 Playlist: 🎵 Time Machine: 2000-12-30
📊 Songs added: 87
🔗 Link: https://open.spotify.com/playlist/...
```

**File Output:** `billboard_hot_100_2000-12-30.txt`

## Common Issues & Solutions

### Issue: "Spotify credentials not configured"
**Cause**: Environment variables not set
**Solution**: 
1. Go to Spotify Developer Dashboard
2. Create app and get credentials
3. Set environment variables as shown in Setup Instructions

### Issue: Some songs not found on Spotify
**Cause**: Songs may be by defunct artists, remixes, or not on Spotify
**Solution**: 
- Script handles this gracefully
- Shows which songs were not found
- Adds all found songs to playlist
- Not a failure - normal for older music

### Issue: HTML parsing fails
**Cause**: Billboard updated their website structure
**Solution**:
- Update CSS selectors in `scrape_billboard_hot_100()`
- Inspect Billboard page with browser DevTools
- Update class names in `find()` calls
- Test with fresh date

### Issue: Rate limiting errors from Spotify
**Cause**: Too many requests in short time
**Solution**:
- Add delays between searches: `time.sleep(0.1)`
- Use batch operations (already implemented)
- Retry with exponential backoff

## Extensions & Enhancements

### 1. Add User Customization
```python
# Let user filter by year range
year = input("Enter year (2000-2024): ")
date_input = f"{year}-01-01"

# Let user specify playlist privacy
is_public = input("Make playlist public? (y/n): ").lower() == 'y'
```

### 2. Advanced Search
```python
# Allow searching by genre, artist, popularity
# Create multiple playlists (one per month in year)
# Add variety with songs from top 50 + hidden gems
```

### 3. Playlist Management
```python
# Update existing playlists instead of creating new
# Merge multiple date playlists
# Create shared playlists for groups
```

### 4. Analytics
```python
# Show decade breakdown
# Analyze artist frequency across decades
# Generate recommendations based on playlist
```

### 5. User Interface
```python
# Create simple web interface with Flask
# Visual timeline of music eras
# Playlist preview with preview audio
```

## Real-World Applications

1. **Anniversary Gifts**: Create playlist from date couple met
2. **Birthday Memories**: Playlist from person's birth year
3. **Milestone Celebrations**: Playlist from significant dates
4. **Educational Tool**: Study music evolution by decade
5. **Nostalgia Marketing**: Recreate historical radio broadcasts
6. **Therapy/Wellness**: Music as memory and emotion aid

## API Reference

### BeautifulSoup Methods Used
| Method | Purpose |
|--------|---------|
| `find_all(tag, class_)` | Find all elements matching criteria |
| `find(tag, class_)` | Find first element matching criteria |
| `get_text(strip=True)` | Extract text content |

### Spotipy Methods Used
| Method | Purpose |
|--------|---------|
| `current_user()` | Get authenticated user info |
| `user_playlist_create()` | Create new playlist |
| `search()` | Search for tracks/artists |
| `playlist_add_items()` | Add tracks to playlist |

## Files Created

```
Day046/
├── main.py                                 # Main application
├── billboard_hot_100_2000-12-30.txt       # Generated song list
└── README.md                               # This file
```

## Best Practices Applied

✅ **Separation of Concerns**: Scraper, API handler, and UI logic separate
✅ **Error Handling**: Multiple levels of error catching and recovery
✅ **User Feedback**: Progress indicators and clear status messages
✅ **Rate Limiting**: Batch operations respect API limits
✅ **Data Validation**: Check HTML structure and API responses
✅ **Credential Security**: Use environment variables, not hardcoding
✅ **Code Documentation**: Docstrings explain purpose and parameters
✅ **Graceful Degradation**: Works even if Spotify unavailable

## Skills Demonstrated

✅ Advanced web scraping with dynamic websites
✅ OAuth 2.0 authentication flow
✅ RESTful API integration
✅ Data transformation and processing
✅ Batch operations and rate limiting
✅ Multi-level error handling
✅ File I/O and data persistence
✅ User interaction and input validation
✅ Environment variable management
✅ API response parsing and navigation

## Summary

Day 046 teaches how to combine multiple technologies (web scraping, APIs, authentication) to create a meaningful application. The Musical Time Machine demonstrates that code can do more than process data—it can create experiences and evoke memories through music. By learning these integration patterns, you've gained skills applicable to countless real-world projects that combine multiple services and APIs.

The project emphasizes the importance of understanding how different systems communicate, handling failures gracefully, and creating user-centric applications that provide value beyond raw functionality.

