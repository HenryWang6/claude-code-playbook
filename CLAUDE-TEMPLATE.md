# [Project Name]

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
| User corrects approach or gives feedback | **Save to Memory** immediately |
| User says "remember X" | **Save to Memory** immediately |

### Anti-patterns to avoid
- Don't Plan Mode for trivial fixes (typo, single-line change)
- Don't mock in tests unless the user explicitly approves it
- Don't over-engineer — three similar lines > premature abstraction
- Don't add error handling for scenarios that can't happen
- Don't create docs/README unless asked

### Commit style
- `<type>: <short description>` — type is feat/fix/chore/docs/refactor/test
- Body explains *why*, not *what*
- Append `Co-Authored-By: Claude Code <noreply@anthropic.com>`
