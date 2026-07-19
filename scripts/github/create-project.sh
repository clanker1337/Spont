#!/usr/bin/env bash
# Best-effort creation of the Spont GitHub Project (Projects V2) with the required
# fields and saved views. Requires `gh` authenticated with project scope and a
# GitHub account/organization that has Projects enabled.
#
# NOTE: Project creation and custom single-select fields require perms this repo's
# token may lack. If this script fails, follow the manual steps printed at the end.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

OWNER="${OWNER:-clanker1337}"
PROJECT_TITLE="${PROJECT_TITLE:-Spont}"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install it and run 'gh auth login'." >&2
  exit 1
fi

echo "Creating project '$PROJECT_TITLE' for $OWNER ..."
PROJECT_URL=$(gh project create --owner "$OWNER" --title "$PROJECT_TITLE" 2>&1) || {
  echo "Project creation failed (likely permissions). Manual steps:"
  echo "  1. GitHub > Org/User > Projects > New project (Board)."
  echo "  2. Add custom single-select fields: Status, Priority, Size, Area, Release."
  echo "  3. Add date fields: Target date; text field: Blocked reason."
  echo "  4. Create saved views: Current milestone, Kanban board, Product roadmap,"
  echo "     Provider work, Bugs, Blocked work, Recently completed."
  echo "  5. Add issues from the backlog to the project."
  exit 1
}
echo "$PROJECT_URL"

# Status options
for v in Backlog Ready "In progress" "In review" Blocked Done; do
  gh project field-create "$PROJECT_TITLE" --owner "$OWNER" --name "Status" \
    --data-type "single select" --single-select-option "$v" 2>/dev/null || true
done
# Priority
for v in P0 P1 P2 P3; do
  gh project field-create "$PROJECT_TITLE" --owner "$OWNER" --name "Priority" \
    --data-type "single select" --single-select-option "$v" 2>/dev/null || true
done
# Size
for v in XS S M L XL; do
  gh project field-create "$PROJECT_TITLE" --owner "$OWNER" --name "Size" \
    --data-type "single select" --single-select-option "$v" 2>/dev/null || true
done
# Area
for v in Product Frontend Domain Engine Providers Testing Infrastructure Documentation; do
  gh project field-create "$PROJECT_TITLE" --owner "$OWNER" --name "Area" \
    --data-type "single select" --single-select-option "$v" 2>/dev/null || true
done
# Release
for v in MVP "Post-MVP"; do
  gh project field-create "$PROJECT_TITLE" --owner "$OWNER" --name "Release" \
    --data-type "single select" --single-select-option "$v" 2>/dev/null || true
done

echo "Project created. Add the backlog issues to it via the web UI or 'gh project item-add'."
echo "Then create the saved views: Current milestone, Kanban board, Product roadmap,"
echo "Provider work, Bugs, Blocked work, Recently completed."
