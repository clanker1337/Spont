#!/usr/bin/env bash
# Import the Spont backlog into GitHub.
# Requires write access: run `gh auth login` first (or export GITHUB_TOKEN with issues scope).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python3 scripts/github/import_issues.py "$@"
