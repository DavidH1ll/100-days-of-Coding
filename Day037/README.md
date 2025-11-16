# Day 37 - Pixela Habit Tracker CLI

Build a command‑line habit tracker using the Pixela API. Today focused on:

- Header‑based authentication (sending `X-USER-TOKEN` instead of query params)
- Making `POST`, `PUT`, and `DELETE` requests with `requests`
- Designing a small, composable API client + CLI
- Visual habit tracking (intensity over time)

## What Is Pixela?
Pixela (https://pixe.la) lets you create graphs where each day you "commit" a quantity (pages read, km cycled, minutes meditated). It renders a calendar-like grid whose color depth reflects intensity.

## Features Implemented
- Create user (agree TOS & age confirmation)
- Create graph (unit, type, color, timezone)
- Add pixel (log today's or arbitrary date value)
- Update pixel (change quantity for a date)
- Delete pixel (remove a day's entry)
- Print graph URL for browser viewing

All authenticated endpoints send `X-USER-TOKEN` header.

## File Overview
```
Day037/
├── main.py      # Pixela CLI client
└── README.md    # This file
```

## Environment Variables (Recommended)
Set these once per session so you don’t expose secrets on the command line:
```powershell
$env:PIXELA_USERNAME="yourusername"
$env:PIXELA_TOKEN="your-secret-token"
$env:PIXELA_GRAPH_ID="cycling"  # or reading, coding, etc.
```
You can override with flags (`--username`, `--token`, `--graph`).

## Creating a User
Only perform once per Pixela account:
```powershell
python main.py create-user yourusername your-secret-token
```
Response should contain `"isSuccess":true` if created.

## Creating a Graph
```powershell
python main.py create-graph cycling "Cycling Distance" km float --color shibafu --timezone Europe/London
```
Common colors: `shibafu, momiji, sora, ichou, ajisai, kuro`.
Graph URL afterwards:
```powershell
python main.py graph-url
```

## Logging a Habit (Add Pixel)
Default date = today:
```powershell
python main.py add 12.7          # e.g. 12.7 km cycled
```
Past date:
```powershell
python main.py add 8 --date 20250103
```

## Updating a Day
```powershell
python main.py update 15 --date 20250103
```

## Deleting a Day
```powershell
python main.py delete --date 20250103
```

## Opening Your Graph
```powershell
python main.py graph-url
```
Outputs: `https://pixe.la/v1/users/<username>/graphs/<graph_id>.html`

## How It Works Internally
1. CLI parses subcommand (`create-user`, `create-graph`, `add`, `update`, `delete`, `graph-url`).
2. Builds endpoint URL: `https://pixe.la/v1/users/<username>/...`
3. Adds `X-USER-TOKEN` header for auth.
4. Sends `POST`, `PUT`, or `DELETE` with JSON payload.
5. Prints raw JSON response for transparency.

## Error Handling & Assumptions
- If required env var missing, script aborts with a message.
- Timeouts set (15s) to avoid hanging.
- Quantities are converted to string per Pixela API spec.
- Graph `type` must match your input (`int` vs `float`).

## Extending Further (Next Steps)
| Goal | Idea |
| ---- | ---- |
| Streak tracking | Add GET to `/graphs/<id>` and compute consecutive days. |
| Bulk import | Parse CSV of date,quantity and loop add calls. |
| Visualization | Local script that fetches pixels and renders heatmap. |
| Notifications | Daily reminder if no pixel logged by certain time. |
| Security | Move token loading to `.env` (e.g. `python-dotenv`). |

## Example Windows Script (Daily Log)
Create a PowerShell script `log_cycle.ps1`:
```powershell
$env:PIXELA_USERNAME="yourusername"
$env:PIXELA_TOKEN="your-secret-token"
$env:PIXELA_GRAPH_ID="cycling"
python "Day037/main.py" add 10.2
```
Schedule in Windows Task Scheduler for 20:00 every day.

## Troubleshooting
| Symptom | Fix |
| ------- | ---- |
| `isSuccess:false` with message about token | Token already used or invalid; choose a different one. |
| 400 error creating graph | Check unique graph ID and valid color keyword. |
| Update returns `record not found` | Pixel for that date wasn’t created yet; use `add` first. |
| Delete says success but graph still shows color | Browser cache; refresh or wait a few seconds. |
| Wrong timezone visual | Recreate graph with correct `--timezone` (cannot edit later). |

## Security Tips
- Treat `PIXELA_TOKEN` like a password.
- Do not commit it to Git.
- Prefer environment variables or encrypted secret managers.

## Inspiration
Inspired by Simone Giertz’s physical habit tracker concept—maintain unbroken streaks and visualize intensity.

---
Happy Tracking! 🚀
