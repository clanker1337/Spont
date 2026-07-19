# Contributing to Spont

Spont uses GitHub as the authoritative system of record. Issues and pull requests track all work.

## Before you code

1. Find or create the relevant issue and read its acceptance criteria, scope, and non-goals.
2. Check dependencies and any blocked reason on the GitHub Project.
3. Sync `main` and create a branch: `issue-<number>-<short-description>`.
4. Never implement substantial work directly on `main`.

## Implementation rules

- Implement only the issue's scope. Split work into small, reviewable PRs.
- Keep provider-specific response types inside the adapter boundary.
- The plan engine must stay deterministic and independently testable.
- Do not send raw provider results to an LLM for plan selection.
- No credentials or secrets in the repo. Server keys live in `.env` (gitignored),
  accessed only via SvelteKit `$env/dynamic/private`.
- Update documentation in the same PR that changes behavior.

## Commits and pull requests

- Use clear imperative commit messages ("feat: add hard-constraint filter").
- Open a PR with `Closes #<issue-number>`, a summary, test evidence, and known limitations.
- Add screenshots for visual changes.
- Wait for required CI checks before merging.
- Prefer squash merge. Delete the branch after merge.
- Deferred work must become a new issue, not a TODO comment.

## Local verification (run before pushing)

    npm run format
    npm run lint
    npm run check
    npm run test
    npm run build
    npm run test:e2e    # when UI changed

Do not claim a check passes unless you actually ran it.

## Demo mode

The app must run with no provider credentials using deterministic fixtures. CI runs in demo
mode so it never depends on live APIs or secrets.

## Definition of done

Acceptance criteria met, required tests pass, CI passes, error/loading states handled,
accessibility considered, no secrets committed, docs current, PR closes the issue, deferred
work has its own issue, and the GitHub Project status is updated.
