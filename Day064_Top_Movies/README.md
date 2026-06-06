# Day 64 - Top 10 Movies Website with Ranking System

A beautiful Flask web application with SQLite database that manages your top 10 favorite movies with automatic ranking based on ratings.

## 🎯 Key Feature - Automatic Ranking System

**Requirement 5 Completed:** Movies are automatically ranked from 1-10 based on their ratings (highest to lowest).

### How Ranking Works

1. **Query movies ordered by rating (descending)**
2. **Convert ScalarResult to Python list**
3. **Enumerate through list and assign rankings**
4. **Highest rating gets #1, lowest gets last position**

### Example Scenarios

**Scenario 1:** Two movies
- The Matrix (9.2) → Rank #2
- Spirited Away (9.5) → Rank #1

**Scenario 2:** Three movies added
- The Matrix (9.3) → Rank #2
- Spirited Away (9.5) → Rank #3
- Parasite (9.9) → Rank #1

**Scenario 3:** After editing ratings
- The Matrix (9.3) → Rank #2
- Spirited Away (9.5) → Rank #1
- Parasite (8.9) → Rank #3

Rankings update automatically whenever you view the home page!

## ✨ Features

- 🎬 **Movie Collection** - Store your favorite movies
- ⭐ **Rating System** - Rate movies from 0-10
- 🏆 **Automatic Ranking** - Rankings based on ratings (highest = #1)
- ✏️ **Edit Ratings** - Update ratings and reviews anytime
- 🗑️ **Delete Movies** - Remove movies from your list
- 🎨 **Beautiful UI** - Movie card design with poster images
- 📱 **Responsive** - Works on all devices

## 📁 Project Structure

```
Day064/
├── main.py                    # Flask app with ranking logic
├── instance/
│   └── movies.db             # SQLite database
├── templates/
│   ├── index.html            # Home page with ranked movies
│   ├── add.html              # Add new movie form
│   └── edit.html             # Edit rating/review form
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

### 3. Access the App

Visit `http://127.0.0.1:5000` in your browser.

## 💾 Database Structure

### Movie Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| title | String(250) | Unique, Not Null |
| year | Integer | Not Null |
| description | String(500) | Not Null |
| rating | Float | Nullable |
| ranking | Integer | Nullable |
| review | String(250) | Nullable |
| img_url | String(250) | Not Null |

## 🏆 Ranking System Implementation

### The Core Logic (home() function)

```python
@app.route("/")
def home():
    # READ ALL RECORDS - Ordered by rating (highest first)
    result = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
    all_movies = result.scalars().all()  # Convert ScalarResult to Python List
    
    # Assign rankings based on position in sorted list
    for i, movie in enumerate(all_movies):
        movie.ranking = i + 1
    
    db.session.commit()
    
    return render_template("index.html", movies=all_movies)
```

### Step-by-Step Breakdown

#### Step 1: Query with ORDER BY
```python
result = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
```

- `db.select(Movie)` - Creates SELECT query
- `.order_by(Movie.rating.desc())` - Orders by rating, highest first
- `desc()` - Descending order (10, 9, 8, 7...)
- Returns a `Result` object

#### Step 2: Convert to Python List
```python
all_movies = result.scalars().all()
```

- `.scalars()` - Extracts scalar values (Movie objects)
- `.all()` - Converts ScalarResult to Python list
- Now we have: `[Movie1, Movie2, Movie3]` ordered by rating

#### Step 3: Assign Rankings
```python
for i, movie in enumerate(all_movies):
    movie.ranking = i + 1
```

- `enumerate(all_movies)` - Gets index and movie
- Index starts at 0, so we add 1
- First movie (highest rating) gets ranking = 1
- Second movie gets ranking = 2, etc.

#### Step 4: Save to Database
```python
db.session.commit()
```

- Saves the updated rankings to database
- Rankings persist until next calculation

### Why This Works

1. **Always sorts by rating first** - Ensures correct order
2. **Enumerate preserves order** - Index matches sorted position
3. **Dynamic calculation** - Recalculates on every home page visit
4. **No manual intervention** - Fully automatic

### Alternative Approaches

**Option 1: Without saving to DB**
```python
for i, movie in enumerate(all_movies):
    movie.ranking = i + 1
# Don't commit - ranking only exists in memory
```

**Option 2: Using list comprehension**
```python
movies_with_rank = [(i+1, movie) for i, movie in enumerate(all_movies)]
```

**Option 3: Reverse order for ascending**
```python
# If you want lowest rating = #1
result = db.session.execute(db.select(Movie).order_by(Movie.rating.asc()))
```

## 🎨 UI Design

### Movie Card Features

- **Front Side:**
  - Large ranking number (top left)
  - Movie poster as background
  - Title and rating at bottom
  - Delete button (top right)

- **Back Side:**
  - Movie description
  - User review (if added)
  - "Update Rating" button

### Visual Hierarchy

```
#1 ⭐ 9.9/10  (Highest rated - Top position)
#2 ⭐ 9.5/10
#3 ⭐ 9.3/10
#4 ⭐ 8.9/10  (Lower rated - Bottom position)
```

## 🔧 CRUD Operations

### CREATE - Add Movie
```python
new_movie = Movie(
    title=..., year=..., description=...,
    rating=..., review=..., img_url=...
)
db.session.add(new_movie)
db.session.commit()
```

### READ - Get Ranked Movies
```python
result = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
all_movies = result.scalars().all()
```

### UPDATE - Edit Rating
```python
movie_to_update = db.get_or_404(Movie, movie_id)
movie_to_update.rating = new_rating
movie_to_update.review = new_review
db.session.commit()
# Ranking recalculates on next home page view
```

### DELETE - Remove Movie
```python
movie_to_delete = db.get_or_404(Movie, movie_id)
db.session.delete(movie_to_delete)
db.session.commit()
# Rankings auto-adjust for remaining movies
```

## 📊 How Rankings Update

### Scenario Walkthrough

**Initial State: Empty Database**
```
No movies yet
```

**Add Movie 1: The Matrix (9.2)**
```
Home page loads → Queries by rating DESC → Assigns rank
Result: #1 The Matrix (9.2)
```

**Add Movie 2: Spirited Away (9.5)**
```
Home page loads → Queries by rating DESC
Order: [Spirited Away (9.5), The Matrix (9.2)]
Assign ranks: enumerate([Movie1, Movie2])
Result:
  #1 Spirited Away (9.5)  ← Higher rating
  #2 The Matrix (9.2)
```

**Add Movie 3: Parasite (9.9)**
```
Home page loads → Queries by rating DESC
Order: [Parasite (9.9), Spirited Away (9.5), Matrix (9.2)]
Assign ranks: enumerate([Movie1, Movie2, Movie3])
Result:
  #1 Parasite (9.9)       ← Highest
  #2 Spirited Away (9.5)
  #3 The Matrix (9.2)
```

**Edit Parasite Rating to 8.9**
```
Submit edit form → Rating changes to 8.9
Return to home → Queries by rating DESC
New Order: [Spirited Away (9.5), Matrix (9.2), Parasite (8.9)]
Assign ranks: enumerate([Movie1, Movie2, Movie3])
Result:
  #1 Spirited Away (9.5)  ← Now highest
  #2 The Matrix (9.2)
  #3 Parasite (8.9)       ← Moved down
```

## 🧪 Testing the Ranking System

### Test 1: Add Movies in Random Order
1. Add "Movie C" (rating 7.0)
2. Add "Movie A" (rating 9.0)
3. Add "Movie B" (rating 8.0)
4. Go to home page
5. **Expected:** #1 Movie A, #2 Movie B, #3 Movie C

### Test 2: Edit to Change Ranking
1. Have 3 movies with different ratings
2. Edit the #3 movie to have highest rating
3. Return to home
4. **Expected:** Previously #3 movie is now #1

### Test 3: Delete Highest Ranked
1. Have 3 movies
2. Delete #1 ranked movie
3. Return to home
4. **Expected:** #2 becomes #1, #3 becomes #2

### Test 4: Tie Ratings
1. Add two movies with same rating (e.g., 8.5)
2. **Expected:** Both will have consecutive ranks
3. Order determined by database ID or title

## 💡 Key Learning Points

### 1. SQLAlchemy order_by()
```python
.order_by(Movie.rating.desc())  # Descending (10→1)
.order_by(Movie.rating.asc())   # Ascending (1→10)
.order_by(Movie.title)          # Alphabetical
```

### 2. Converting Query Results
```python
result = db.session.execute(query)  # Result object
scalars = result.scalars()          # ScalarResult object
list = result.scalars().all()       # Python list
```

### 3. Enumerate for Ranking
```python
for index, item in enumerate(list):
    # index: 0, 1, 2, 3...
    # ranking: 1, 2, 3, 4... (index + 1)
```

### 4. Dynamic Property Assignment
```python
movie.ranking = i + 1  # Modifies object property
db.session.commit()    # Saves to database
```

## 🐛 Troubleshooting

### Rankings Don't Update
**Problem:** Rankings show old values  
**Solution:** Ensure `db.session.commit()` is called after assignment

### All Movies Show Same Rank
**Problem:** Ranking not assigned in loop  
**Solution:** Check `enumerate()` loop and `movie.ranking = i + 1`

### Movies Not Sorted by Rating
**Problem:** Order seems random  
**Solution:** Verify `.order_by(Movie.rating.desc())` in query

### None Shows Instead of Number
**Problem:** Ranking displays "None"  
**Solution:** 
- Check ranking is assigned before rendering
- Ensure template uses `{{ movie.ranking }}`

## 🌟 Enhancements

### 1. Genre-Based Ranking
```python
top_action = Movie.query.filter_by(genre='Action').order_by(Movie.rating.desc()).all()
```

### 2. Year-Based Ranking
```python
.order_by(Movie.year.desc(), Movie.rating.desc())  # Newest first, then by rating
```

### 3. Custom Ranking Criteria
```python
# Weighted score: rating * 10 + year_score
movie.rank_score = movie.rating * 10 + (movie.year - 1900) * 0.1
.order_by(Movie.rank_score.desc())
```

### 4. Top N Only
```python
top_10 = db.session.execute(
    db.select(Movie).order_by(Movie.rating.desc()).limit(10)
).scalars().all()
```

## 📚 Technologies Used

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM
- **SQLite** - Database
- **HTML5/CSS3** - Frontend
- **Font Awesome** - Icons

## 🎉 Project Complete!

Successfully implemented:
- ✅ Automatic ranking system
- ✅ Dynamic recalculation on page load
- ✅ Order by rating (descending)
- ✅ Convert Result to list
- ✅ Enumerate to assign rankings
- ✅ Beautiful movie card UI
- ✅ Full CRUD operations

The ranking number (1-10) now displays prominently on each movie card! 🏆
