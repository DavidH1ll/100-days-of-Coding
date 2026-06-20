import os

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "shop-secret-key")

PRODUCTS = [
    {
        "id": 1,
        "name": "Wireless Headphones",
        "price": 79.99,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300",
        "category": "Electronics",
    },
    {
        "id": 2,
        "name": "Mechanical Keyboard",
        "price": 129.99,
        "image": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=300",
        "category": "Electronics",
    },
    {
        "id": 3,
        "name": "Ergonomic Mouse",
        "price": 49.99,
        "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=300",
        "category": "Electronics",
    },
    {
        "id": 4,
        "name": "USB-C Hub",
        "price": 34.99,
        "image": "https://images.unsplash.com/photo-1625723044792-44de16ccb4e9?w=300",
        "category": "Accessories",
    },
    {
        "id": 5,
        "name": "Laptop Stand",
        "price": 44.99,
        "image": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=300",
        "category": "Accessories",
    },
    {
        "id": 6,
        "name": "Webcam 1080p",
        "price": 59.99,
        "image": "https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=300",
        "category": "Electronics",
    },
    {
        "id": 7,
        "name": "Desk Lamp LED",
        "price": 39.99,
        "image": "https://images.unsplash.com/photo-1507473885765-e6ed057ab6fe?w=300",
        "category": "Office",
    },
    {
        "id": 8,
        "name": 'Monitor 27"',
        "price": 299.99,
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=300",
        "category": "Electronics",
    },
    {
        "id": 9,
        "name": "Notebook Set",
        "price": 14.99,
        "image": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=300",
        "category": "Office",
    },
]


@app.route("/")
def home():
    cart = session.get("cart", {})
    cart_count = sum(cart.values())
    return render_template("index.html", products=PRODUCTS, cart_count=cart_count)


@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    cart_items = []
    total = 0
    for pid, qty in cart.items():
        product = next((p for p in PRODUCTS if p["id"] == int(pid)), None)
        if product:
            subtotal = product["price"] * qty
            cart_items.append({**product, "quantity": qty, "subtotal": subtotal})
            total += subtotal
    return render_template("cart.html", items=cart_items, total=total)


@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    product_id = str(data.get("product_id"))
    cart = session.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session["cart"] = cart
    cart_count = sum(cart.values())
    return jsonify({"success": True, "cart_count": cart_count})


@app.route("/api/cart/remove", methods=["POST"])
def remove_from_cart():
    data = request.get_json()
    product_id = str(data.get("product_id"))
    cart = session.get("cart", {})
    if product_id in cart:
        cart[product_id] -= 1
        if cart[product_id] <= 0:
            del cart[product_id]
    session["cart"] = cart
    return jsonify({"success": True})


@app.route("/checkout")
def checkout():
    if not session.get("cart"):
        return redirect(url_for("view_cart"))

    cart = session.get("cart", {})
    total = sum(
        next(p["price"] for p in PRODUCTS if p["id"] == int(pid)) * qty for pid, qty in cart.items()
    )
    hst = round(total * 0.13, 2)
    grand_total = round(total + hst, 2)

    session.pop("cart", None)
    return render_template("checkout.html", subtotal=total, hst=hst, total=grand_total)


if __name__ == "__main__":
    app.run(debug=True)
