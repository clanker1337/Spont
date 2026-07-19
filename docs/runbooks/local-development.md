# Local Development Runbook

## Prerequisites

- Node.js 22.x
- npm 10.x (pnpm not required)
- Docker (for container builds)
- Optional: `gh` CLI for GitHub issue import

## Install

    npm install

This installs from the committed lockfile.

## Develop (demo mode, no keys)

    npm run dev

Demo mode uses deterministic fixture providers. No `.env` needed.

## Enable live providers (optional)

Copy the example and set server-only keys:

    cp .env.example .env

    # .env (server-side only, gitignored)
    GOOGLE_PLACES_API_KEY=...
    GOOGLE_GEOCODING_API_KEY=...
    GOOGLE_ROUTES_API_KEY=...

Keys are read via SvelteKit `$env/dynamic/private` inside `/api/*` server endpoints. They are
never exposed to the browser.

## Quality gates (run before pushing)

    npm run format      # prettier --write
    npm run lint        # eslint
    npm run check       # svelte-check (types)
    npm run test        # vitest unit + integration
    npm run build       # production build
    npm run test:e2e    # playwright smoke (after UI exists)

CI runs the same gates in demo mode and does not require secrets.

## Docker

    docker build -t spont .
    docker run -p 3000:3000 --env-file .env spont

HTTPS must terminate in front of the container in deployed environments.

## Creating the GitHub backlog

If `gh` is authenticated with write access:

    bash scripts/github/import-issues.sh

This creates labels, milestones, and the 32 backlog issues from
`docs/planning/issue-backlog.json`.
