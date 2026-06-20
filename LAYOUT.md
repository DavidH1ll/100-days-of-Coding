# Repository Layout

The standard structure for a day folder in this repository. Existing
days have a range of legacy layouts from the 100-day learning arc;
this document defines the target for **new** days and for refactors
of existing days. **Day 100 (`Day100_Earnings_Predictor/`) is the
model citizen** — it follows this layout end to end.

## Python script (default)

```
DayXXX_Name/
├── main.py or <descriptive_name>.py   # entry point with functions + __main__ guard
├── README.md
├── requirements.txt
├── .env.example                       # only if the project uses secrets / API keys
├── conftest.py                        # only if the project has tests
└── tests/                             # only if the project has tests
    └── test_<module>.py
```

Example: `Day100_Earnings_Predictor/`.

## Flask app

```
DayXXX_Name/
├── main.py                            # Flask entry point
├── templates/                         # Jinja templates (source, must be tracked)
├── static/                            # static assets (optional)
├── README.md
├── requirements.txt
├── .env.example
└── tests/                             # optional
    └── test_*.py
```

Example: `Day069_Blog_Users_Comments/`. Note that `templates/*.html` are
**source files** and must remain tracked — they are not generated
output.

## Data science / notebook

```
DayXXX_Name/
├── <descriptive_name>.py              # the analysis script
├── README.md
├── requirements.txt
├── figures/                           # generated PNGs / HTMLs (gitignored)
└── tests/                             # optional
    └── test_*.py
```

Example (after refactor): `Day080_House_Price_Predictor/`. Generated
visualisations go in `figures/`, which is gitignored via the
`*.png` / `*.html` rules in `.gitignore`.

## File conventions

- **Python file names**: `snake_case` (e.g. `calculator.py`, not
  `Calculator.py`). Day folders are `DayNNN_Name` with a capital `D`
  and underscore separator.
- **`main.py` vs descriptive name**: a single-file project can use
  `main.py`. Multi-module or "headline" projects should use a
  descriptive name (e.g. `house_price_predictor.py`,
  `earnings_predictor.py`).
- **`README.md`**: explain what the project does, how to run it
  (the exact command), and any required setup. The template is up
  to the project but at minimum should have an Overview section.
- **`requirements.txt`**: project-specific dependencies. Do not
  duplicate the root `requirements.txt`.
- **Generated outputs**: PNGs, interactive HTMLs, and CSVs go in a
  subfolder (`figures/`, `output/`, `data/`) so they're easy to
  gitignore and don't pollute the day root.
- **API keys / secrets**: copy `.env.example` to `.env` and fill in
  values locally. **Never commit a real `.env`** — the root
  `.gitignore` already protects against this.

## Code conventions (in `house_price_predictor.py`, etc.)

- **Functions over top-level scripts**: split into named functions
  with single responsibilities. Use a `run_pipeline()` orchestrator
  and `if __name__ == "__main__":` guard.
- **Type hints**: add them. Even on tutorial code they make the
  intent clear.
- **Docstrings**: one line on every function; Args/Returns where
  useful.
- **`pathlib.Path`** instead of string paths. Avoid hardcoded
  `DayXXX/...` strings that depend on the current working directory.
- **Constants at the top** (RANDOM_STATE, file paths, hyperparameter
  grids). Makes them easy to tweak and easy to mock in tests.
- **Suppress warnings narrowly**. `warnings.filterwarnings("ignore")`
  blanket is bad — scope to the specific warning class you mean.

## Testing conventions

- **pytest**. Tests live in a `tests/` subfolder.
- **Conftest**: if tests need to import the project's main module,
  add a `conftest.py` at the day root that inserts the day folder
  into `sys.path`. This avoids requiring the project to be installed
  as a package.
- **Fast**: tests should run in seconds, not minutes. Use small `n`
  parameters for synthetic data, small param grids for
  `GridSearchCV`, and small `cv` values.
- **One assertion per test** is a guideline, not a rule. Group
  related assertions in the same test if they all verify one thing
  (e.g. "model fits and predicts in expected range").
- **No flaky tests**: never depend on real network, real time, or
  random ordering without seeding.

## Why this exists

The 100 day folders were written over 100 consecutive days as
tutorial exercises. The earlier days follow whatever pattern the
tutorial prescribed; the later days reflect accumulated habits. A
**single documented standard** means new days and refactors of
existing days have a target, and reviewers can navigate the repo
consistently. Existing days are kept as-is unless explicitly
refactored — the goal is incremental improvement, not a forced
migration of 100 folders.
