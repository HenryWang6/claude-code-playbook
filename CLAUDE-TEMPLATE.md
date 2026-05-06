# [Project Name]
> [One sentence: what this does and who it's for]

## Tech Stack
- [language / framework / platform]
- [key dependencies]
- Build: [build tool]

## Conventions
- [code style, patterns, naming rules]
- [testing conventions]
- [commit message style]

## Key Paths
- [src/] — [what's here]
- [tests/] — [what's here]
- [docs/] — [what's here]

## Scope
- [what the project does — features, outputs, supported use cases]
- [what's explicitly out of scope — no server, no auth, etc.]
<!-- When scope changes: update this list. Save the *reason* to project memory (if only Claude needs it) or docs/decisions/ (if the team needs it too). -->

## Active Decisions
- [things we're reconsidering, on hold, or actively debating]
- [keep this short — 2-3 lines. Update as priorities shift.]
<!-- For settled architecture decisions with full rationale, write them up in docs/decisions/ (version-controlled, team-visible). -->

## Constraints
- [things that must NOT be changed]
- [external systems that must stay compatible]

---

## Claude Code Workflow (shared across all projects)

### Decision triggers

| When | Then |
|------|------|
| New feature, >2 files, or architectural choice | **Plan Mode** — design first, code after approval |
| 3+ distinct steps | **TaskCreate** — track each step, use dependencies |
| Need to search/explore codebase | **Explore Agent** (don't guess file paths) |
| Multi-step research spanning many files | **general-purpose Agent** |
| Implementation done | **Review** — check edge cases, security, over-engineering |
| Scope or priorities changed | **Update CLAUDE.md** `## Scope` / `## Active Decisions` — keep it lightweight (2-3 lines) |
| Settled an architecture decision | **Write an ADR** in `docs/decisions/` with full rationale — litmus test: would another dev need this? |
| User corrects approach or gives feedback | **Save to Memory** immediately |
| User says "remember X" | **Save to Memory** immediately |

### Anti-patterns to avoid
- Don't Plan Mode for trivial fixes (typo, single-line change)
- Don't mock in tests unless the user explicitly approves it
- Don't over-engineer — three similar lines > premature abstraction
- Don't add error handling for scenarios that can't happen
- Don't create docs/README unless asked (docs/decisions/ ADRs are the exception — create those when architecture decisions settle)

### Commit style
- `<type>: <short description>` — type is feat/fix/chore/docs/refactor/test
- Body explains *why*, not *what*
- Append `Co-Authored-By: Claude Code <noreply@anthropic.com>`
