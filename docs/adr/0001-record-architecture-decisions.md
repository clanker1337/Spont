# 1. Record Architecture Decisions

Date: 2026-07-19

## Status

Accepted

## Context

Spont is a new project. We need a consistent way to record material technical and product
decisions so future work can rely on them and changes go through review.

## Decision

We will record architecture decisions as Architecture Decision Records (ADRs) in `docs/adr/`,
numbered sequentially starting at 0001. Each ADR uses this template:

- Title: `<number>-<kebab-subject>.md`
- Sections: Status, Context, Decision, Consequences, Alternatives considered
- Status values: Proposed, Accepted, Deprecated, Superseded (by `<number>`)

Foundational tooling and provider choices require an ADR before implementation. Changes to an
accepted ADR create a new ADR that supersedes the old one; the old file's status is updated.

## Consequences

- Decisions are reviewable and traceable.
- No untracked architectural change: a PR that changes foundational behavior must update or add
  an ADR.
- The lockfile pins versions; material version/tooling changes are recorded here.

## Alternatives considered

- Wiki / docs prose only: rejected because it scatters decisions and lacks a stable index.
- Commit messages only: rejected because they are poor for long-form rationale and discovery.
