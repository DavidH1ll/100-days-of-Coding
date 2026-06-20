"""Test configuration for the Day 96 online shop.

Loads this day's ``main.py`` as a uniquely-named module so pytest
collecting tests from multiple days doesn't return a previously-
cached ``main`` module. Exposes the Flask app and product list via
fixtures.
"""

import importlib.util
import sys
from pathlib import Path

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))

# Load main.py under a per-day name to avoid sys.modules collisions
_MODULE_NAME = f"_main_{THIS_DIR.name}"
_spec = importlib.util.spec_from_file_location(_MODULE_NAME, THIS_DIR / "main.py")
_mod = importlib.util.module_from_spec(_spec)
sys.modules[_MODULE_NAME] = _mod
_spec.loader.exec_module(_mod)

# Pre-bind the names we'll expose via fixtures
APP = _mod.app
PRODUCTS = _mod.PRODUCTS

import pytest  # noqa: E402


@pytest.fixture
def app():
    """Flask app instance."""
    return APP


@pytest.fixture
def products():
    """List of products from main.PRODUCTS."""
    return PRODUCTS


@pytest.fixture
def client(app):
    """Flask test client for making requests to the app."""
    return app.test_client()


def _add_to_cart(client, product_id: int, quantity: int = 1) -> None:
    """Add a product to the cart via the JSON API endpoint."""
    response = client.post(
        "/api/cart/add",
        json={"product_id": product_id, "quantity": quantity},
    )
    assert response.status_code == 200
