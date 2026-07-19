# System Overview

## Principles

- Discovery and plan generation are separate concerns.
- Provider-specific response types never escape the provider adapter.
- The plan engine is deterministic and independently testable.
- Raw provider results are never sent to an LLM for plan selection.
- The app runs in demo mode with zero credentials.
- Secrets are server-side only.

## Layers

1. User interface (Svelte components, forms, results, map)
2. Application orchestration (search controller, pipeline)
3. Domain models (normalized types)
4. Deterministic filtering and scoring (pure functions)
5. Plan generation (diversity selection)
6. Provider interfaces (Geocoding, Places, Events, Weather, Routing)
7. Provider adapters (live + deterministic fixture implementations)

## Source layout

    src/
      lib/
        components/      # UI components
        domain/         # normalized types
        engine/         # pipeline, filters, scoring, selection
        providers/      # interfaces + adapters (google, open-meteo, demo, map)
        server/         # server-only proxy endpoints, env, key handling
        stores/         # client state
        utilities/      # pure helpers (time, geo, formatting)
      routes/
        api/            # server endpoints that hold provider keys
    tests/              # unit + integration
    docs/
      adr/  product/  architecture/  runbooks/
    .github/            # CI, templates, CODEOWNERS

## Data flow (request)

UI -> validate SearchConfiguration (Zod) -> orchestrator -> Geocoding (resolve origin)
-> Places (nearby, 5–8 categories) -> normalize + dedupe -> hard constraints
-> approximate distance filter -> preliminary score -> Routing (route top ~12)
-> travel/schedule/weather/budget constraints -> final score -> diversity selection (3 plans)
-> UI. Each provider call is behind an interface; live and fixture adapters are swappable
via configuration (demo mode uses fixtures).

## Provider boundary

Adapters convert external responses into normalized domain types and validate them with Zod
at the boundary. They map transport errors into a typed `ProviderError`. Timeouts and limited
retries are handled inside the adapter. The rest of the system depends only on interfaces and
domain types.

## Demo mode

With no provider credentials configured, the orchestrator selects fixture adapters. All test
suites use fixtures; CI runs in demo mode so it never needs secrets or live network.

## Deployment

SvelteKit Node adapter packaged in Docker (`node:22-alpine`). HTTPS in deployed environments.
No database. Provider keys injected as environment variables at runtime, never baked in.
