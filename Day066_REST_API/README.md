# Day 66 - Build Your Own REST API Service

## 🎯 Project Goal

Learn how to create a complete REST API from scratch using Flask. Build an API service that provides access to cafe data (remote-work friendly cafes with WiFi, power outlets, and coffee prices) that other developers can consume.

---

## 🌐 What is a REST API?

**REST** (Representational State Transfer) is an architectural style for building APIs that uses HTTP methods to perform operations on resources.

### HTTP Methods (CRUD Operations)

| HTTP Method | CRUD Operation | Purpose | Example |
|-------------|----------------|---------|---------|
| **GET** | Read | Retrieve data | Get all cafes |
| **POST** | Create | Add new data | Add new cafe |
| **PUT/PATCH** | Update | Modify existing data | Update cafe price |
| **DELETE** | Delete | Remove data | Delete closed cafe |

### RESTful Principles

1. **Resource-Based URLs**: `/cafes`, `/cafes/42`
2. **HTTP Methods**: Use appropriate HTTP verbs
3. **Stateless**: Each request is independent
4. **JSON Format**: Data exchanged in JSON
5. **Status Codes**: Proper HTTP status codes (200, 201, 404, 403)

---

## 🏗️ API Architecture

### Database Model

```python
class Cafe(db.Model):
    id: int                  # Primary key
    name: str                # Cafe name
    map_url: str             # Google Maps link
    img_url: str             # Image URL
    location: str            # Area/neighborhood
    seats: str               # Seating capacity
    has_toilet: bool         # Restroom availability
    has_wifi: bool           # WiFi availability
    has_sockets: bool        # Power outlet availability
    can_take_calls: bool     # Phone call friendly
    coffee_price: str        # Coffee price
```

### Endpoints Overview

```
📍 API Endpoints:

PUBLIC (No authentication):
├── GET    /                       → API documentation homepage
├── GET    /random                 → Get random cafe
├── GET    /all                    → Get all cafes
├── GET    /search?loc={location}  → Search cafes by location
└── POST   /add                    → Add new cafe

SECURED (API key required):
├── PATCH  /update-price/{id}      → Update coffee price
└── DELETE /report-closed/{id}     → Delete cafe
```

---

## 📚 API Endpoints Documentation

### 1. GET /random - Get Random Cafe

**Purpose**: Retrieve a random cafe from the database

**Request**:
```http
GET /random HTTP/1.1
Host: 127.0.0.1:5000
```

**Response** (200 OK):
```json
{
  "cafe": {
    "id": 1,
    "name": "Science Cafe",
    "map_url": "https://goo.gl/maps/RLZq4JnzaCdZCqrX7",
    "img_url": "https://example.com/cafe.jpg",
    "location": "Peckham",
    "seats": "20-30",
    "has_toilet": true,
    "has_wifi": true,
    "has_sockets": true,
    "can_take_calls": false,
    "coffee_price": "£2.50"
  }
}
```

---

### 2. GET /all - Get All Cafes

**Purpose**: Retrieve all cafes from the database (sorted by name)

---

### 3. GET /search - Search Cafes by Location

**Purpose**: Find cafes in a specific area/neighborhood

**Request**:
```http
GET /search?loc=Peckham HTTP/1.1
```

---

### 4. POST /add - Add New Cafe

**Purpose**: Add a new cafe to the database

**Required Form Data**:
- `name`, `map_url`, `img_url`, `location`, `seats`
- `has_toilet`, `has_wifi`, `has_sockets`, `can_take_calls`
- `coffee_price`

---

### 5. PATCH /update-price/{cafe_id} - Update Coffee Price 🔒

**Authentication**: Requires API key `TopSecretAPIKey`

**Request**:
```http
PATCH /update-price/42?new_price=£3.50&api-key=TopSecretAPIKey
```

---

### 6. DELETE /report-closed/{cafe_id} - Delete Cafe 🔒

**Authentication**: Requires API key

---

## 🚀 Getting Started

```bash
cd "/mnt/storage/Visual Studio Projects/100 days of Coding/Day066"
pip install -r requirements.txt
python main.py
```

Open: http://127.0.0.1:5000

---

## 🧪 Testing the API

### Using cURL

```bash
# Get random cafe
curl http://127.0.0.1:5000/random

# Get all cafes
curl http://127.0.0.1:5000/all

# Search by location
curl "http://127.0.0.1:5000/search?loc=Peckham"

# Add new cafe
curl -X POST http://127.0.0.1:5000/add \
  -d "name=Test Cafe" \
  -d "location=London" \
  -d "coffee_price=£2.50" \
  ... (all required fields)

# Update price (with API key)
curl -X PATCH "http://127.0.0.1:5000/update-price/1?new_price=£3.50&api-key=TopSecretAPIKey"

# Delete cafe (with API key)
curl -X DELETE "http://127.0.0.1:5000/report-closed/1?api-key=TopSecretAPIKey"
```

### Using Postman

1. Create new requests for each endpoint
2. Set HTTP method (GET, POST, PATCH, DELETE)
3. Add required parameters/body data
4. Include API key for secured endpoints

---

## 🧠 Key Concepts Learned

### 1. REST Architecture

- Resource-based URLs
- HTTP methods for actions
- Proper status codes (200, 201, 400, 403, 404)

### 2. Database to JSON Serialization

```python
def to_dict(self):
    return {column.name: getattr(self, column.name) 
            for column in self.__table__.columns}
```

### 3. Query Parameters vs URL Parameters

**URL Parameters**: `/update-price/<int:cafe_id>`  
**Query Parameters**: `?new_price=£3.50&api-key=TopSecretAPIKey`

### 4. HTTP Methods in Flask

```python
@app.route("/add", methods=["POST"])
@app.route("/update", methods=["PATCH"])
@app.route("/delete", methods=["DELETE"])
```

### 5. API Authentication

```python
api_key = request.args.get("api-key")
if api_key != API_KEY:
    return jsonify(error="Unauthorized"), 403
```

---

## 💰 Monetization Strategies

### How to Charge for Your API

1. **Freemium Model**: Free tier + paid unlimited
2. **Per-Request Pricing**: $0.001 per API call
3. **Subscription Plans**: $9-$99/month
4. **Feature-Based**: Free read, paid write

---

## 🚀 Extension Ideas

**Beginner**:
- Add more fields (hours, price range, noise level)
- Add filtering (has_wifi=true)
- Add sorting (sort=price)

**Intermediate**:
- Pagination (page=1&per_page=10)
- Rate limiting
- Advanced search

**Advanced**:
- User authentication (JWT)
- Usage analytics dashboard
- API versioning (/v1/, /v2/)

---

## ✅ Project Checklist

- [x] GET endpoints for reading data
- [x] POST endpoint for creating data
- [x] PATCH endpoint for updating data
- [x] DELETE endpoint for deleting data
- [x] API key authentication
- [x] Proper HTTP status codes
- [x] JSON response format
- [x] Error handling
- [x] Interactive documentation

---

## 🎉 Conclusion

You've built a complete REST API demonstrating:

- **RESTful Architecture**: HTTP methods and status codes
- **Database Integration**: Full CRUD with SQLAlchemy
- **Security**: API key authentication
- **Documentation**: Professional API docs
- **Scalability**: Foundation for monetization

You now understand how companies provide API services and can create your own!

**Happy API Building! 🚀**
