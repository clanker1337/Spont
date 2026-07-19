# Scoring and Filtering

All filtering and scoring are deterministic pure functions over normalized domain types.
Score components are returned in development mode for transparency. Rating alone must not
dominate recommendations.

## Hard constraints (reject the candidate)

- Will be closed before arrival.
- Will close before the activity can reasonably finish.
- Event starts too late or ends outside the available window.
- Plan cannot finish within available time.
- Minimum estimated cost exceeds budget.
- One-way travel time exceeds the user's stated maximum.
- Weather makes the activity unreasonable (see weather policy).
- Required information missing to the point the plan is not actionable.

Uncertain values may produce warnings or penalties instead of rejection when they do not
justify rejection.

## Preliminary scoring (before routing)

Cheap signals only (no travel-time yet): preference match, category match, energy match,
rating/review confidence, novelty, weather suitability, open-now confidence, cost confidence,
minus missing-data and duplicate-category penalties. Used to pick the ~12 candidates to route.

## Final scoring (after routing)

Positive factors (weights in code, documented here):
- preference match
- activity-category match
- energy-level match
- rating confidence
- review confidence
- novelty
- weather suitability
- open-now confidence
- cost confidence

Negative factors:
- travel-time penalty
- budget risk
- schedule risk
- missing-data penalty
- duplicate-category penalty
- low-confidence penalty

Weights are constants in `engine/scoring.ts`; unit tests pin their effect. No single factor
may dominate; rating contributes a bounded share.

## Weather policy (pure functions, unit-tested)

- Heavy rain rejects unsheltered outdoor activities.
- High heat penalizes exposed midday activities.
- Strong wind penalizes exposed overlooks, waterfronts, and cycling.
- Good conditions boost parks, trails, scenic walks, and outdoor markets.

Weather affects eligibility and ranking, not merely display.

## Diversity selection (exactly three)

The three recommendations must not be minor variations of the same activity. Category and
experience diversity rules apply. Roles:
- Plan 1: highest total viable score
- Plan 2: best low-cost or low-friction viable option
- Plan 3: highest-novelty viable option

If fewer than three strong plans exist, return the best viable plans plus an explicit
structured insufficiency result. Never invent places.
