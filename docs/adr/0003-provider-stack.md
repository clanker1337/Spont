# 3. Provider Stack

Date: 2026-07-19

## Status

Accepted

## Context

We need geocoding, places, routing, and weather. Provider choices affect cost, key handling,
and compatibility, and must be recorded.

## Decision

- Places: Google Places API (New) — Nearby Search (New) + Place Details (New).
- Geocoding: Google Geocoding API (same vendor).
- Routing: Google Routes API (see ADR-0004).
- Weather: Open-Meteo (no key required).
- Events: Ticketmaster (post-MVP, M7).
- Demo/fixture adapters for every provider so the app runs with zero credentials.

## Consequences

- One commercial vendor (Google) for geocoding/places/routing simplifies key handling and
  billing; Open-Meteo removes a key for weather.
- Live adapters are server-side only.
- Nominatim is explicitly excluded as the primary POI discovery system.

## Alternatives considered

- Legacy Google Places: rejected (deprecated for new projects).
- Mapbox for routing: rejected for MVP (see ADR-0004).
- Nominatim as primary POI: rejected (not for systematic discovery, rate/ToS limits).
- Other weather APIs (keyed): rejected in favor of keyless Open-Meteo.
