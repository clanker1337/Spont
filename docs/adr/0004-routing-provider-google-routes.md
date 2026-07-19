# 4. Routing Provider — Google Routes (over Mapbox)

Date: 2026-07-19

## Status

Accepted

## Context

Travel-time lookup is needed for shortlisted candidates across drive/walk/bike/transit. The
spec allows Google Routes or Mapbox; the choice must be recorded.

## Decision

Use Google Routes API.

## Consequences

- Single vendor/key surface with Places and Geocoding; one server-side credential pattern.
- Supports all required travel modes (`DRIVE`, `WALK`, `BICYCLE`, `TRANSIT`) with
  `routingPreference` and traffic awareness.
- Avoids introducing a second provider's SDK, key, and response shape into the MVP.

## Alternatives considered

- Mapbox Directions/Routing: cheaper per request and has a matrix endpoint, but adds a second
  credential and a different coordinate/response model. Deferred; can be added later behind the
  same `RoutingProvider` interface if cost becomes a concern.
