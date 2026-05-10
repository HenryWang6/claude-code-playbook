# Markdown Previewer
> A CLI tool that converts Markdown files to static HTML

## Tech Stack
- Python 3.11.7 (pyenv virtualenv: `md_preview`)
- mistune 3.x for Markdown parsing
- argparse (stdlib) for CLI

## Conventions
- Single-file CLI entry point: `md_preview.py`
- Use argparse for CLI
- Keep HTML template inline (no separate template file for v1)
- Functions: one responsibility each, snake_case naming

## Key Paths
- `md_preview.py` — CLI entry point, all logic

## Scope
- CLI tool: `python md_preview.py input.md` → `input.html`
- Support: headings, paragraphs, bold/italic, links, images, code blocks, unordered lists
- No live server, no file watcher
- This repo also contains playbook documentation (CLAUDE-CODE-*.md, CLAUDE-TEMPLATE.md) and docs/decisions/ for settled architecture decisions

## Active Decisions
- No active debates — scope is stable for v1

## Constraints
- Single external dependency: mistune (pure Python, no C extensions)

---

## Claude Code Workflow (shared across all projects)

### Decision triggers

| When | Then |
|------|------|
| New feature, >2 files, or architectural choice | **Plan Mode** — design first, code after approval |
| 3+ distinct steps | **TaskCreate** — track each step, use dependencies |
| Starting a new task | **Read project map first** (CLAUDE.md Key Paths, ARCHITECTURE.md, or file tree), then target only the files you need |
| Need to search/explore codebase | **Explore Agent** (don't guess file paths) |
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
