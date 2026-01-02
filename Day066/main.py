"""
Day 66 - Build Your Own REST API Service
==========================================

This REST API provides access to cafe data, including information about
remote-work friendly cafes with WiFi, power outlets, and coffee prices.

API Endpoints:
- GET  /random           - Get a random cafe
- GET  /all              - Get all cafes
- GET  /search?loc=<location> - Search cafes by location
- POST /add              - Add a new cafe (requires parameters)
- PATCH /update-price/<cafe_id> - Update coffee price (requires API key)
- DELETE /report-closed/<cafe_id> - Delete a cafe (requires API key)
"""

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# API Key for secured endpoints
API_KEY = "TopSecretAPIKey"


# ==================== DATABASE MODEL ====================

class Cafe(db.Model):
    """Database model for Cafe with all remote-work related information."""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        """Convert Cafe object to dictionary for JSON serialization."""
        # Method 1: Using dictionary comprehension
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
        
        # Method 2: Manual dictionary creation (alternative)
        # return {
        #     "id": self.id,
        #     "name": self.name,
        #     "map_url": self.map_url,
        #     "img_url": self.img_url,
        #     "location": self.location,
        #     "seats": self.seats,
        #     "has_toilet": self.has_toilet,
        #     "has_wifi": self.has_wifi,
        #     "has_sockets": self.has_sockets,
        #     "can_take_calls": self.can_take_calls,
        #     "coffee_price": self.coffee_price,
        # }


# Create tables (only needs to run once)
with app.app_context():
    db.create_all()


# ==================== ROUTES ====================

@app.route("/")
def home():
    """Render API documentation homepage."""
    return render_template("index.html")


# ==================== HTTP GET - Read Records ====================

@app.route("/random")
def get_random_cafe():
    """
    GET a random cafe from the database.
    
    Returns:
        JSON: Random cafe object
    
    Example Response:
        {
            "cafe": {
                "id": 1,
                "name": "Science Cafe",
                "map_url": "https://goo.gl/maps/...",
                "img_url": "https://example.com/image.jpg",
                "location": "Peckham",
                "seats": "20-30",
                "has_toilet": true,
                "has_wifi": true,
                "has_sockets": true,
                "can_take_calls": false,
                "coffee_price": "£2.50"
            }
        }
    """
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    
    if all_cafes:
        random_cafe = random.choice(all_cafes)
        return jsonify(cafe=random_cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "No cafes in database."}), 404


@app.route("/all")
def get_all_cafes():
    """
    GET all cafes from the database.
    
    Returns:
        JSON: List of all cafe objects
    
    Example Response:
        {
            "cafes": [
                {
                    "id": 1,
                    "name": "Science Cafe",
                    ...
                },
                {
                    "id": 2,
                    "name": "Lighthaus",
                    ...
                }
            ]
        }
    """
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    
    # Convert list of Cafe objects to list of dictionaries
    cafes_list = [cafe.to_dict() for cafe in all_cafes]
    
    return jsonify(cafes=cafes_list)


@app.route("/search")
def search_cafe():
    """
    GET cafes by location query parameter.
    
    Query Parameters:
        loc (str): Location to search for (e.g., ?loc=Peckham)
    
    Returns:
        JSON: List of cafes in that location or error message
    
    Example Request:
        GET /search?loc=Peckham
    
    Example Response (Success):
        {
            "cafes": [
                {
                    "id": 1,
                    "name": "Science Cafe",
                    "location": "Peckham",
                    ...
                }
            ]
        }
    
    Example Response (Not Found):
        {
            "error": {
                "Not Found": "Sorry, we don't have a cafe at that location."
            }
        }
    """
    # Get query parameter 'loc' from URL
    query_location = request.args.get("loc")
    
    # Search database for cafes in that location (case-insensitive)
    result = db.session.execute(
        db.select(Cafe).where(Cafe.location == query_location)
    )
    all_cafes = result.scalars().all()
    
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={
            "Not Found": "Sorry, we don't have a cafe at that location."
        }), 404


# ==================== HTTP POST - Create Record ====================

@app.route("/add", methods=["POST"])
def add_cafe():
    """
    POST a new cafe to the database.
    
    Required Form Data:
        - name: Cafe name (str)
        - map_url: Google Maps URL (str)
        - img_url: Image URL (str)
        - location: Location/area (str)
        - seats: Number of seats (str, e.g., "20-30")
        - has_toilet: Toilet availability (bool, "True"/"False")
        - has_wifi: WiFi availability (bool)
        - has_sockets: Power socket availability (bool)
        - can_take_calls: Phone call friendly (bool)
        - coffee_price: Coffee price (str, e.g., "£2.50")
    
    Returns:
        JSON: Success message or error
    
    Example Request (POST form data):
        name=TestCafe
        map_url=https://goo.gl/maps/test
        img_url=https://example.com/test.jpg
        location=TestLocation
        seats=50+
        has_toilet=True
        has_wifi=True
        has_sockets=True
        can_take_calls=False
        coffee_price=£3.00
    
    Example Response (Success):
        {
            "response": {
                "success": "Successfully added the new cafe."
            }
        }
    """
    try:
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            seats=request.form.get("seats"),
            has_toilet=bool(request.form.get("has_toilet")),
            has_wifi=bool(request.form.get("has_wifi")),
            has_sockets=bool(request.form.get("has_sockets")),
            can_take_calls=bool(request.form.get("can_take_calls")),
            coffee_price=request.form.get("coffee_price"),
        )
        
        db.session.add(new_cafe)
        db.session.commit()
        
        return jsonify(response={
            "success": "Successfully added the new cafe."
        }), 201  # 201 Created status code
        
    except Exception as e:
        return jsonify(error={
            "Bad Request": f"Failed to add cafe. {str(e)}"
        }), 400


# ==================== HTTP PATCH - Update Record ====================

@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    """
    PATCH (update) the coffee price for a specific cafe.
    
    URL Parameters:
        cafe_id (int): The ID of the cafe to update
    
    Query Parameters:
        new_price (str): The new coffee price (e.g., ?new_price=£3.50)
    
    Headers Required:
        api-key: Your API key for authentication
    
    Returns:
        JSON: Success message or error
    
    Example Request:
        PATCH /update-price/42?new_price=£3.50
        Headers: api-key: TopSecretAPIKey
    
    Example Response (Success):
        {
            "response": {
                "success": "Successfully updated the price."
            }
        }
    
    Example Response (Not Found):
        {
            "error": {
                "Not Found": "Sorry, a cafe with that id was not found in the database."
            }
        }
    
    Example Response (Forbidden):
        {
            "error": "Sorry, that's not allowed. Make sure you have the correct api_key."
        }
    """
    # Check API key authentication
    if request.args.get("api-key") != API_KEY:
        return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api_key."), 403
    
    # Get new price from query parameter
    new_price = request.args.get("new_price")
    
    # Find cafe by ID
    cafe = db.session.get(Cafe, cafe_id)
    
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        return jsonify(error={
            "Not Found": "Sorry, a cafe with that id was not found in the database."
        }), 404


# ==================== HTTP DELETE - Delete Record ====================

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    """
    DELETE a cafe from the database (report it as closed).
    
    URL Parameters:
        cafe_id (int): The ID of the cafe to delete
    
    Query Parameters:
        api-key (str): Your API key for authentication
    
    Returns:
        JSON: Success message or error
    
    Example Request:
        DELETE /report-closed/42?api-key=TopSecretAPIKey
    
    Example Response (Success):
        {
            "response": {
                "success": "Successfully deleted the cafe."
            }
        }
    
    Example Response (Not Found):
        {
            "error": {
                "Not Found": "Sorry, a cafe with that id was not found in the database."
            }
        }
    
    Example Response (Forbidden):
        {
            "error": "Sorry, that's not allowed. Make sure you have the correct api_key."
        }
    """
    # Check API key authentication
    api_key = request.args.get("api-key")
    
    if api_key != API_KEY:
        return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api_key."), 403
    
    # Find cafe by ID
    cafe = db.session.get(Cafe, cafe_id)
    
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe."}), 200
    else:
        return jsonify(error={
            "Not Found": "Sorry, a cafe with that id was not found in the database."
        }), 404


# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    app.run(debug=True)
