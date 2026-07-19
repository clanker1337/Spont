# 2. SvelteKit + Svelte 5 + TypeScript Strict

Date: 2026-07-19

## Status

Accepted

## Context

We need a responsive PWA with a server side to hold provider keys, strict typing for safety,
and a fast test/build pipeline. Versions must be stable and mutually compatible.

## Decision

- SvelteKit 2.x with Svelte 5 (runes).
- TypeScript in `strict` mode.
- Zod 4 for runtime validation at boundaries.
- Vitest for unit/integration; Playwright for browser smoke.
- @vite-pwa/sveltekit for the PWA.
- Docker `node:22-alpine` for deployment.
- No database in the MVP.

Exact pinned versions are recorded in `package-lock.json` at scaffold (issue #2/#3) and
verified for compatibility (notably Vitest 4 vs the SvelteKit workspace plugin).

## Consequences

- Server routes (`/api/*`) can hold keys; client never sees them.
- Strong typing reduces provider-boundary mistakes.
- Svelte 5 runes change component authoring vs Svelte 4; team must follow Svelte 5 patterns.

## Alternatives considered

- Plain Vite SPA: rejected (no server side for key safety, no SSR).
- Svelte 4: rejected (older, less future-proof).
- Other PWA plugins: @vite-pwa/sveltekit chosen for SvelteKit integration.
