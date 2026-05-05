# Markdown Previewer

## Tech Stack
- Python 3.11.7 (pyenv virtualenv: `md_preview`)
- mistune 3.x for Markdown parsing
- argparse (stdlib) for CLI

## Conventions
- Single-file CLI entry point: `md_preview.py`
- Use argparse for CLI
- Keep HTML template inline (no separate template file for v1)
- Functions: one responsibility each, snake_case naming

## Scope (v1)
- CLI tool: `python md_preview.py input.md` → `input.html`
- Support: headings, paragraphs, bold/italic, links, images, code blocks, unordered lists
- No live server, no file watcher

## Key Constraint
- Single external dependency: mistune (pure Python, no C extensions)
