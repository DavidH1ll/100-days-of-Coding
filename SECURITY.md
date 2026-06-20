# Security Policy

## Supported Versions

This repository documents learning projects built across 100 days.
The day folders are tutorial artefacts and are not maintained as
production code — security fixes are applied on a best-effort basis
to the most recent commit on `main`.

| Branch  | Supported          |
|---------|--------------------|
| `main`  | :white_check_mark: |
| older   | :x:                |

## Reporting a Vulnerability

If you have found a vulnerability **in the repository itself** (for
example: a real API key that was committed, a `.env` file in the
working tree, or a secret accidentally included in a code sample) —
please report it privately:

- **Email:** open a private security advisory at
  <https://github.com/DavidH1ll/100-days-of-Coding/security/advisories/new>
- **What to include:** the path of the file, the line number, and a
  short description of the issue.

You should **not** open a public issue for security problems.

## Notes on Day-Folder Code

Some day folders use placeholder strings such as `your_password` or
`YOUR_CLIENT_ID`. These are intentional examples, not real secrets.
If you find a real secret committed to the repo, please follow the
reporting process above.

If you have committed a personal API key to a fork or branch of this
project, follow your provider's revocation process immediately (for
example, regenerate the key in their dashboard) and then remove it
from history with `git filter-repo` or the BFG.
