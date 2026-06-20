"""Tests for the Day 66 cafe REST API.

Uses Flask's ``test_client`` so no real server is needed and the tests
run in milliseconds. The conftest.py module loads this day's main
as a uniquely-named module to avoid cross-day collisions and
exposes ``app``, ``api_key``, and other fixtures for the tests to
use.
"""

from __future__ import annotations

import pytest  # noqa: F401  — fixtures (client, api_key, etc.) injected by conftest


class TestHome:
    def test_home_returns_200(self, client) -> None:
        response = client.get("/")
        assert response.status_code == 200


class TestGetRandom:
    def test_random_with_no_cafes_returns_404(self, client) -> None:
        response = client.get("/random")
        assert response.status_code == 404
        assert "error" in response.get_json()

    def test_random_with_cafes_returns_200(self, client, add_sample_cafe) -> None:
        response = client.get("/random")
        assert response.status_code == 200
        body = response.get_json()
        assert "cafe" in body
        assert body["cafe"]["name"] == "Test Cafe"


class TestGetAll:
    def test_all_with_no_cafes_returns_empty_list(self, client) -> None:
        response = client.get("/all")
        assert response.status_code == 200
        assert response.get_json() == {"cafes": []}

    def test_all_returns_added_cafes(self, client, sample_cafe) -> None:
        client.post("/add", data=sample_cafe)
        response = client.get("/all")
        assert response.status_code == 200
        cafes = response.get_json()["cafes"]
        assert len(cafes) == 1
        assert cafes[0]["name"] == "Test Cafe"


class TestSearch:
    def test_search_with_match_returns_200(self, client, add_sample_cafe) -> None:
        response = client.get("/search", query_string={"loc": "TestCity"})
        assert response.status_code == 200
        cafes = response.get_json()["cafes"]
        assert len(cafes) == 1
        assert cafes[0]["location"] == "TestCity"

    def test_search_with_no_match_returns_404(self, client) -> None:
        response = client.get("/search", query_string={"loc": "NonExistent"})
        assert response.status_code == 404
        assert "error" in response.get_json()

    def test_search_without_loc_param(self, client) -> None:
        response = client.get("/search")
        # query_location is None, so WHERE location = None matches nothing → 404
        assert response.status_code == 404


class TestAddCafe:
    def test_add_valid_cafe_returns_201(self, client, sample_cafe) -> None:
        response = client.post("/add", data=sample_cafe)
        assert response.status_code == 201
        assert "Successfully" in response.get_json()["response"]["success"]

    def test_add_cafe_persists(self, client, sample_cafe) -> None:
        client.post("/add", data=sample_cafe)
        cafes = client.get("/all").get_json()["cafes"]
        assert len(cafes) == 1
        assert cafes[0]["coffee_price"] == "£2.50"

    def test_add_duplicate_name_returns_400(self, client, sample_cafe) -> None:
        client.post("/add", data=sample_cafe)
        response = client.post("/add", data=sample_cafe)
        assert response.status_code == 400
        assert "error" in response.get_json()


class TestUpdatePrice:
    def test_update_with_correct_api_key(
        self,
        client,
        add_sample_cafe,
        api_key,
    ) -> None:
        response = client.patch(
            f"/update-price/{add_sample_cafe}",
            query_string={"new_price": "£4.00", "api-key": api_key},
        )
        assert response.status_code == 200
        # Verify the price was actually updated
        cafes = client.get("/all").get_json()["cafes"]
        assert cafes[0]["coffee_price"] == "£4.00"

    def test_update_with_wrong_api_key(
        self,
        client,
        add_sample_cafe,
    ) -> None:
        response = client.patch(
            f"/update-price/{add_sample_cafe}",
            query_string={"new_price": "£4.00", "api-key": "WrongKey"},
        )
        assert response.status_code == 403

    def test_update_with_missing_api_key(
        self,
        client,
        add_sample_cafe,
    ) -> None:
        response = client.patch(
            f"/update-price/{add_sample_cafe}",
            query_string={"new_price": "£4.00"},
        )
        assert response.status_code == 403

    def test_update_nonexistent_cafe(self, client, api_key) -> None:
        response = client.patch(
            "/update-price/9999",
            query_string={"new_price": "£4.00", "api-key": api_key},
        )
        assert response.status_code == 404


class TestDeleteCafe:
    def test_delete_with_correct_api_key(
        self,
        client,
        add_sample_cafe,
        api_key,
    ) -> None:
        response = client.delete(
            f"/report-closed/{add_sample_cafe}",
            query_string={"api-key": api_key},
        )
        assert response.status_code == 200
        # Verify cafe is gone
        cafes = client.get("/all").get_json()["cafes"]
        assert cafes == []

    def test_delete_with_wrong_api_key(
        self,
        client,
        add_sample_cafe,
    ) -> None:
        response = client.delete(
            f"/report-closed/{add_sample_cafe}",
            query_string={"api-key": "WrongKey"},
        )
        assert response.status_code == 403

    def test_delete_with_missing_api_key(
        self,
        client,
        add_sample_cafe,
    ) -> None:
        response = client.delete(
            f"/report-closed/{add_sample_cafe}",
        )
        assert response.status_code == 403


class TestConstants:
    def test_default_api_key(self, api_key) -> None:
        # main.py falls back to a default if API_KEY env var is unset
        assert api_key == "TopSecretAPIKey"
