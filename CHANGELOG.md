# Changelog

All notable changes to this repository are recorded here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- 119 pytest tests across 6 day folders (Day 037, 066, 080, 081, 096, 100).
- `ruff` lint and format on every commit (pre-commit) and every push (CI).
- Generated outputs in `figures/` and `data/`, gitignored.
- `LAYOUT.md` defining the standard structure for day folders.
- `HIGHLIGHTS.md` tour of the polished projects.
- `.env.example` templates for Day 032, 033, 035, 036, 037, 038, 039,
  046, 047, 083, 087, 095, 096.
- GitHub Actions CI workflow (Python 3.11, ruff, pytest).
- `pre-commit-config.yaml` with ruff and standard hooks.

### Changed
- Renamed all 100 day folders to include descriptive project names
  (e.g. `Day081_Typing_Speed_Test`).
- Refactored Day 100 capstone from a 190-line top-level script into
  12 typed, documented functions.
- Refactored Day 080 (House Price Predictor) into 13 typed functions.
- Refactored Day 081 (Typing Speed Test): renamed
  `typing_speed_test.py` to `main.py`, extracted scoring into
  `scoring.py`.
- Refactored Day 066 (Cafe REST API): replaced manual `requests`-based
  `test_api.py` with proper pytest `test_client` tests.
- Refactored Day 096 (Online Shop): added 17 pytest tests.
- Refactored Day 037 (Pixela Tracker): CRLF+tabs → LF+spaces, added
  19 pytest tests.

### Removed
- Tracked generated outputs (22 PNGs from Day 072-080, 9 Plotly HTMLs
  from Day 075/078).
- Junk file `config/data.txt`.
