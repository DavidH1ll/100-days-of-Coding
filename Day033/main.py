"""
Day 33 - ISS Overhead Email Notifier (APIs)

Usage:
  python main.py [--loop]

Environment variables (see .env.example, README.md):
  LAT, LNG, EMAIL_USER, EMAIL_PASS, TO_EMAIL, SMTP_SERVER, SMTP_PORT,
  USE_TLS, DRY_RUN, FROM_NAME, FORCE_NOTIFY, CHECK_INTERVAL, DISTANCE_DEG_THRESHOLD
"""

from __future__ import annotations

import json
import math
import os
import smtplib
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import Optional, Tuple
from urllib.error import URLError, HTTPError
from urllib.request import urlopen


ISS_API = "http://api.open-notify.org/iss-now.json"
SUN_API = "https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0"


def get_env_bool(key: str, default: bool = False) -> bool:
	"""Return an environment variable parsed as a boolean.

	Accepts common truthy strings: {"1", "true", "yes", "on"} (case-insensitive).
	If the variable is missing, returns ``default``.
	"""
	val = os.getenv(key)
	if val is None:
		return default
	return str(val).strip().lower() in {"1", "true", "yes", "on"}


def get_env_float(key: str, default: float) -> float:
	"""Return an environment variable parsed as ``float`` or ``default`` on error."""
	val = os.getenv(key)
	try:
		return float(val) if val is not None else default
	except Exception:
		return default


def fetch_json(url: str) -> Optional[dict]:
	"""Fetch a URL and return parsed JSON, or ``None`` on failure.

	Network errors and JSON parsing issues are caught and logged as warnings.
	"""
	try:
		with urlopen(url, timeout=20) as resp:
			data = resp.read()
		return json.loads(data.decode("utf-8"))
	except (URLError, HTTPError, TimeoutError, ValueError) as e:
		print(f"[WARN] Failed to fetch {url}: {e}")
		return None


def get_iss_position() -> Optional[Tuple[float, float]]:
	"""Return the current ISS latitude/longitude as floats, or ``None``.

	Uses the Open Notify ISS API. If the response indicates failure or values
	cannot be parsed, returns ``None``.
	"""
	data = fetch_json(ISS_API)
	if not data or data.get("message") != "success":
		return None
	pos = data.get("iss_position", {})
	try:
		lat = float(pos.get("latitude"))
		lng = float(pos.get("longitude"))
		return lat, lng
	except Exception:
		return None


def get_sun_times(lat: float, lng: float) -> Optional[Tuple[datetime, datetime]]:
	"""Get today's sunrise and sunset times (UTC) for a location.

	Returns a tuple ``(sunrise_utc, sunset_utc)`` as timezone-aware datetimes
	in UTC, or ``None`` if the API call fails or values can't be parsed.
	"""
	url = SUN_API.format(lat=lat, lng=lng)
	data = fetch_json(url)
	if not data or data.get("status") != "OK":
		return None
	results = data.get("results", {})
	try:
		sunrise = datetime.fromisoformat(results["sunrise"]).replace(tzinfo=timezone.utc)
		sunset = datetime.fromisoformat(results["sunset"]).replace(tzinfo=timezone.utc)
		return sunrise, sunset
	except Exception as e:
		print(f"[WARN] Bad sunrise/sunset data: {e}")
		return None


def is_night_now(lat: float, lng: float, now_utc: Optional[datetime] = None) -> Optional[bool]:
	"""Determine if it's currently night at a location (using UTC times).

	Night is defined as the period after today's local sunset until the next
	local sunrise. Returns ``True`` if night, ``False`` if day, or ``None`` if
	sunrise/sunset could not be determined.
	"""
	now_utc = now_utc or datetime.now(timezone.utc)
	times = get_sun_times(lat, lng)
	if not times:
		return None
	sunrise, sunset = times
	# Night is when now is after sunset or before sunrise
	return now_utc >= sunset or now_utc <= sunrise


def angular_distance_deg(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
	"""Approximate great-circle angular distance in degrees.

	Uses the spherical law of cosines. Result is clamped to handle rounding
	errors that might push values outside the valid domain of ``acos``.
	"""
	rlat1, rlon1, rlat2, rlon2 = map(math.radians, [lat1, lon1, lat2, lon2])
	cos_d = math.sin(rlat1) * math.sin(rlat2) + math.cos(rlat1) * math.cos(rlat2) * math.cos(rlon2 - rlon1)
	# Clamp due to float rounding
	cos_d = max(-1.0, min(1.0, cos_d))
	return math.degrees(math.acos(cos_d))


def is_iss_overhead(lat: float, lng: float, iss_lat: float, iss_lng: float, threshold_deg: float = 5.0) -> bool:
	"""Return True if ISS is within ``threshold_deg`` angular distance."""
	dist = angular_distance_deg(lat, lng, iss_lat, iss_lng)
	return dist <= threshold_deg


def build_message(from_addr: str, to_addr: str, subject: str, body: str, from_name: Optional[str] = None) -> EmailMessage:
	"""Create a simple plaintext email message object.

	``from_name`` (if provided) will be added as a display name for the From
	header. The body is set as ``text/plain``.
	"""
	msg = EmailMessage()
	msg["From"] = f"{from_name} <{from_addr}>" if from_name else from_addr
	msg["To"] = to_addr
	msg["Subject"] = subject
	msg.set_content(body)
	return msg


def send_email(msg: EmailMessage) -> None:
	"""Send an email message using SMTP configuration from environment.

	Requires EMAIL_USER and EMAIL_PASS. Uses TLS if USE_TLS=true (default).
	Raises RuntimeError when credentials are missing.
	"""
	server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
	port = int(os.getenv("SMTP_PORT", "587"))
	use_tls = get_env_bool("USE_TLS", True)
	user = os.getenv("EMAIL_USER")
	pwd = os.getenv("EMAIL_PASS")
	if not user or not pwd:
		raise RuntimeError("EMAIL_USER and EMAIL_PASS must be set to send emails.")
	with smtplib.SMTP(server, port, timeout=30) as smtp:
		smtp.ehlo()
		if use_tls:
			smtp.starttls()
			smtp.ehlo()
		smtp.login(user, pwd)
		smtp.send_message(msg)



def check_and_notify(override_dry_run: Optional[bool] = None, override_force: Optional[bool] = None) -> int:
	"""Core workflow: determine conditions and send/print notification.

	Returns an exit-like status code:
	  0 -> Success or no action needed
	  1 -> Transient data issue (API fetch failed) – safe to retry
	  2 -> Configuration error (invalid LAT/LNG)
	  3 -> Email send failure
	"""
	# Read config
	try:
		lat = float(os.getenv("LAT", "0"))
		lng = float(os.getenv("LNG", "0"))
	except ValueError:
		print("[ERROR] LAT/LNG must be numeric.")
		return 2
	distance_threshold = get_env_float("DISTANCE_DEG_THRESHOLD", 5.0)
	dry_run = override_dry_run if override_dry_run is not None else get_env_bool("DRY_RUN", True)
	force_notify = override_force if override_force is not None else get_env_bool("FORCE_NOTIFY", False)
	from_name = os.getenv("FROM_NAME", "ISS Notifier")
	user = os.getenv("EMAIL_USER", "")
	to_addr = os.getenv("TO_EMAIL") or user or "no-reply@example.com"
	from_addr = user or "no-reply@example.com"

	if force_notify:
		body = (
			"Look up! (Forced Notification)\n\n"
			f"Location set: lat={lat}, lng={lng}\n"
			f"Time (UTC): {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S}"
		)
		subject = "ISS Overhead (Test)"
		msg = build_message(from_addr, to_addr, subject, body, from_name)
		if dry_run:
			print("----- DRY RUN (forced) -----")
			print(msg)
			print("----------------------------\n")
			return 0
		else:
			try:
				send_email(msg)
				print(f"[SENT] Forced notification to {to_addr}")
				return 0
			except Exception as e:
				print(f"[ERROR] Failed to send (forced): {e}")
				return 3

	iss_pos = get_iss_position()
	if not iss_pos:
		print("[INFO] Could not get ISS position; will retry later.")
		return 1
	iss_lat, iss_lng = iss_pos

	night = is_night_now(lat, lng)
	if night is None:
		print("[INFO] Could not get sunrise/sunset; will retry later.")
		return 1

	overhead = is_iss_overhead(lat, lng, iss_lat, iss_lng, distance_threshold)
	print(
		f"[DEBUG] now_utc={datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S}, "
		f"night={night}, overhead={overhead}, iss=({iss_lat:.2f},{iss_lng:.2f})"
	)

	if night and overhead:
		body = (
			"Look up! The ISS is overhead and it's dark outside.\n\n"
			f"Your location: lat={lat}, lng={lng}\n"
			f"ISS position: lat={iss_lat:.2f}, lng={iss_lng:.2f}\n"
			f"Time (UTC): {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S}"
		)
		subject = "ISS Overhead Now"
		msg = build_message(from_addr, to_addr, subject, body, from_name)
		if dry_run:
			print("----- DRY RUN (no email sent) -----")
			print(msg)
			print("-----------------------------------\n")
			return 0
		else:
			try:
				send_email(msg)
				print(f"[SENT] Notification to {to_addr}")
				return 0
			except Exception as e:
				print(f"[ERROR] Failed to send: {e}")
				return 3
	else:
		print("[INFO] Conditions not met (need night and overhead).")
		return 0


def main(argv: list[str]) -> int:
	"""Entry point parsing CLI flags and optionally looping.

	Flags:
	  --dry-run  : force dry-run regardless of env
	  --force    : force notification regardless of conditions
	  --loop     : run continuously using CHECK_INTERVAL
	"""
	loop = "--loop" in argv
	override_force = "--force" in argv
	override_dry = "--dry-run" in argv
	if not loop:
		return check_and_notify(override_dry_run=override_dry, override_force=override_force)
	interval = int(os.getenv("CHECK_INTERVAL", "600"))
	print(f"[INFO] Looping every {interval}s. Press Ctrl+C to stop.")
	try:
		while True:
			check_and_notify(override_dry_run=override_dry, override_force=override_force)
			time.sleep(interval)
	except KeyboardInterrupt:
		print("\n[INFO] Stopped.")
		return 0


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))

