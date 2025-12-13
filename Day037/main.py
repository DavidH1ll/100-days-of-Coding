import os
import sys
import argparse
import datetime as dt
import requests

BASE_URL = "https://pixe.la/v1/users"


def _today() -> str:
	return dt.date.today().strftime("%Y%m%d")


def _require_env(name: str) -> str:
	val = os.getenv(name)
	if not val:
		print(f"Environment variable {name} is required for this operation.", file=sys.stderr)
		sys.exit(1)
	return val


def create_user(args: argparse.Namespace):
	payload = {
		"token": args.token,
		"username": args.username,
		"agreeTermsOfService": "yes",
		"notMinor": "yes"
	}
	r = requests.post(BASE_URL, json=payload, timeout=15)
	print(r.text)


def create_graph(args: argparse.Namespace):
	username = _require_env("PIXELA_USERNAME") if not args.username else args.username
	token = _require_env("PIXELA_TOKEN") if not args.token else args.token
	graph_id = args.id
	url = f"{BASE_URL}/{username}/graphs"
	headers = {"X-USER-TOKEN": token}
	payload = {
		"id": graph_id,
		"name": args.name,
		"unit": args.unit,
		"type": args.type,
		"color": args.color,
		"timezone": args.timezone,
	}
	r = requests.post(url, json=payload, headers=headers, timeout=15)
	print(r.text)
	if r.ok:
		print(f"Graph URL: https://pixe.la/v1/users/{username}/graphs/{graph_id}.html")


def add_pixel(args: argparse.Namespace):
	username = _require_env("PIXELA_USERNAME")
	token = _require_env("PIXELA_TOKEN")
	graph_id = _require_env("PIXELA_GRAPH_ID") if not args.graph else args.graph
	date = args.date or _today()
	url = f"{BASE_URL}/{username}/graphs/{graph_id}"
	headers = {"X-USER-TOKEN": token}
	payload = {"date": date, "quantity": str(args.quantity)}
	r = requests.post(url, json=payload, headers=headers, timeout=15)
	print(r.text)


def update_pixel(args: argparse.Namespace):
	username = _require_env("PIXELA_USERNAME")
	token = _require_env("PIXELA_TOKEN")
	graph_id = _require_env("PIXELA_GRAPH_ID") if not args.graph else args.graph
	date = args.date or _today()
	url = f"{BASE_URL}/{username}/graphs/{graph_id}/{date}"
	headers = {"X-USER-TOKEN": token}
	payload = {"quantity": str(args.quantity)}
	r = requests.put(url, json=payload, headers=headers, timeout=15)
	print(r.text)


def delete_pixel(args: argparse.Namespace):
	username = _require_env("PIXELA_USERNAME")
	token = _require_env("PIXELA_TOKEN")
	graph_id = _require_env("PIXELA_GRAPH_ID") if not args.graph else args.graph
	date = args.date or _today()
	url = f"{BASE_URL}/{username}/graphs/{graph_id}/{date}"
	headers = {"X-USER-TOKEN": token}
	r = requests.delete(url, headers=headers, timeout=15)
	print(r.text)


def graph_url(args: argparse.Namespace):
	username = _require_env("PIXELA_USERNAME")
	graph_id = _require_env("PIXELA_GRAPH_ID") if not args.graph else args.graph
	print(f"Graph URL: https://pixe.la/v1/users/{username}/graphs/{graph_id}.html")


def parse_args(argv=None):
	p = argparse.ArgumentParser(description="Pixela Habit Tracker CLI (Day 37)")
	sub = p.add_subparsers(dest="cmd", required=True)

	user_p = sub.add_parser("create-user", help="Create a Pixela user")
	user_p.add_argument("username")
	user_p.add_argument("token", help="Desired secret token (store securely)")
	user_p.set_defaults(func=create_user)

	g = sub.add_parser("create-graph", help="Create a graph for tracking a habit")
	g.add_argument("id", help="Graph ID (short identifier, e.g. cycling)")
	g.add_argument("name", help="Graph display name")
	g.add_argument("unit", help="Unit e.g. km, pages, minutes")
	g.add_argument("type", choices=["int", "float"], help="Value type")
	g.add_argument("--color", default="shibafu", help="Pixela color keyword (e.g. shibafu, momiji, sora, ichou, ajisai, kuro)")
	g.add_argument("--timezone", default="UTC", help="Timezone e.g. Europe/London")
	g.add_argument("--username")
	g.add_argument("--token")
	g.set_defaults(func=create_graph)

	add = sub.add_parser("add", help="Add a pixel (log quantity for a date)")
	add.add_argument("quantity", type=float, help="Quantity performed today")
	add.add_argument("--date", help="Date YYYYMMDD (defaults to today)")
	add.add_argument("--graph", help="Override PIXELA_GRAPH_ID env var")
	add.set_defaults(func=add_pixel)

	upd = sub.add_parser("update", help="Update an existing pixel")
	upd.add_argument("quantity", type=float)
	upd.add_argument("--date", help="Date YYYYMMDD (defaults to today)")
	upd.add_argument("--graph", help="Override PIXELA_GRAPH_ID env var")
	upd.set_defaults(func=update_pixel)

	dele = sub.add_parser("delete", help="Delete a pixel")
	dele.add_argument("--date", help="Date YYYYMMDD (defaults to today)")
	dele.add_argument("--graph", help="Override PIXELA_GRAPH_ID env var")
	dele.set_defaults(func=delete_pixel)

	gurl = sub.add_parser("graph-url", help="Print the graph URL to open in browser")
	gurl.add_argument("--graph", help="Override PIXELA_GRAPH_ID env var")
	gurl.set_defaults(func=graph_url)

	return p.parse_args(argv)


def main():
	args = parse_args()
	args.func(args)


if __name__ == "__main__":
	main()

