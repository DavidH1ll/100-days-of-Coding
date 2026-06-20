"""Tests for the Day 96 online shop Flask app.

Uses Flask's ``test_client`` so no real server is needed. Cart state
lives in the Flask session, which is per-client and reset between
tests (each test gets a fresh ``client`` fixture). The conftest loads
this day's main as a uniquely-named module to avoid cross-day
collisions and exposes ``app``, ``products``, and ``client``
fixtures.
"""

from __future__ import annotations

import pytest  # noqa: F401  — fixtures (client, products, app) injected by conftest

HST_RATE = 0.13


class TestHome:
    def test_home_returns_200(self, client) -> None:
        response = client.get("/")
        assert response.status_code == 200

    def test_home_shows_products(self, client, products) -> None:
        response = client.get("/")
        body = response.get_data(as_text=True)
        # Spot-check a couple of product names
        assert products[0]["name"] in body
        assert products[-1]["name"] in body

    def test_home_with_empty_cart(self, client) -> None:
        response = client.get("/")
        assert response.status_code == 200
        # No errors on empty cart


class TestCart:
    def test_empty_cart_renders(self, client) -> None:
        response = client.get("/cart")
        assert response.status_code == 200

    def test_add_item_via_api(self, client, products) -> None:
        response = client.post(
            "/api/cart/add",
            json={"product_id": products[0]["id"]},
        )
        assert response.status_code == 200
        body = response.get_json()
        assert body["success"] is True
        assert body["cart_count"] == 1

    def test_add_same_item_twice_increases_quantity(self, client, products) -> None:
        client.post("/api/cart/add", json={"product_id": products[0]["id"]})
        response = client.post(
            "/api/cart/add",
            json={"product_id": products[0]["id"]},
        )
        assert response.get_json()["cart_count"] == 2

    def test_add_different_items(self, client, products) -> None:
        client.post("/api/cart/add", json={"product_id": products[0]["id"]})
        response = client.post(
            "/api/cart/add",
            json={"product_id": products[1]["id"]},
        )
        assert response.get_json()["cart_count"] == 2

    def test_cart_total_reflects_items(self, client, products) -> None:
        client.post("/api/cart/add", json={"product_id": products[0]["id"]})
        client.post("/api/cart/add", json={"product_id": products[1]["id"]})
        response = client.get("/cart")
        body = response.get_data(as_text=True)
        # Both product names should appear
        assert products[0]["name"] in body
        assert products[1]["name"] in body

    def test_remove_item(self, client, products) -> None:
        # Add 2 of the same item, then remove 1
        client.post("/api/cart/add", json={"product_id": products[0]["id"]})
        client.post("/api/cart/add", json={"product_id": products[0]["id"]})
        response = client.post(
            "/api/cart/remove",
            json={"product_id": products[0]["id"]},
        )
        assert response.status_code == 200
        # Add endpoint to check count
        add_resp = client.post(
            "/api/cart/add",
            json={"product_id": products[0]["id"]},
        )
        assert add_resp.get_json()["cart_count"] == 2

    def test_remove_nonexistent_item_is_noop(self, client, products) -> None:
        # Adding then removing then adding should not error
        client.post("/api/cart/add", json={"product_id": products[0]["id"]})
        client.post(
            "/api/cart/remove",
            json={"product_id": products[1]["id"]},
        )
        # No exception; cart still has the first item
        add_resp = client.post(
            "/api/cart/add",
            json={"product_id": products[1]["id"]},
        )
        assert add_resp.get_json()["cart_count"] == 2


class TestCheckout:
    def test_empty_cart_redirects_to_cart(self, client) -> None:
        response = client.get("/checkout")
        assert response.status_code == 302
        assert "/cart" in response.headers["Location"]

    def test_checkout_with_items_clears_cart(self, client, products) -> None:
        client.post("/api/cart/add", json={"product_id": products[0]["id"]})
        response = client.get("/checkout")
        assert response.status_code == 200
        # Cart should now be empty
        add_resp = client.post(
            "/api/cart/add",
            json={"product_id": products[0]["id"]},
        )
        assert add_resp.get_json()["cart_count"] == 1

    def test_checkout_calculates_hst(self, client, products) -> None:
        # Add one item with a known price
        product = products[0]
        expected_subtotal = product["price"]
        expected_hst = round(expected_subtotal * HST_RATE, 2)
        client.post("/api/cart/add", json={"product_id": product["id"]})
        response = client.get("/checkout")
        body = response.get_data(as_text=True)
        # The page should display the totals
        assert f"{expected_subtotal:.2f}" in body
        assert f"{expected_hst:.2f}" in body

    def test_checkout_with_multiple_quantities(self, client, products) -> None:
        product = products[0]
        client.post("/api/cart/add", json={"product_id": product["id"]})
        client.post("/api/cart/add", json={"product_id": product["id"]})
        client.post("/api/cart/add", json={"product_id": product["id"]})
        expected_subtotal = round(product["price"] * 3, 2)
        expected_hst = round(expected_subtotal * HST_RATE, 2)
        # Reset and redo to verify the page renders
        client.post("/api/cart/remove", json={"product_id": product["id"]})
        client.post("/api/cart/remove", json={"product_id": product["id"]})
        client.post("/api/cart/remove", json={"product_id": product["id"]})
        client.post("/api/cart/add", json={"product_id": product["id"]})
        client.post("/api/cart/add", json={"product_id": product["id"]})
        client.post("/api/cart/add", json={"product_id": product["id"]})
        response = client.get("/checkout")
        body = response.get_data(as_text=True)
        assert f"{expected_subtotal:.2f}" in body
        assert f"{expected_hst:.2f}" in body


class TestProducts:
    def test_all_products_have_required_fields(self, products) -> None:
        required = {"id", "name", "price", "image", "category"}
        for product in products:
            assert required.issubset(product.keys()), f"Missing fields in {product}"

    def test_all_product_ids_are_unique(self, products) -> None:
        ids = [p["id"] for p in products]
        assert len(ids) == len(set(ids))

    def test_all_prices_are_positive(self, products) -> None:
        for product in products:
            assert product["price"] > 0
