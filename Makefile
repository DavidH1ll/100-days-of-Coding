.PHONY: help install lint format test test-all test-day clean

help:
	@echo "Common targets:"
	@echo "  install     - pip install -r requirements.txt"
	@echo "  lint        - ruff check ."
	@echo "  format      - ruff format ."
	@echo "  test        - pytest (full suite)"
	@echo "  test-day D  - pytest for a single day, e.g. make test-day D=Day100"
	@echo "  clean       - remove caches (__pycache__, .pytest_cache, .ruff_cache)"

install:
	pip install -r requirements.txt

lint:
	ruff check .

format:
	ruff format .

test:
	pytest -v

test-day:
	pytest "$(D)"/tests -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache
