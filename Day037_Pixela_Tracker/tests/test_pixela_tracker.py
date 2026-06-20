"""Tests for Day 037 — Pixela Habit Tracker CLI.

The CLI delegates the actual HTTP work to Pixela. These tests cover:
  - The pure helpers (`_today`, `_require_env`)
  - Argparse wiring (every subcommand, defaults, overrides)
  - The HTTP-using functions, with `requests.post/put/delete` mocked
"""
from __future__ import annotations

import argparse
import datetime as dt
from unittest.mock import MagicMock, patch

import pixela_tracker as pt
import pytest

# ---------------------------------------------------------------------------
# _today
# ---------------------------------------------------------------------------


def test_today_returns_yyyymmdd_string() -> None:
    result = pt._today()
    assert isinstance(result, str)
    assert len(result) == 8
    assert result.isdigit()
    assert dt.datetime.strptime(result, "%Y%m%d").date() == dt.date.today()


# ---------------------------------------------------------------------------
# _require_env
# ---------------------------------------------------------------------------


def test_require_env_returns_value_when_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PIXELA_TEST_VAR", "secret123")
    assert pt._require_env("PIXELA_TEST_VAR") == "secret123"


def test_require_env_exits_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PIXELA_TEST_VAR", raising=False)
    with pytest.raises(SystemExit) as exc_info:
        pt._require_env("PIXELA_TEST_VAR")
    assert exc_info.value.code == 1


def test_require_env_exits_when_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PIXELA_TEST_VAR", "")
    with pytest.raises(SystemExit) as exc_info:
        pt._require_env("PIXELA_TEST_VAR")
    assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# parse_args
# ---------------------------------------------------------------------------


def test_parse_args_create_user() -> None:
    args = pt.parse_args(["create-user", "alice", "tok123"])
    assert isinstance(args, argparse.Namespace)
    assert args.cmd == "create-user"
    assert args.username == "alice"
    assert args.token == "tok123"
    assert args.func is pt.create_user


def test_parse_args_create_graph_required() -> None:
    args = pt.parse_args(["create-graph", "cycling", "Cycling", "km", "int"])
    assert args.cmd == "create-graph"
    assert args.id == "cycling"
    assert args.name == "Cycling"
    assert args.unit == "km"
    assert args.type == "int"
    # Defaults
    assert args.color == "shibafu"
    assert args.timezone == "UTC"
    assert args.username is None
    assert args.token is None
    assert args.func is pt.create_graph


def test_parse_args_create_graph_with_overrides() -> None:
    args = pt.parse_args([
        "create-graph", "reading", "Reading", "pages", "float",
        "--color", "momiji",
        "--timezone", "Europe/London",
        "--username", "alice",
        "--token", "tok",
    ])
    assert args.color == "momiji"
    assert args.timezone == "Europe/London"
    assert args.username == "alice"
    assert args.token == "tok"


def test_parse_args_create_graph_rejects_bad_type() -> None:
    with pytest.raises(SystemExit):
        pt.parse_args(["create-graph", "id", "Name", "unit", "string"])


def test_parse_args_add_pixel_quantity_only() -> None:
    args = pt.parse_args(["add", "5.0"])
    assert args.cmd == "add"
    assert args.quantity == 5.0
    assert args.date is None
    assert args.graph is None
    assert args.func is pt.add_pixel


def test_parse_args_add_pixel_with_date_and_graph() -> None:
    args = pt.parse_args(["add", "10", "--date", "20260615", "--graph", "reading"])
    assert args.quantity == 10.0
    assert args.date == "20260615"
    assert args.graph == "reading"


def test_parse_args_update_pixel() -> None:
    args = pt.parse_args(["update", "7", "--date", "20260615"])
    assert args.func is pt.update_pixel
    assert args.quantity == 7.0
    assert args.date == "20260615"


def test_parse_args_delete_pixel() -> None:
    args = pt.parse_args(["delete", "--date", "20260615"])
    assert args.func is pt.delete_pixel
    assert args.date == "20260615"


def test_parse_args_graph_url() -> None:
    args = pt.parse_args(["graph-url", "--graph", "cycling"])
    assert args.func is pt.graph_url
    assert args.graph == "cycling"


def test_parse_args_requires_subcommand() -> None:
    with pytest.raises(SystemExit):
        pt.parse_args([])


# ---------------------------------------------------------------------------
# create_user (mocked HTTP)
# ---------------------------------------------------------------------------


def test_create_user_posts_expected_payload(
    capsys: pytest.CaptureFixture[str],
) -> None:
    fake_response = MagicMock()
    fake_response.text = "{\"message\":\"Success.\",\"isSuccess\":true}"
    with patch("pixela_tracker.requests.post", return_value=fake_response) as post:
        args = pt.parse_args(["create-user", "alice", "tok123"])
        pt.create_user(args)

    post.assert_called_once()
    call = post.call_args
    assert call.args[0] == pt.BASE_URL
    assert call.kwargs["json"] == {
        "token": "tok123",
        "username": "alice",
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    assert call.kwargs["timeout"] == 15


def test_create_user_prints_response_text(
    capsys: pytest.CaptureFixture[str],
) -> None:
    fake_response = MagicMock()
    fake_response.text = "{\"message\":\"Created.\"}"
    with patch("pixela_tracker.requests.post", return_value=fake_response):
        args = pt.parse_args(["create-user", "alice", "tok"])
        pt.create_user(args)

    captured = capsys.readouterr()
    assert "Created." in captured.out


# ---------------------------------------------------------------------------
# add_pixel (mocked HTTP, env vars + CLI override)
# ---------------------------------------------------------------------------


def test_add_pixel_uses_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PIXELA_USERNAME", "alice")
    monkeypatch.setenv("PIXELA_TOKEN", "tok")
    monkeypatch.setenv("PIXELA_GRAPH_ID", "cycling")
    fake_response = MagicMock()
    fake_response.text = "{\"message\":\"Success.\"}"
    with patch("pixela_tracker.requests.post", return_value=fake_response) as post:
        args = pt.parse_args(["add", "5.0"])
        pt.add_pixel(args)

    call = post.call_args
    assert call.args[0] == f"{pt.BASE_URL}/alice/graphs/cycling"
    assert call.kwargs["headers"] == {"X-USER-TOKEN": "tok"}
    payload = call.kwargs["json"]
    assert payload["quantity"] == "5.0"
    assert payload["date"] == dt.date.today().strftime("%Y%m%d")


def test_add_pixel_cli_graph_overrides_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PIXELA_USERNAME", "alice")
    monkeypatch.setenv("PIXELA_TOKEN", "tok")
    monkeypatch.setenv("PIXELA_GRAPH_ID", "cycling")
    fake_response = MagicMock()
    fake_response.text = "{\"message\":\"Success.\"}"
    with patch("pixela_tracker.requests.post", return_value=fake_response) as post:
        args = pt.parse_args(["add", "5.0", "--graph", "reading"])
        pt.add_pixel(args)

    assert "graphs/reading" in post.call_args.args[0]
    assert "cycling" not in post.call_args.args[0]


# ---------------------------------------------------------------------------
# graph_url
# ---------------------------------------------------------------------------


def test_graph_url_prints_url(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("PIXELA_USERNAME", "alice")
    monkeypatch.setenv("PIXELA_GRAPH_ID", "cycling")
    args = pt.parse_args(["graph-url"])
    pt.graph_url(args)
    captured = capsys.readouterr()
    assert "https://pixe.la/v1/users/alice/graphs/cycling.html" in captured.out
