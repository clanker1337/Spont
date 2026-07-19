# Provider Strategy

Every provider has: an interface, a live adapter, a deterministic fixture/demo adapter,
boundary schema validation (Zod), typed error mapping, timeout handling, and limited retries.
Tests use fixtures, never live APIs. Public Nominatim is NOT used for systematic POI discovery.

## Geocoding — Google Geocoding API

- Role: forward geocode of typed city/neighborhood/address; reverse geocode for map-point label.
- Why Google: single vendor with Places/Routing; consistent server-side key handling.
- Live adapter: calls Geocoding API server-side; validates with Zod; maps errors to ProviderError.
- Fixture adapter: in-repo dataset of known places for demo/offline.
- ADR: docs/adr/0003-provider-stack.md

## Places — Google Places API (New)

- Role: Nearby Search (New) for candidate discovery; Place Details (New) for hours, rating,
  price level, and geometry.
- Why (New) over Legacy: Legacy is deprecated for new projects; (New) returns richer fields
  and is future-proof. Verify current field names/pricing at adapter build (issue #12).
- Live adapter: server-side; boundary validation; typed errors; timeout + limited retries.
- Fixture adapter: captured sample responses normalized into domain candidates.
- ADR: docs/adr/0003-provider-stack.md

## Routing — Google Routes API (selected over Mapbox)

- Role: travel-time and route lookup for shortlisted candidates (drive/walk/bike/transit).
- Why Google Routes: one vendor/key surface with Places; all required travel modes;
  server-side only. Mapbox is cheaper but adds a second credential and a different response
  shape; rejected for MVP.
- Live adapter: server-side; validates; typed errors; timeout + limited retries.
- Fixture adapter: precomputed travel times keyed by origin/destination/mode.
- ADR: docs/adr/0004-routing-provider-google-routes.md

## Weather — Open-Meteo

- Role: current + short-horizon forecast to drive eligibility and ranking.
- Why Open-Meteo: free, no API key, CORS-friendly, ideal for both live and fixture paths.
- Live adapter: server-side call (keyless); validate fields/units at boundary (issue #19).
- Fixture adapter: static forecast samples.
- ADR: docs/adr/0003-provider-stack.md

## Events — Ticketmaster (POST-MVP, M7)

- Added only after the core places-based MVP works. Same interface/adapter contract.

## Selection & configuration

- Adapters are injected. Demo mode (no credentials) selects fixture adapters.
- Live adapters are chosen when their server-side key is present.
- Provider selection and failures degrade gracefully (see issue #26).
