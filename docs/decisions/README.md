# Architecture Decision Records (ADRs)

This directory holds settled architecture decisions with full rationale — version-controlled, team-visible, and read by Claude when the topic area surfaces.

## When to write an ADR

Use the litmus test: *"Would another developer joining tomorrow need to know why we made this choice?"*

If yes → write an ADR here. If only Claude needs to know (e.g., personal workflow preferences) → save to Claude Memory instead.

For lightweight, in-progress state (what we're building right now, what's being reconsidered), use `## Scope` and `## Active Decisions` in [CLAUDE.md](../../CLAUDE.md).

## Template

```markdown
# [Title]

- **Status:** proposed / accepted / deprecated / superseded
- **Date:** YYYY-MM-DD

## Context

What problem are we solving? What constraints are we working within?

## Decision

What did we choose and why? What alternatives did we reject?

## Consequences

What got easier? What got harder? What's the migration path?
```

## Example

```markdown
# Use SQLite for local storage

- **Status:** accepted
- **Date:** 2026-05-06

## Context

Need persistent local storage for a single-machine CLI tool. No concurrent writes, dataset fits in memory.

## Decision

Use SQLite. Rejected Postgres (overkill for single-machine), rejected JSON files (no query support).

## Consequences

- Easier: zero setup, single file, no daemon
- Harder: limited to single-writer, no horizontal scaling path
```

Keep each ADR focused on one decision. If a decision changes, mark the old one as `superseded` and link to the replacement.
