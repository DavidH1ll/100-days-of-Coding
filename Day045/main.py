"""
Day 45 - Web Scraping with BeautifulSoup
Extract movie data from websites using BeautifulSoup4 and requests

This project demonstrates how to:
1. Request a webpage using the requests library
2. Parse HTML using BeautifulSoup
3. Extract specific data elements from the HTML
4. Organize and display the extracted data
"""

import requests
from bs4 import BeautifulSoup

# ============================================================================
# Example 1: Simple HTML Parsing
# ============================================================================

def example_simple_parsing():
    """Demonstrate basic BeautifulSoup parsing with a simple HTML string"""
    print("=" * 70)
    print("Example 1: Simple HTML Parsing")
    print("=" * 70)
    
    # Sample HTML content
    html_content = """
    <html>
        <head>
            <title>Movie List</title>
        </head>
        <body>
            <h1>Top Movies of All Time</h1>
            <div class="movie-item">
                <h2>Inception</h2>
                <p class="rating">Rating: 8.8/10</p>
                <p class="year">Year: 2010</p>
            </div>
            <div class="movie-item">
                <h2>The Matrix</h2>
                <p class="rating">Rating: 8.7/10</p>
                <p class="year">Year: 1999</p>
            </div>
        </body>
    </html>
    """
    
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract the title
    title = soup.find('title').string
    print(f"\nPage Title: {title}\n")
    
    # Extract all movies
    movies = soup.find_all('div', class_='movie-item')
    print(f"Found {len(movies)} movies:\n")
    
    for i, movie in enumerate(movies, 1):
        movie_name = movie.find('h2').string
        rating = movie.find('p', class_='rating').string
        year = movie.find('p', class_='year').string
        
        print(f"{i}. {movie_name}")
        print(f"   {rating}")
        print(f"   {year}\n")


# ============================================================================
# Example 2: Web Scraping from a Real Website
# ============================================================================

def scrape_movie_data():
    """
    Scrape movie data from a real website
    
    Note: This example uses a public website with no robots.txt restrictions
    Always check a website's terms of service and robots.txt before scraping
    """
    print("=" * 70)
    print("Example 2: Web Scraping Movie Data")
    print("=" * 70)
    
    try:
        # Example: Scraping from a website (using IMDb Top 250 as example)
        # Note: This is educational; always respect website terms of service
        
        url = "https://www.imdb.com/chart/top250/"
        
        print(f"\nAttempting to scrape: {url}\n")
        print("Note: This requires the website to allow scraping.\n")
        
        # Add headers to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Send GET request
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find movie titles (IMDb structure)
        movies = soup.find_all('h3', class_='ipc-title__text')
        
        print(f"Successfully fetched page. Found {len(movies)} movies.\n")
        print("Top 10 Movies:")
        print("-" * 70)
        
        for i, movie in enumerate(movies[:10], 1):
            title = movie.string.strip()
            # Extract ranking number
            rank = title.split('.')[0] if '.' in title else i
            movie_name = title.split('. ', 1)[1] if '. ' in title else title
            
            print(f"{rank}. {movie_name}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        print("Note: Some websites block automated requests.")
        print("This is normal and expected for many websites.\n")


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
    example_simple_parsing()
    print("\n")
    
    scrape_movie_data()
    print("\n")
    
    analyze_local_html()
    print("\n")
    
    advanced_parsing_example()
    
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
