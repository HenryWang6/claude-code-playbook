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
<!-- For larger projects (50+ files): add an ARCHITECTURE.md or project map file listing each module with a one-line description. -->

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
| Starting work in an unfamiliar module | **Read project map first** (CLAUDE.md Key Paths, ARCHITECTURE.md, or file tree), then target only the files you need |
| Completed a logical unit of code | **Micro-verify** — run the lightest check that catches errors at this boundary before moving on |
| Same verification fails 3 times | **Stop and report** — do not guess alternative fixes; report what was tried and ask for guidance |
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
- Don't verify only at the end — verify each logical unit before moving on. Feedback radius must be smaller than your diagnostic range.

### Micro-Verification Loops

Verify after each independently testable logical unit — a function, a component, an API endpoint. Not an arbitrary line count.

Litmus test: **"If this verification fails, can I pinpoint the cause in 10 seconds?"** If no, split the unit further.

Verification progression: compile/type-check → run the single unit → full test suite. Never skip a stage. Circuit breaker: 3 consecutive failures on the same unit → stop and report.

A task is DONE when all verifications pass, not when the code is written.

See [Best Practices](CLAUDE-CODE-BEST-PRACTICES.md#37-test-driven-ai-agent-tdd-for-agents) for language-specific examples and Iron Triangle integration.

### Repository Mapping (Two-Step Fetch)

Before reading source files, read the project map first:

1. **Orient:** CLAUDE.md `## Key Paths` and `## Scope`, or directory listing
2. **Target:** State which files you need — then read only those files

Goal: prevent attention dilution. Don't dump irrelevant files into context.

See [Best Practices](CLAUDE-CODE-BEST-PRACTICES.md#38-repository-mapping--context-management) for project-size-based map formats.

### Commit style
- `<type>: <short description>` — type is feat/fix/chore/docs/refactor/test
- Body explains *why*, not *what*
- Append `Co-Authored-By: Claude Code <noreply@anthropic.com>`
