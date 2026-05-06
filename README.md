# Claude Code Playbook

A practical guide to working with Claude Code — learned by doing, documented for reference.

## What's inside

| File | Purpose |
|------|---------|
| `CLAUDE.md` | This project's own instruction file — dogfoods the template |
| `CLAUDE-TEMPLATE.md` | **Seed file** — copy into new projects, then ask Claude to interview you and fill it in |
| `CLAUDE-CODE-ACTIONS.md` | **Action guide** — what to do and when, organized by project phase |
| `CLAUDE-CODE-BEST-PRACTICES.md` | **Concept manual** — deep dive into CLAUDE.md, Plan Mode, Tasks, Memory, Hooks, Agents, Git workflow |
| `docs/decisions/` | ADR directory for settled architecture decisions (template inside) |
| `md_preview.py` | Example project built while learning the workflow (Markdown → HTML previewer) |

## How to use

**Starting a new project:**
```bash
cp CLAUDE-TEMPLATE.md ~/my-new-project/CLAUDE.md
```
Then tell Claude: "Read this CLAUDE.md template, interview me, and customize it for this project."

**Stuck or forgot the workflow:**
Open `CLAUDE-CODE-ACTIONS.md` — it's organized by "when" so you can jump to the section you need.

**Want to understand a concept deeply:**
`CLAUDE-CODE-BEST-PRACTICES.md` covers the why and how behind each feature.

**Not sure where to put something?**
Use the litmus test: *"Would another developer need this to avoid wasting time?"* → `docs/decisions/`. Only Claude needs it? → Memory. Full table in `CLAUDE-CODE-ACTIONS.md` Section 2.2.

## One-sentence summary

> **Plan before you code. Explore before you plan. Review before you commit.**
