# 6. No Database; Demo Mode Required

Date: 2026-07-19

## Status

Accepted

## Decision

- The MVP uses no database; all state is request-scoped or client-side.
- The application MUST run end-to-end in demo mode with zero provider credentials, using
  deterministic in-repo fixture adapters.

## Consequences

- Simpler deployment; no stateful infrastructure in MVP.
- CI runs in demo mode and never needs secrets or live network.
- Live behavior is opt-in via server-side keys; fixture behavior is the default and the test
  baseline.

## Alternatives considered

- Local SQLite for caches: rejected for MVP (adds ops surface; not required by product).
- Demo mode as optional: rejected (must be the default so the app is always runnable).
