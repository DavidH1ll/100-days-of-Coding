"""
Day 45 - Scraping and Saving the Top 100 Movies List
Extract the top 100 greatest movies of all time from Empire Magazine
and save them to a text file in order from 1 to 100.

Project Goals:
1. Use requests to fetch the Empire top 100 movies webpage
2. Use BeautifulSoup to parse the HTML structure
3. Extract all movie titles from <h3 class='title'> elements
4. Reverse the list (since it's ordered 100 to 1, not 1 to 100)
5. Save the movies to a text file (movies.txt)
"""

import requests
from bs4 import BeautifulSoup
import os

# Empire's Top 100 Greatest Movies of All Time
# Note: This URL may change, check course resources for the current URL
URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_FILE = os.path.join(SCRIPT_DIR, 'movies.txt')

# ============================================================================
# Main Scraper Function
# ============================================================================

def scrape_top_100_movies():
    """
    Scrape the Empire top 100 movies list from the website
    and save it to a text file.
    """
    print("=" * 70)
    print("Day 45: Scraping Top 100 Greatest Movies")
    print("=" * 70)
    print()
    
    try:
        print("📥 Fetching webpage...")
        # Make a GET request to the website
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        print("✅ Page fetched successfully!\n")
        
        # Get the raw HTML content
        website_html = response.text
        
        print("🔍 Parsing HTML with BeautifulSoup...")
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(website_html, 'html.parser')
        
        print("✅ HTML parsed successfully!\n")
        
        print("🎬 Searching for movie titles...")
        # Find all movie titles - they are in <h3> tags with class 'title'
        all_movies = soup.find_all('h3', class_='title')
        
        print(f"✅ Found {len(all_movies)} movies!\n")
        
        if len(all_movies) == 0:
            print("⚠️  Warning: No movies found. The website structure may have changed.")
            print("Please verify the URL and HTML structure.\n")
            return False
        
        print("📝 Extracting movie titles...")
        # Extract just the text from each h3 element using getText()
        movie_titles = [movie.getText().strip() for movie in all_movies]
        
        print(f"✅ Extracted {len(movie_titles)} movie titles!\n")
        
        # Display first 5 and last 5 movies to verify extraction
        print("First 5 movies (before reversal - should be 100-96):")
        for i, movie in enumerate(movie_titles[:5], 1):
            print(f"  {i}. {movie}")
        
        print("\nLast 5 movies (before reversal - should be 5-1):")
        for i, movie in enumerate(movie_titles[-5:], len(movie_titles) - 4):
            print(f"  {i}. {movie}")
        print()
        
        print("🔄 Reversing the list (currently 100→1, need 1→100)...")
        # Reverse the list so it starts from 1 instead of 100
        # Using slice notation [::-1] to reverse the entire list
        movies = movie_titles[::-1]
        
        print("✅ List reversed!\n")
        
        # Verify reversal
        print("After reversal - First 5 movies (should now be 1-5):")
        for i, movie in enumerate(movies[:5], 1):
            print(f"  {i}. {movie}")
        
        print("\nAfter reversal - Last 5 movies (should now be 96-100):")
        for i, movie in enumerate(movies[-5:], len(movies) - 4):
            print(f"  {i}. {movie}")
        print()
        
        print("💾 Writing movies to movies.txt...")
        # Write the movies to a text file in write mode
        with open(MOVIES_FILE, 'w', encoding='utf-8') as file:
            for movie in movies:
                file.write(movie + '\n')
        
        print("✅ Successfully saved to movies.txt!\n")
        
        print("=" * 70)
        print("Project Complete! 🎉")
        print("=" * 70)
        print(f"\n✅ Saved {len(movies)} movies to '{MOVIES_FILE}'")
        print("\nYou can now:")
        print("  • Open movies.txt to view the complete list")
        print("  • Watch movies and cross them off the list")
        print("  • Pick a random movie to watch next")
        print("\nNote: There is a known typo at #93 in the original Empire list.\n")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching the website: {e}")
        print("This website may block automated requests or the URL may have changed.")
        print("Please check the course resources for the current URL.\n")
        return False
    except Exception as e:
        print(f"\n❌ An error occurred: {e}\n")
        return False


# ============================================================================
# Educational Example
# ============================================================================

def demonstrate_scraping_concepts():
    """
    Demonstrate key BeautifulSoup and web scraping concepts
    using a local HTML example.
    """
    print("\n" + "=" * 70)
    print("Educational Example: How Web Scraping Works")
    print("=" * 70 + "\n")
    
    # Example HTML - simulating a simple movie list
    example_html = """
    <html>
        <body>
            <div class="movies">
                <h3 class="title">100. Movie Name Here</h3>
                <h3 class="title">99. Another Movie</h3>
                <h3 class="title">98. Third Movie</h3>
            </div>
        </body>
    </html>
    """
    
    print("Step 1: Parse HTML with BeautifulSoup")
    print("-" * 70)
    soup = BeautifulSoup(example_html, 'html.parser')
    print("✓ HTML parsed\n")
    
    print("Step 2: Find all <h3> elements with class='title'")
    print("-" * 70)
    all_movies = soup.find_all('h3', class_='title')
    print(f"✓ Found {len(all_movies)} elements\n")
    
    print("Step 3: Extract text using getText()")
    print("-" * 70)
    movie_titles = [movie.getText() for movie in all_movies]
    for i, title in enumerate(movie_titles, 1):
        print(f"  {i}. {title}")
    print()
    
    print("Step 4: Reverse the list using [::-1]")
    print("-" * 70)
    reversed_movies = movie_titles[::-1]
    for i, title in enumerate(reversed_movies, 1):
        print(f"  {i}. {title}")
    print()
    
    print("Step 5: Write to file")
    print("-" * 70)
    print("with open('movies.txt', 'w') as file:")
    print("    for movie in reversed_movies:")
    print("        file.write(movie + '\\n')")
    print("✓ File created\n")


# ============================================================================
# Example 3: Local Website Analysis
# ============================================================================

def analyze_local_html():
    """Analyze HTML structure and extract nested elements"""
    print("=" * 70)
    print("Example 3: HTML Structure Analysis")
    print("=" * 70)
    
    html_content = """
    <html>
        <body>
            <section class="top-movies">
                <h1>Empire's 100 Greatest Movies</h1>
                <ul class="movie-list">
                    <li>
                        <span class="rank">#1</span>
                        <span class="title">The Godfather</span>
                        <span class="year">(1972)</span>
                    </li>
                    <li>
                        <span class="rank">#2</span>
                        <span class="title">The Shawshank Redemption</span>
                        <span class="year">(1994)</span>
                    </li>
                    <li>
                        <span class="rank">#3</span>
                        <span class="title">The Godfather Part II</span>
                        <span class="year">(1974)</span>
                    </li>
                    <li>
                        <span class="rank">#4</span>
                        <span class="title">Pulp Fiction</span>
                        <span class="year">(1994)</span>
                    </li>
                    <li>
                        <span class="rank">#5</span>
                        <span class="title">Forrest Gump</span>
                        <span class="year">(1994)</span>
                    </li>
                </ul>
            </section>
        </body>
    </html>
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the main heading
    heading = soup.find('h1').string
    print(f"\n{heading}\n")
    
    # Find all list items
    movies = soup.find_all('li')
    print(f"Found {len(movies)} movies:\n")
    
    # Extract data from each movie
    movie_list = []
    for movie_li in movies:
        rank = movie_li.find('span', class_='rank').string
        title = movie_li.find('span', class_='title').string
        year = movie_li.find('span', class_='year').string
        
        movie_data = {
            'rank': rank,
            'title': title,
            'year': year
        }
        movie_list.append(movie_data)
        
        print(f"{rank} - {title} {year}")
    
    return movie_list


# ============================================================================
# Example 4: CSS Selectors and Advanced Parsing
# ============================================================================

def advanced_parsing_example():
    """Demonstrate advanced BeautifulSoup techniques using CSS selectors"""
    print("=" * 70)
    print("Example 4: Advanced Parsing with CSS Selectors")
    print("=" * 70)
    
    html_content = """
    <div class="container">
        <article class="movie-review">
            <header>
                <h2 class="movie-title">Inception</h2>
                <span class="director">Christopher Nolan</span>
            </header>
            <div class="metadata">
                <span class="year">2010</span>
                <span class="runtime">148 min</span>
                <span class="rating">★★★★★ (8.8/10)</span>
            </div>
            <p class="summary">A mind-bending sci-fi thriller about dreams within dreams.</p>
        </article>
    </div>
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    print("\nUsing CSS Selectors:\n")
    
    # Use select() method with CSS selectors
    title = soup.select_one('h2.movie-title').string
    director = soup.select_one('.director').string
    
    # Get metadata spans
    year_elem = soup.select_one('span.year')
    runtime_elem = soup.select_one('span.runtime')
    rating_elem = soup.select_one('span.rating')
    
    summary = soup.select_one('p.summary').string
    
    year = year_elem.string if year_elem else "N/A"
    runtime = runtime_elem.string if runtime_elem else "N/A"
    rating = rating_elem.string if rating_elem else "N/A"
    
    print(f"Title: {title}")
    print(f"Director: {director}")
    print(f"Year: {year}")
    print(f"Runtime: {runtime}")
    print(f"Rating: {rating}")
    print(f"Summary: {summary}\n")


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "Day 45 - Web Scraping with BeautifulSoup" + " " * 11 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # Run examples
    demonstrate_scraping_concepts()
    print("\n")
    
    scrape_top_100_movies()
    
    # Summary
    print("=" * 70)
    print("Key BeautifulSoup Methods Demonstrated:")
    print("=" * 70)
    print("""
    1. BeautifulSoup(html, 'html.parser')
       - Creates a BeautifulSoup object from HTML content
    
    2. soup.find(tag, class_='classname')
       - Finds the first matching element
    
    3. soup.find_all(tag, class_='classname')
       - Finds all matching elements (returns a list)
    
    4. element.string
       - Gets the text content of an element
    
    5. soup.select('css.selector')
       - Uses CSS selectors to find elements
    
    6. soup.select_one('css.selector')
       - Uses CSS selectors to find first element
    
    Web Scraping Best Practices:
    ✓ Always check robots.txt before scraping
    ✓ Respect website terms of service
    ✓ Add user-agent headers to avoid blocking
    ✓ Use delays between requests to avoid overloading servers
    ✓ Store data responsibly
    ✓ Never scrape personal or sensitive data
    """)
    print("=" * 70)


if __name__ == "__main__":
    main()
