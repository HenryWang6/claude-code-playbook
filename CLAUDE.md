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
