# Contributing to 100 Days of Coding

Thank you for your interest in contributing to this learning project! 🎉

## About This Repository

This is a personal learning repository documenting my journey through 100 days of Python programming. While it's primarily for my own education, I welcome contributions that can help improve the code quality and documentation.

## How You Can Contribute

### 🐛 Bug Reports
If you find a bug in any of the projects:
1. Check if the issue already exists
2. Open a new issue with:
   - Day number and project name
   - Description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Your Python version and OS

### 💡 Suggestions
I appreciate suggestions for:
- Code improvements and refactoring
- Better practices and patterns
- Documentation enhancements
- Additional features for existing projects

### 📝 Documentation
Help improve documentation by:
- Adding missing README files for early days
- Fixing typos and clarifying instructions
- Adding more detailed setup guides
- Creating visual aids (screenshots, diagrams)

### 🔧 Code Quality
Suggestions for:
- Better error handling
- Code optimization
- Following Python best practices (PEP 8)
- Security improvements

## Contribution Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b improvement/description
   ```
3. **Make your changes**
4. **Test your changes** (ensure the code still works)
5. **Commit with clear messages**
   ```bash
   git commit -m "Day036: Improve error handling in stock_api.py"
   ```
6. **Push to your fork**
   ```bash
   git push origin improvement/description
   ```
7. **Open a Pull Request** with:
   - Clear description of changes
   - Which day(s) it affects
   - Why the change is beneficial

## Code Standards

- Follow PEP 8 style guide
- Add docstrings to functions and classes
- Include comments for complex logic
- Use type hints where appropriate
- Keep functions focused and small

## Project Layout

See [`LAYOUT.md`](LAYOUT.md) for the standard structure for day
folders. The short version: descriptive Python file names, type
hints and docstrings, a `tests/` subfolder with pytest, generated
outputs in `figures/`, and secrets in `.env` (not committed).

The tool config lives at the repo root:

- `pyproject.toml` — ruff config + pytest config
- `.pre-commit-config.yaml` — pre-commit hooks
- `.github/workflows/ci.yml` — CI (ruff + pytest on push and PR)

Run `pre-commit install` once to enable local checks.

## What I'm NOT Looking For

- Complete rewrites (this is a learning journey)
- Adding new days (I'll do those myself)
- Major architectural changes without discussion

## Questions?

Open an issue with the label `question` and I'll respond as soon as I can.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping me learn and improve! 
