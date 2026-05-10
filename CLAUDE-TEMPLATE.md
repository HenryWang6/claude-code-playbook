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
- [ARCHITECTURE.md] — project map (recommended if 50+ files)

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
| New feature, unclear scope or architecture | **Architect subagent** — produces SPEC.md + TODO.md, writes no code |
| New feature, scope is clear, >2 files | **Plan Mode** — design first, code after approval |
| SPEC.md exists, TODO.md has unchecked items | **Developer subagent** — implements one task at a time with micro-verification |
| Developer completed tasks, want independent QA | **Reviewer subagent** — runs tests, appends review to DONE.md |
| 3+ distinct steps | **TaskCreate** — track each step, use dependencies |
| Starting a new task | **Read project map first** (CLAUDE.md Key Paths, ARCHITECTURE.md, or file tree), then target only the files you need |
| Need to search/explore codebase | **Explore Agent** (don't guess file paths) |
| Multi-step research spanning many files | **general-purpose Agent** |
| Completed a logical unit of code | **Micro-verify** — run the lightest check that catches errors at this boundary before moving on |
| Same verification fails 3 times | **Stop and report** — do not guess alternative fixes; report what was tried and ask for guidance |
| Implementation done | **Review** — check edge cases, security, over-engineering |
| Scope or priorities changed | **Update CLAUDE.md** `## Scope` / `## Active Decisions` — keep it lightweight (2-3 lines) |
| Settled an architecture decision | **Write an ADR (Architecture Decision Record)** in `docs/decisions/` with full rationale — litmus test: would another dev need this? |
| User corrects approach or gives feedback | **Save to Memory** immediately |
| User says "remember X" | **Save to Memory** immediately |

### Anti-patterns to avoid
- Don't Plan Mode for trivial fixes (typo, single-line change)
- Don't mock in tests unless the user explicitly approves it
- Don't over-engineer — three similar lines > premature abstraction
- Don't add error handling for scenarios that can't happen
- Don't create docs/README unless asked
- Don't verify only at the end — verify each logical unit before moving on. The bug should be in the code you just wrote, not spread across the last 200 lines.

### Commit style
- `<type>: <short description>` — type is feat/fix/chore/docs/refactor/test
- Body explains *why*, not *what*
- Append `Co-Authored-By: Claude Code <noreply@anthropic.com>`
