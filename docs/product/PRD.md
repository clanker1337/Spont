# Product Requirements Document — Spont

## Objective

Answer: "Given where I am, how much time and money I have, how far I am willing to travel,
and current conditions, give me exactly three plans I can begin now."

Each plan is complete and immediately actionable, not a generic list of nearby places.

## Users

People who want a concrete thing to do right now near them, within their constraints,
without researching options themselves.

## User inputs

The interface collects:

- Starting location (current browser location, typed city/neighborhood/address, or a chosen map point)
- Available time
- Maximum one-way travel time
- Transportation mode (walk, bike, drive, transit)
- Budget
- Indoor / outdoor / either
- Energy level
- Preferred activity categories
- Number of people

Precise location is not mandatory.

## MVP output

Exactly three distinct plans:

1. Best overall match
2. Lowest-cost or lowest-friction option
3. Most unusual viable option

Each plan includes:

- Plan title
- Destination
- Concise activity description
- Departure time
- Estimated arrival time
- Expected return time
- Travel time
- Activity duration
- Estimated cost or cost range
- Indoor/outdoor classification
- Current opening confidence
- Weather implications
- Reasons it was selected
- Warnings or uncertainty
- Navigation action

The first release produces single-destination plans only. Multi-stop composition is later.

## Pipeline (high level)

1. Validate user input
2. Resolve origin coordinates
3. Query 5–8 relevant place-category groups
4. Normalize raw results
5. Deduplicate candidates
6. Apply inexpensive hard constraints
7. Apply approximate distance filtering
8. Score preliminary candidates
9. Route only the strongest candidates (target max 12)
10. Apply travel-time, schedule, weather, and budget constraints
11. Generate exactly three diverse plans
12. Return warnings and confidence

Raw provider results are never sent to an LLM for selection. The engine is deterministic.

## Non-goals (MVP)

- User accounts, social features, reservations, purchases
- Worldwide transit routing, multi-day planning, multi-stop optimization
- Recommendation history
- Event-site scraping, AI-generated reviews
- Ticketmaster events and preference history are post-MVP (M7, M8)

## Success metrics (MVP)

- Returns exactly three viable plans when strong candidates exist
- Returns an explicit structured insufficiency result when fewer than three exist
- Never invents places, times, costs, or ratings
- Runs end-to-end in demo mode with no credentials
- Hard constraints never produce an unactionable plan

## Open questions

- How to weight novelty vs. preference match for "most unusual" (see scoring ADR/runbook)
- Whether to surface a 4th "wildcard" plan when diversity is thin (deferred)
