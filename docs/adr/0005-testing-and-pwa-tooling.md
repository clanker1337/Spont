# 5. Testing and PWA Tooling

Date: 2026-07-19

## Status

Accepted

## Decision

- Vitest 4.x for unit + integration tests (workspace plugin for SvelteKit); pin after verifying
  compatibility with the SvelteKit Vite plugin.
- Playwright for browser smoke tests (separate from Vitest).
- @vite-pwa/sveltekit for the installable PWA (manifest + service worker).
- All provider tests use fixtures; live APIs are never called in CI.

## Consequences

- Deterministic, fast unit/integration suite; CI needs no secrets.
- PWA works offline for cached assets; provider calls still require network in live mode.
- Playwright adds a browser download in CI (cached).

## Alternatives considered

- Jest: rejected (SvelteKit/Vitest integration is first-class).
- vitest browser mode for e2e: rejected in favor of Playwright for true browser smoke.
- Manual PWA setup: rejected (plugin reduces boilerplate and SSR pitfalls).
