# Spont

Spont is a location-aware, spontaneous-plan generator. Given where you are, how much
time and money you have, how far you are willing to travel, and current conditions, Spont
returns exactly three complete, immediately actionable plans you can begin now:

1. Best overall match
2. Lowest-cost / lowest-friction option
3. Most unusual viable option

It is not a generic nearby-business directory. Every plan includes departure/arrival/return
times, travel time, activity duration, cost or cost range, indoor/outdoor classification,
opening confidence, weather implications, reasons it was selected, and warnings.

## Status

Milestone M0 (Repository and planning) in progress. Application implementation has not started.
See `docs/product/PRD.md`, `docs/architecture/`, and `docs/adr/` for the full design.

## Tech stack

- SvelteKit (2.x) + Svelte 5
- TypeScript (strict mode)
- Zod (runtime validation)
- Vitest (unit + integration)
- Playwright (browser smoke tests)
- @vite-pwa/sveltekit (progressive web app)
- Docker (deployment)
- No database in the MVP

## Quick start (demo mode, no API keys)

    npm install
    npm run dev

Demo mode runs entirely on deterministic in-repo fixtures. No provider credentials are
required. To enable live providers, copy `.env.example` to `.env` and set the server-only
keys (see `docs/runbooks/local-development.md`).

## Common scripts

    npm run dev          # local dev server
    npm run check        # svelte-check (type checking)
    npm run lint         # eslint
    npm run format       # prettier
    npm run test         # vitest unit + integration
    npm run test:e2e     # playwright smoke tests
    npm run build        # production build

## Repository conventions

- Branch format: `issue-<number>-<short-description>`
- Every PR includes `Closes #<issue-number>`, test evidence, and known limitations.
- Work is tracked on GitHub Issues and the GitHub Project; main is protected.
- See `.hermes.md`, `CONTRIBUTING.md`, and `SECURITY.md` for full standards.

## Documentation map

- Product: `docs/product/PRD.md`
- Architecture: `docs/architecture/system-overview.md`, `provider-strategy.md`, `scoring-and-filtering.md`
- Decisions: `docs/adr/`
- Runbooks: `docs/runbooks/local-development.md`
- Issue backlog (importable): `docs/planning/issue-backlog.json`

## License

MIT — see `LICENSE`.
