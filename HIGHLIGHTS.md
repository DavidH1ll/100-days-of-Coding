# Highlights

A focused tour of the projects and patterns that show up well on this
journey — the ones I'd point a reviewer at first, and the practices the
repo now follows across the later days.

For day-by-day content see [README.md](README.md). For conventions used
across the day folders see [LAYOUT.md](LAYOUT.md).

---

## Most Polished Projects

### Day 100 — Earnings Predictor (capstone)
[`Day100_Earnings_Predictor/`](Day100_Earnings_Predictor/)

A complete ML pipeline: load, clean, engineer features, train five
models, compare with cross-validation, dump the comparison and a
feature-importance chart.

- Refactored from a 190-line top-level script into 12 typed, documented
  functions with an `if __name__ == "__main__"` guard.
- Outputs (PNG figures, a CSV of the model comparison) go to `figures/`
  and `data/` so they can be regenerated and `.gitignore`d.
- 19 pytest tests covering the data-loading, cleaning, and evaluation
  helpers — the math is testable without spinning up a training run.

### Day 080 — House Price Predictor
[`Day080_House_Price_Predictor/`](Day080_House_Price_Predictor/)

Linear Regression vs. Random Forest on the California housing dataset
with EDA, residual plots, and a model-comparison figure.

- Refactored the original notebook-style script into 13 typed functions.
- Generated PNGs and the processed dataset live in `figures/` and
  `data/` (gitignored).
- 19 pytest tests, full suite runs in 2.6 s.

### Day 096 — Online Shop (Flask + JS cart)
[`Day096_Online_Shop/`](Day096_Online_Shop/)

A small e-commerce site: product grid, session-based cart, an async
checkout that POSTs JSON, Bootstrap-styled templates.

- 17 pytest tests using Flask's `test_client` (no live server needed).
- Uses `importlib` in `conftest.py` to load the app as a per-day
  module so it can sit alongside other days' tests without
  `sys.modules` collisions.

### Day 081 — Typing Speed Test
[`Day081_Typing_Speed_Test/`](Day081_Typing_Speed_Test/)

Tkinter typing-test app with WPM and accuracy. The original
`typing_speed_test.py` was the app, not a test — renamed to
`main.py` and pulled the scoring math into a separate `scoring.py`
module so it can be tested.

- 26 unit tests on the pure scoring functions (`compute_wpm`,
  `compute_accuracy`, `compute_completion`).
- Tests run in 0.03 s — no display required.

### Day 066 — Cafe REST API
[`Day066_REST_API/`](Day066_REST_API/)

RESTful cafe database with full CRUD and API-key auth. The original
`test_api.py` was a manual integration test that hit a running server
— replaced with 19 proper pytest tests using Flask's `test_client`.

- `conftest.py` sets a temp-file `DATABASE_URI` and uses `importlib`
  to import the app under a per-day module name.
- Tests cover auth (200/401/403), CRUD, validation errors, and
  random-cafe endpoint.

### Day 037 — Pixela Habit Tracker CLI
[`Day037_Pixela_Tracker/`](Day037_Pixela_Tracker/)

A small CLI for posting daily habit pixels to the Pixela API
(create user, create graph, add/update/delete pixels, print graph
URL). The original `pixela_tracker.py` was already cleanly factored
into typed functions and an argparse dispatch — it just needed
tests and a `.env.example` template.

- 19 pytest tests covering the pure helpers (`_today`, `_require_env`),
  every argparse subcommand, and the HTTP-using functions with
  `requests` mocked.
- Tests pin the env-var/CLI-override behaviour for the add/update
  flow so the contract doesn't silently regress.

---

## Notable Patterns Across the Repo

### Test infrastructure
- **119 pytest tests** across 6 days (037, 066, 080, 081, 096, 100).
  Full suite runs in ~5.6 s.
- **Cross-day conftest isolation.** Several days have a `main.py` that
  is also the script entry point. Their `conftest.py` files use
  `importlib.util.spec_from_file_location` to load `main.py` as a
  unique module name (e.g. `_main_Day066_REST_API`) so pytest can
  collect tests from multiple days in one run without them stepping
  on each other in `sys.modules`.
- **One conftest per day, not one root conftest.** Each day is a
  self-contained unit; nothing bleeds across days.

### Code quality
- **`ruff`** for lint and format. Config in `pyproject.toml`.
- **`pre-commit`** runs `ruff check --fix` and `ruff format` on every
  commit.
- **GitHub Actions** runs `ruff check`, `ruff format --check`, and
  `pytest -v` on every push to `main`.

### Project layout
- **One standard, three flavours.** LAYOUT.md defines a single folder
  shape for Python scripts, Flask apps, and data-science days. Day
  100 is the reference implementation; later days follow it.
- **Generated outputs in `figures/` and `data/`**, never at the
  folder root. This keeps `.gitignore` patterns simple and the
  working tree clean.
- **No `__pycache__`, no `.env`, no `.venv`** in the repo. Patterns
  in `.gitignore` are written for 3-digit day names
  (`Day07[0-9][0-9]_*`) so they actually match.

---

## Data-Science and ML Work

| Day | Topic | What's interesting |
|-----|-------|-------------------|
| 071 | Pandas intro | `.groupby()`, `.describe()`, sorting — first real DataFrame work |
| 072 | Matplotlib | Subplots, bar/pie charts, legends |
| 073 | Merge & aggregate | `.merge()`, `.pivot_table()`, multi-file joins |
| 074 | Time series | `resample()`, `rolling()`, Google Trends data |
| 075 | Plotly + App Store | Interactive scatter, sunburst, HTML export |
| 076 | NumPy | Broadcasting, `linalg`, reshaping |
| 077 | Linear regression | `seaborn.regplot`, `scipy.stats.linregress`, residuals |
| 078 | Nobel Prize | `plotly.choropleth`, multi-library viz |
| 079 | t-tests | Semmelweis handwashing, `scipy.stats.ttest_ind` |
| 080 | Regression models | Linear vs Random Forest, cross-validated metrics |
| 098 | Space Race | Choropleth, sunburst, cost-over-time analysis |
| 099 | Police deaths | Chi-square, heatmaps, demographic distributions |
| 100 | ML capstone | 5 models, `GridSearchCV`, feature importance, model selection |

---

## What This Repo Shows

- **Range.** Core Python through OOP, automation, scraping, three
  web frameworks (Flask, FastAPI patterns), data science, ML, and
  game/UI work in 100 self-contained projects.
- **Refactoring discipline.** The "tooling" cleanup (Phase 1) added
  a single standard for tests, lint, and project layout across the
  repo. The "refactors" (Phase 2/3) took four of the later
  day-folders and pulled the imperative scripts apart into
  testable, documented functions.
- **Honest claims.** No day is claimed as production-ready. Each
  day folder has its own `requirements.txt` and (where applicable)
  `.env.example`. Generated outputs are gitignored. Secrets are
  read from the environment.
