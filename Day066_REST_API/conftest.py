"""Test configuration for the Day 66 cafe REST API.

Loads this day's ``main.py`` as a uniquely-named module so pytest
collecting tests from multiple days doesn't return a previously-
cached ``main`` module. Exposes the Flask app, db, model class,
and API key via fixtures (not via direct import, because pytest
doesn't auto-inject conftest module-level names into test modules).
"""

import importlib.util
import os
import sys
import tempfile
from pathlib import Path

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))

# Load main.py under a per-day name to avoid sys.modules collisions
_MODULE_NAME = f"_main_{THIS_DIR.name}"
_spec = importlib.util.spec_from_file_location(_MODULE_NAME, THIS_DIR / "main.py")
_mod = importlib.util.module_from_spec(_spec)
sys.modules[_MODULE_NAME] = _mod
_spec.loader.exec_module(_mod)

# Module-level bindings used to build fixtures below
APP = _mod.app
DB = _mod.db
CAFE = _mod.Cafe
API_KEY = _mod.API_KEY

# Override DATABASE_URI for the rest of the process (in case main is
# re-imported in a later session).
_TMP_DB_DIR = tempfile.mkdtemp(prefix="day066_test_")
os.environ["DATABASE_URI"] = f"sqlite:///{os.path.join(_TMP_DB_DIR, 'test.db')}"

import pytest  # noqa: E402


@pytest.fixture
def client():
    """Flask test client for making requests to the app."""
    return APP.test_client()


@pytest.fixture
def db():
    """SQLAlchemy db instance (for direct queries in fixtures/tests)."""
    return DB


@pytest.fixture
def cafe_class():
    """Cafe ORM model class."""
    return CAFE


@pytest.fixture
def api_key():
    """API key used by secured endpoints."""
    return API_KEY


@pytest.fixture(autouse=True)
def reset_db():
    """Drop and recreate all tables before each test for isolation."""
    with APP.app_context():
        DB.drop_all()
        DB.create_all()
    yield


@pytest.fixture
def sample_cafe():
    """A minimal valid cafe payload for POST /add."""
    return {
        "name": "Test Cafe",
        "map_url": "https://example.com/maps/test",
        "img_url": "https://example.com/img/test.jpg",
        "location": "TestCity",
        "seats": "20-30",
        "has_toilet": "True",
        "has_wifi": "True",
        "has_sockets": "True",
        "can_take_calls": "False",
        "coffee_price": "£2.50",
    }


@pytest.fixture
def add_sample_cafe(client, sample_cafe):
    """Add a sample cafe via the API and return its id."""
    response = client.post("/add", data=sample_cafe)
    assert response.status_code == 201
    cafes = client.get("/all").get_json()["cafes"]
    return cafes[0]["id"]
