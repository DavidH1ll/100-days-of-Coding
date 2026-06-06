"""Day 35 - Weather Alert App

Checks upcoming weather (next N hours) using OpenWeatherMap forecast API and
sends an email alert if precipitation is likely. Supports dry-run, force, and
looping modes.

Usage:
  python main.py [--dry-run] [--force] [--loop]

Environment (.env.example provided):
  WEATHER_API_KEY, LAT, LNG, UNITS, EMAIL_USER, EMAIL_PASS, TO_EMAIL,
  SMTP_SERVER, SMTP_PORT, USE_TLS, FROM_NAME, DRY_RUN, FORCE_ALERT,
  CHECK_INTERVAL, ALERT_HORIZON_HOURS
"""
from __future__ import annotations

import os
import smtplib
import sys
import time
from email.message import EmailMessage
from datetime import datetime, timezone
from typing import Optional, List, Dict
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from weather import fetch_forecast, simplify_forecast, will_precipitate_periods


def env_bool(key: str, default: bool = False) -> bool:
	val = os.getenv(key)
	if val is None:
		return default
	return val.strip().lower() in {"1", "true", "yes", "on"}


def build_email(from_addr: str, to_addr: str, subject: str, body: str, from_name: Optional[str]) -> EmailMessage:
	msg = EmailMessage()
	msg["From"] = f"{from_name} <{from_addr}>" if from_name else from_addr
	msg["To"] = to_addr
	msg["Subject"] = subject
	msg.set_content(body)
	return msg


def send_email(msg: EmailMessage) -> None:
	server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
	port = int(os.getenv("SMTP_PORT", "587"))
	use_tls = env_bool("USE_TLS", True)
	user = os.getenv("EMAIL_USER")
	pwd = os.getenv("EMAIL_PASS")
	if not user or not pwd:
		raise RuntimeError("EMAIL_USER and EMAIL_PASS must be set to send.")
	with smtplib.SMTP(server, port, timeout=30) as smtp:
		smtp.ehlo()
		if use_tls:
			smtp.starttls(); smtp.ehlo()
		smtp.login(user, pwd)
		smtp.send_message(msg)


def format_periods(periods: List[Dict[str, object]]) -> str:
	lines = []
	for p in periods[:6]:  # limit for brevity
		t = p['time_utc']
		lines.append(
			f"{t:%Y-%m-%d %H:%M}Z | pop={p['pop']:.0%} rain={p['rain_mm']:.1f}mm snow={p['snow_mm']:.1f}mm {p['weather_main']} ({p['weather_desc']})"
		)
	return "\n".join(lines)


def check_and_alert(override_dry: Optional[bool] = None, override_force: Optional[bool] = None) -> int:
	api_key = os.getenv("WEATHER_API_KEY")
	if not api_key:
		print("[ERROR] WEATHER_API_KEY not set.")
		return 2
	try:
		lat = float(os.getenv("LAT", "0"))
		lon = float(os.getenv("LNG", "0"))
	except ValueError:
		print("[ERROR] LAT/LNG must be numeric.")
		return 2
	units = os.getenv("UNITS", "metric")
	horizon = int(os.getenv("ALERT_HORIZON_HOURS", "12"))
	dry_run = override_dry if override_dry is not None else env_bool("DRY_RUN", True)
	force = override_force if override_force is not None else env_bool("FORCE_ALERT", False)

	raw = fetch_forecast(lat, lon, api_key, units)
	if not raw:
		return 1
	periods = simplify_forecast(raw, horizon)
	precip_periods = will_precipitate_periods(periods)

	user = os.getenv("EMAIL_USER", "")
	to_addr = os.getenv("TO_EMAIL") or user or "no-reply@example.com"
	from_addr = user or "no-reply@example.com"
	from_name = os.getenv("FROM_NAME", "Weather Alert")

	now = datetime.now(timezone.utc)
	subject = "Weather Alert: Precipitation Expected" if precip_periods else "Weather Check: No Precipitation"

	body_lines = [
		f"Generated: {now:%Y-%m-%d %H:%M:%S}Z",
		f"Location: lat={lat}, lon={lon}",
		f"Horizon: {horizon}h",
		f"Units: {units}",
		"",
	]

	if force:
		body_lines.append("FORCE ALERT ACTIVE - Sending regardless of conditions.\n")

	if precip_periods or force:
		body_lines.append("Precipitation periods (subset):")
		body_lines.append(format_periods(precip_periods if precip_periods else periods))
	else:
		body_lines.append("No precipitation expected in selected horizon.")
		body_lines.append("Sample periods:")
		body_lines.append(format_periods(periods))

	body = "\n".join(body_lines)
	msg = build_email(from_addr, to_addr, subject, body, from_name)

	if dry_run:
		print("----- DRY RUN -----")
		print(msg)
		print("-------------------\n")
		return 0

	if precip_periods or force:
		try:
			send_email(msg)
			print(f"[SENT] Alert to {to_addr}")
			return 0
		except Exception as e:
			print(f"[ERROR] Send failed: {e}")
			return 3
	else:
		print("[INFO] No alert conditions met.")
		return 0


def main(argv: list[str]) -> int:
	loop = "--loop" in argv
	override_force = "--force" in argv
	override_dry = "--dry-run" in argv
	if not loop:
		return check_and_alert(override_dry=override_dry, override_force=override_force)
	interval = int(os.getenv("CHECK_INTERVAL", "1800"))
	print(f"[INFO] Looping every {interval}s. Ctrl+C to stop.")
	try:
		while True:
			check_and_alert(override_dry=override_dry, override_force=override_force)
			time.sleep(interval)
	except KeyboardInterrupt:
		print("\n[INFO] Stopped.")
		return 0


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))

