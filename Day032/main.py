"""
Day 32 - Automated Birthday Email Sender

Usage:
  - Configure environment variables (see README.md or .env.example)
  - Run: python main.py

Behavior:
  - Reads birthdays from birthdays.csv (name,email,year,month,day)
  - If today matches (month, day), picks a random template from letter_templates/
  - Replaces [NAME] in the template and composes an email
  - Sends via SMTP unless DRY_RUN=true, in which case it prints the message
"""

from __future__ import annotations

import csv
import os
import random
import smtplib
import sys
from dataclasses import dataclass
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable, List, Optional


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "birthdays.csv"
TEMPLATES_DIR = BASE_DIR / "letter_templates"


@dataclass
class Person:
	name: str
	email: str
	year: int
	month: int
	day: int

	@property
	def md(self) -> tuple[int, int]:
		return (self.month, self.day)


def read_birthdays(csv_path: Path) -> List[Person]:
	people: List[Person] = []
	if not csv_path.exists():
		print(f"[WARN] Missing CSV file: {csv_path}")
		return people
	with csv_path.open(newline="", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		required = {"name", "email", "year", "month", "day"}
		if not required.issubset(reader.fieldnames or []):
			raise ValueError(
				f"birthdays.csv must contain columns: {', '.join(sorted(required))}"
			)
		for row in reader:
			try:
				people.append(
					Person(
						name=row["name"].strip(),
						email=row["email"].strip(),
						year=int(row["year"]),
						month=int(row["month"]),
						day=int(row["day"]),
					)
				)
			except Exception as e:
				print(f"[WARN] Skipping row due to error: {row} -> {e}")
	return people


def pick_random_template(templates_dir: Path) -> Optional[str]:
	if not templates_dir.exists():
		print(f"[WARN] Missing templates dir: {templates_dir}")
		return None
	files = [p for p in templates_dir.iterdir() if p.is_file() and p.suffix == ".txt"]
	if not files:
		print(f"[WARN] No .txt templates found in: {templates_dir}")
		return None
	chosen = random.choice(files)
	return chosen.read_text(encoding="utf-8")


def render_template(template: str, name: str) -> str:
	return template.replace("[NAME]", name)


def get_env_bool(key: str, default: bool = False) -> bool:
	val = os.getenv(key)
	if val is None:
		return default
	return str(val).strip().lower() in {"1", "true", "yes", "on"}


def build_message(from_addr: str, to_addr: str, subject: str, body: str, from_name: Optional[str] = None) -> EmailMessage:
	msg = EmailMessage()
	msg["From"] = f"{from_name} <{from_addr}>" if from_name else from_addr
	msg["To"] = to_addr
	msg["Subject"] = subject
	msg.set_content(body)
	return msg


def send_email(msg: EmailMessage) -> None:
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


def main() -> int:
	today = datetime.now()
	md_today = (today.month, today.day)

	people = read_birthdays(CSV_PATH)
	if not people:
		print("[INFO] No people to process.")
		return 0

	# Filter by today's birthdays
	todays_people = [p for p in people if p.md == md_today]
	if not todays_people:
		print(f"[INFO] No birthdays today ({today:%Y-%m-%d}).")
		return 0

	template = pick_random_template(TEMPLATES_DIR)
	if not template:
		print("[ERROR] Cannot proceed without a template.")
		return 2

	dry_run = get_env_bool("DRY_RUN", True)
	user = os.getenv("EMAIL_USER", "")
	from_name = os.getenv("FROM_NAME", "Birthday Bot")

	for person in todays_people:
		body = render_template(template, person.name)
		subject = f"Happy Birthday, {person.name}!"
		from_addr = user if user else "no-reply@example.com"
		msg = build_message(from_addr, person.email, subject, body, from_name=from_name)

		if dry_run:
			print("----- DRY RUN (no email sent) -----")
			print(msg)
			print("-----------------------------------\n")
		else:
			try:
				send_email(msg)
				print(f"[SENT] to {person.email} - {person.name}")
			except Exception as e:
				print(f"[ERROR] Failed to send to {person.email}: {e}")
				return 3

	return 0


if __name__ == "__main__":
	sys.exit(main())

