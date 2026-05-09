# Claude Code Engineering Best Practices Guide

## Table of Contents

- [1. Project Structure](#1-project-structure)
  - [1.1 CLAUDE.md — Project-Level Instruction File](#11-claudemd--project-level-instruction-file)
  - [1.2 .claude/ Directory](#12-claude-directory)
  - [1.3 Memory System](#13-memory-system)
- [2. Daily Workflow](#2-daily-workflow)
  - [2.1 Core Cycle: Plan → Implement → Review](#21-core-cycleplan--implement--review)
  - [2.2 Using Plan Mode](#22-using-plan-mode)
  - [2.3 Task Management](#23-task-management)
  - [2.4 Using Agents](#24-using-agents)
  - [2.5 Parallel Strategies](#25-parallel-strategies)
- [3. Habits and Techniques](#3-habits-and-techniques)
  - [3.1 Writing Prompts](#31-writing-prompts)
  - [3.2 Agents vs Direct Tool Calls](#32-agents-vs-direct-tool-calls)
  - [3.3 Permission Configuration](#33-permission-configuration)
  - [3.4 Hooks Mechanism](#34-hooks-mechanism)
  - [3.5 Git Workflow](#35-git-workflow)
  - [3.6 Common Anti-Patterns](#36-common-anti-patterns)
  - [3.7 Test-Driven AI Agent (TDD for Agents)](#37-test-driven-ai-agent-tdd-for-agents)
  - [3.8 Repository Mapping & Context Management](#38-repository-mapping--context-management)
- [4. Quick Reference](#4-quick-reference)

---

## 1. Project Structure

### 1.1 CLAUDE.md — Project-Level Instruction File

`CLAUDE.md` is an instruction file placed at the project root. **Claude Code loads it automatically on every session start.** It tells Claude about the project's background, conventions, dependencies, and things to watch out for.

**A typical CLAUDE.md structure:**

```markdown
# Project Name
> A web app with React frontend and Go backend

## Tech Stack
- Frontend: React 18 + TypeScript + Tailwind
- Backend: Go 1.22 + PostgreSQL
- Build: Vite (frontend), Makefile (backend)

## Conventions
- Use functional components with hooks, no class components
- API routes follow RESTful pattern: /api/v1/{resource}
- Tests use Vitest (frontend) and stdlib testing (backend)
- Commit messages in conventional commits format

## Key Paths
- src/components/ — shared UI components
- src/pages/ — route-level page components
- internal/handlers/ — HTTP handlers
- internal/service/ — business logic

## Scope
- User-facing web app with auth, dashboard, and data export
- No mobile app, no offline support

## Active Decisions
- Considering whether to migrate from REST to GraphQL for the dashboard

## Constraints
- Never modify generated/ directory — it's auto-generated from OpenAPI spec
- Auth middleware expects a JWT in the Authorization header
- Environment variables are documented in .env.example
```

**Writing tips:**
- Be concise — Claude reads this every time, verbosity wastes context
- Write "why" and "constraints," not things derivable from the code
- Keep it current — when conventions change, CLAUDE.md changes too
- Use `/init` to have Claude auto-generate a first draft

**Scope + Active Decisions: the lightweight feature state**

`## Scope` and `## Active Decisions` together form the project's "working memory" — the one artifact Claude reads every session to understand what we're building, what changed, and what's being reconsidered. They are the place for lightweight, high-churn feature state:

- **Scope** — current project boundary. What's in, what's explicitly out. Updated when scope changes.
- **Active Decisions** — transient debates and reconsiderations. "Considering replacing REST with GraphQL" or "Auth rewrite on hold until Q3." Keep to 2-3 lines.

When something gets removed from Scope or Active Decisions, ask: *"Would another developer need to know why we dropped this?"* If yes → write an ADR in `docs/decisions/`. If only Claude needs it → save to project Memory. Both channels are covered below in Section 1.3.

### 1.2 .claude/ Directory

`.claude/` is the project-level configuration directory for Claude Code, placed at the project root:

```
.claude/
├── settings.json       # Project-level config (permissions, hooks, env vars, etc.)
├── settings.local.json # Local override config (not committed to git)
└── memory/             # Memory system persistence directory
    ├── MEMORY.md       # Memory index file
    ├── user_role.md    # User-related memories
    ├── feedback_xxx.md # Feedback-related memories
    └── ...
```

**Core settings.json configuration options:**

```json
{
  "permissions": {
    "allow": [
      "Bash(npm:*)",
      "Bash(git:*)",
      "Bash(go:*)"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(sudo:*)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "prettier --write $CLAUDE_TOOL_INPUT_FILE_PATH"
        }]
      }
    ]
  },
  "env": {
    "NODE_ENV": "development"
  }
}
```

**settings.local.json** is for private local config (e.g., personal API keys) and should be added to `.gitignore`.

### 1.3 Memory System

Memory is a persistent, cross-session memory system. Claude retrieves relevant memories automatically. There are four types:

| Type | Purpose | Example |
|------|------|------|
| **user** | User's role, preferences, knowledge background | "I'm a Go backend engineer with limited React experience" |
| **feedback** | User corrections and confirmations | "Don't mock the database — last time mocked tests passed but the production migration failed" |
| **project** | Project facts, decisions, timelines | "Auth middleware rewrite is driven by compliance requirements, not tech-debt cleanup" |
| **reference** | Pointers to external resources | "Pipeline bugs are tracked in the Linear INGEST project" |

**Memory writing principles:**
- Don't write things derivable from code/git (file paths, code patterns, architecture)
- Don't write ephemeral task state (use Tasks for that)
- Write "why" and "context" — help future Claude judge if the memory is still valid
- Feedback memories must include **Why** and **How to apply**

**Memory file format:**

```markdown
---
name: prefer-real-db-in-tests
description: Integration tests must use a real database, no mocking
type: feedback
---

Integration tests must connect to a real database, no mocking.
**Why:** Last time mocked tests passed but the production migration failed — mock/prod divergence went undetected.
**How to apply:** Any test involving database operations must use a real test database.
```

### 1.4 Which Channel for What — Decision Framework

Project knowledge lives in three channels with different reach, weight, and audience:

| Channel | Loaded when | Audience | Best for |
|---------|-------------|----------|----------|
| **CLAUDE.md** (Scope + Active Decisions) | Every session, always | Claude + team | Lightweight feature state: what we're building, what changed, what's being reconsidered |
| **docs/decisions/** (ADRs) | When the topic area surfaces | Team + future you | Settled architecture decisions with full rationale — "why SQLite over Postgres" |
| **Memory** (project type) | On-demand, by relevance | Claude only | Deep history: "we abandoned live preview because hot-reload broke under concurrent edits" |
| **Git log** | Only when queried | Everyone | Forensic: what actually shipped, in what order |
| **Code itself** | When read/explored | Everyone | Ground truth of what exists right now |

**Litmus test:** *"Would another developer joining tomorrow need this to avoid wasting time?"* If yes → `docs/decisions/`. If no, but Claude would serve you better by knowing it → Memory.

**Anti-patterns:**
- Don't put team-relevant design rationale in Memory — it's invisible to teammates
- Don't put personal preferences in `docs/decisions/` — those aren't architecture decisions
- Don't let CLAUDE.md Scope/Active Decisions grow stale — they're the most important 10 lines you update

---

## 2. Daily Workflow

### 2.1 Core Cycle: Plan → Implement → Review

The recommended workflow for using Claude Code is a three-layer cycle:

```
Plan → Implement → Review → Loop
```

**Plan phase:**
- For **any non-trivial change**, use Plan Mode to let Claude explore the code and design an approach
- You review the approach and make a decision before it writes any code
- This avoids the waste of "wrote a bunch of code then realized the direction was wrong"

**Implement phase:**
- Claude implements step by step, you confirm results after each step
- Complex tasks are broken into multiple Tasks to track progress
- Run tests / verify after each logical unit is completed

**Review phase:**
- Use `/review` or directly ask Claude to review the changes
- Check: logical correctness, security vulnerabilities, edge cases, over-engineering
- Commit after review passes

### 2.2 Using Plan Mode

**When you must enter Plan Mode:**
- New feature implementation
- Multi-file changes (>2-3 files)
- Multiple valid implementation approaches
- Architectural-level decisions
- Requirements are unclear and need exploration first

**When you don't need it:**
- Single-line / few-line bug fix or typo
- Already have very clear, detailed instructions
- Pure exploration / research questions

**How Plan Mode works:**
1. Claude first searches code via Explore Agent, understands the existing implementation
2. Designs the approach using Plan Agent
3. Writes a plan file to `.claude/plans/`
4. You review the plan and suggest changes
5. Once confirmed, Claude exits Plan Mode and begins implementing

### 2.3 Task Management

For complex tasks with more than 3 steps, use the Task system to track progress:

```
TaskCreate → TaskUpdate(in_progress) → Do → TaskUpdate(completed) → Next
```

**Best practices:**
- Task subjects use imperative mood, short and actionable (e.g., "Add JWT verification middleware")
- Mark tasks **immediately** as completed, don't batch
- Use `addBlocks` / `addBlockedBy` to express task dependencies
- Create new tasks promptly when you discover them

**Example:**

```
Task 1: Add JWT middleware (pending)
Task 2: Protect /api/private routes (pending, blockedBy: 1)
Task 3: Add tests for auth flow (pending, blockedBy: 1)
```

### 2.4 Using Agents

Claude Code has several specialized sub-agents, each with its own use case:

| Agent | Purpose | When to Use |
|-------|------|---------|
| **Explore** | Fast read-only search | Search code, find files, grep symbols, locate definitions. **Search only, no code changes.** |
| **Plan** | Software architecture design | Design implementation approaches, evaluate architecture decisions, output step-by-step plans. |
| **general-purpose** | General multi-step tasks | Complex tasks requiring search + analysis + possibly code changes. |
| **claude-code-guide** | Questions about Claude Code itself | "What can Claude do?", "How do I configure X?", "How does this feature work?" |

**Agent usage principles:**
- If you know the file path, use Read/Edit directly — don't go through an Agent
- If you only know the symbol name / keyword, use Explore Agent to search
- If it's an open-ended exploration ("How does auth work in this project?"), use Explore Agent (medium/very thorough)
- If an Agent is already running and its task isn't done, use **SendMessage** to continue the same Agent, **don't spawn a new one** (new Agents don't have prior context)
- Explicitly tell the Agent whether you want **research only** or **write code** — it doesn't know your intent

#### 2.4.1 Custom Subagent Patterns (Iron Triangle)

Beyond the built-in agents, you can design your own subagent roles for software development. The recommended pattern is the **Iron Triangle** — three roles that map to the Plan → Implement → Review cycle:

| Role | Maps To | Trigger | Key Deliverable |
|------|---------|---------|-----------------|
| **Architect** | Plan Mode | New feature, unclear scope | SPEC.md + TODO.md (with acceptance criteria) |
| **Developer** | Implement | TODO.md has unchecked items | Code changes + DONE.md (change log) |
| **Reviewer** | Review | Tasks marked done in TODO.md | Review conclusion appended to DONE.md |

Plus one on-demand role: **Bootstrap** — summoned only at project init or when adding new infrastructure. Sets up the dev environment and verifies all commands work, then disappears.

**Key rules for custom subagents:**
- **Files as shared memory** — agents communicate through SPEC.md, TODO.md, and DONE.md, not through conversation context
- **Human holds the baton** — you decide when to move from Architect to Developer to Reviewer; no fully autonomous loops
- **Document and commit as you go** — every agent session ends with written output and a git commit; agent work without a paper trail is lost work
- **One task per commit** — keeps changes small, reviewable, and traceable

See the full guide: [CLAUDE-CODE-SUBAGENTS.md](CLAUDE-CODE-SUBAGENTS.md) — includes copy-paste System Prompt templates for each role, a worked Pomodoro Timer example, and common pitfalls.

### 2.5 Parallel Strategies

**When to parallelize:**
- Multiple **mutually independent** search/exploration tasks (launch multiple Explore Agents simultaneously)
- Multiple **mutually independent** bash commands (e.g., run `git status` and `git diff` in parallel)
- File writes + other independent operations

**When NOT to parallelize:**
- Subsequent operations depend on the results of prior operations
- After an Edit, you need to see the effect before the next Edit

**Practical experience:**
```
# Good parallelism — three independent searches
Explore("Find where auth middleware is defined")
Explore("Find all API route definitions")
Explore("Find auth mock patterns in test files")

# Bad parallelism — the second depends on the first's result
Explore("Find auth middleware") + Explore("Read auth middleware and explain it")  ← second needs first's result
```

---

## 3. Habits and Techniques

### 3.1 Writing Prompts

**When writing prompts for Agents, use this formula:**

> **Goal + Background + Known Constraints + Output Format**

Example (good prompt):

```
We're refactoring the auth middleware to move session token storage from cookies to the Authorization header.
The project uses Go + chi router.
The existing middleware is at internal/middleware/auth.go.
I need a plan: which files to modify, what changes in each file, migration steps, how to ensure backward compatibility.
Output a step-by-step plan with a risk level annotation for each step.
```

Example (bad prompt):

```
Look at auth and tell me how to change it
```

**Key points:**
- Tell the Agent **why you're doing this** (business/technical context) — it helps make better judgments
- Be clear about **known constraints** (what must not be changed, what must remain compatible)
- Specify the **output format** ("report under 200 words," "step-by-step plan," "conclusions only, no process")
- Don't write "based on your findings, fix it" in a prompt — that's pushing the understanding task onto the Agent. You should digest the Agent's research results yourself, then write instructions

### 3.2 Agents vs Direct Tool Calls

**A simple decision tree:**

```
Do you know the file path?
├── Yes → Use Read / Edit directly
└── No → Do you know what symbol/keyword to search for?
    ├── Yes and scope is clear → Use Bash: grep/find directly
    └── No or scope is unclear → Use Explore Agent
```

**Specific scenarios:**

| Scenario | Tool |
|------|------|
| Read a file at a known path | `Read` |
| Search for occurrences of a function name | `Bash: grep -r "funcName" .` |
| Find the full implementation chain of a feature | Explore Agent (medium) |
| Search across multiple naming conventions and related concepts | Explore Agent (very thorough) |
| Complex multi-step research task | general-purpose Agent |

### 3.3 Permission Configuration

Claude Code's permission system lets you precisely control which operations require confirmation and which are auto-approved.

**Recommended layered strategy:**

```json
// .claude/settings.json — project-level, committed to git
{
  "permissions": {
    "allow": [
      "Bash(git:status)",
      "Bash(git:diff)",
      "Bash(git:log)",
      "Bash(npm:run*)",
      "Bash(go:test*)"
    ],
    "deny": [
      "Bash(rm:-rf*)",
      "Bash(sudo:*)",
      "Bash(curl:* | sh)",
      "Bash(git:push:--force*)"
    ]
  }
}
```

```json
// .claude/settings.local.json — local override, not committed
{
  "permissions": {
    "allow": [
      "Bash(npm:install*)",
      "Bash(docker:*)"
    ]
  }
}
```

**Principles:**
- Only allow operations you are confident are safe
- `settings.local.json` should not be committed to git (add to `.gitignore`)
- Use `/config` command or `update-config` skill to modify config — safer than manual editing
- `deny` takes priority over `allow`

### 3.4 Hooks Mechanism

Hooks let Claude Code automatically execute commands when certain events occur. Ideal for: **"Every time X happens, do Y"** automation needs.

**Common Hooks:**

| Hook | Trigger | Typical Use |
|------|---------|---------|
| `PostToolUse` | After tool call | Auto-format, lint |
| `PreToolUse` | Before tool call | Block dangerous operations |
| `Notification` | Notification events | Desktop notifications |
| `Stop` | Claude response ends | Auto-run tests |
| `UserPromptSubmit` | User sends a message | Inject additional context |

**Example — auto-format after every Edit:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "prettier --write ${CLAUDE_TOOL_INPUT_FILE_PATH}"
        }]
      }
    ]
  }
}
```

**Important notes:**
- Hook command failures do **not** roll back the operation — don't rely on hooks for critical validation
- Hooks run via the Claude Code harness, not by Claude — so memory and preferences cannot replace hooks
- For complex hook logic, write a script file and invoke the script in the hook command

### 3.5 Git Workflow

**Claude Code's built-in Git Safety Protocol:**

Claude has the following built-in constraints:
- Won't auto `git push --force` to main/master
- Won't skip hooks (`--no-verify`, `--no-gpg-sign`)
- Won't perform destructive operations (`reset --hard`, `checkout .`, `clean -f`) unless you explicitly request them
- Won't commit proactively — only commits when you explicitly ask

**Recommended daily rhythm:**

1. **Before starting work:** Confirm the branch is clean, understand the current state
2. **During implementation:** Verify after each logical unit (run tests, check UI)
3. **After completing:** Have Claude do self-review, confirm no leftover debug code or sensitive info
4. **When committing:** Explicitly tell Claude "commit these changes," provide commit message direction

**Commit message convention:**

```
<type>: <short description>

<optional body — why the change, not what changed>

Co-Authored-By: Claude Code <noreply@anthropic.com>
```

Claude automatically appends the `Co-Authored-By` line, marking this as an AI-assisted commit.

### 3.6 Common Anti-Patterns

Here are common pitfalls when using Claude Code:

**1. Entering Plan Mode for trivial changes**
- Fixing a one-line typo or adding a log statement doesn't need a plan
- Principle: the simpler the change, the lighter the process

**2. Mega-prompts**
- Dumping massive context = drowning key information
- Refine: goal, constraints, output format — that's enough

**3. Asking an Agent to "understand + execute" in one step**
- "Based on your findings, fix the bug" — this pushes the understanding task onto the Agent
- Correct approach: let the Agent research → you digest the results → then give precise instructions

**4. "Try again" inside an Agent**
- Agents don't see prior conversations. If you need to continue the same Agent's task, use SendMessage — don't re-spawn

**5. Starting large changes without Plan Mode**
- Multi-file refactor without a design first → halfway through realize the architecture is wrong → start over
- 5 minutes of planning saves 30 minutes of rework

**6. Using Memory as a TODO list**
- Memory is long-term, cross-session storage — don't store current task state in it
- Use the Task system for transient tracking

**7. Declaring done without verification**
- Claude won't automatically open a browser to verify UI — if you had it change frontend code, explicitly ask it to start the dev server and test in a browser

**8. Over-abstraction / premature optimization**
- "Add a factory pattern for the email sender" — but you only have one email sender
- Three similar lines > premature abstraction

**9. Using hooks for critical business validation**
- Hook failure won't prevent the operation from executing
- Put critical validation in CI, not in Claude Code hooks

**10. Allowing all permissions**
- Broad `"allow": ["Bash(*)"]` = running naked
- Use a denylist to guard the bottom line (`rm -rf`, `sudo`, `curl | sh`)

**11. End-of-task verification**
- Writing all the code, then running the full test suite — when it fails, the error surface is the entire change and diagnosis is expensive
- Instead: verify each independently testable logical unit before moving to the next. The feedback radius (how much code you have to search for the bug) must be smaller than your diagnostic range (how much code you can reason about in 10 seconds)

**12. Reading without a map**
- Diving into source files without first understanding the project structure — this fills context with irrelevant files and dilutes attention
- Instead: read the project map first (CLAUDE.md `## Key Paths`, `## Scope`, or a dedicated file tree), then output an explicit list of which files you need to read, and read only those

---

### 3.7 Test-Driven AI Agent (TDD for Agents)

The core problem: AI agents naturally defer verification to the end of implementation. They write all the code, then run the tests — and when it fails, the error surface is the entire change. This is the single biggest efficiency killer in AI-assisted development.

The solution: **micro-verification loops** — verify after each independently testable logical unit, not after the whole task.

**What is a logical unit?**

A piece of code with clear input/output boundaries that can be verified independently. The litmus test: *"If this unit's verification fails, can I pinpoint the cause in 10 seconds?"*

| Language/Stack | A logical unit ≈ | Lightest verification |
|---------------|-------------------|----------------------|
| Python | A function | `python -c "import module; module.func(test_input)"` |
| TypeScript | A component or a function | `npx tsc --noEmit`, or run the single test |
| Go | A function or a handler | `go build ./...` or `go test -run TestXxx` |
| SQL | A CTE or a subquery | Compile the model, or run with a LIMIT |
| Rust | A function or a module | `cargo check` or `cargo test test_name` |

**Circuit breaker rule:**

If the same logical unit fails verification 3 times in a row, **stop and report**. Three consecutive failures on the same code means the approach is wrong — not the implementation. Do not guess a 4th fix. Report to the human: what was attempted, what errors occurred, what you recommend.

**Verification progression:**

```
Unit verify (compile/lint) → Unit verify (run) → Full test suite → End-to-end
```

Each stage gates the next. Never skip a stage. Never run the full test suite before individual units pass.

**Integration with the Iron Triangle:**
- **Developer:** micro-verifies after each logical unit, records verification commands in DONE.md
- **Reviewer:** independently re-runs the test suite, checks DONE.md for verification evidence. No evidence → NEEDS FIX
- **Architect:** specifies acceptance criteria granular enough for unit-level verification

### 3.8 Repository Mapping & Context Management

The core problem: AI agents have limited context windows and suffer from **attention dilution** — the more irrelevant code they read, the worse their reasoning becomes. Giving an agent a task and letting it explore freely often results in it reading 15 files when only 3 matter.

The solution: **two-step fetch** — read the map first, then target specific files.

**Step 1: Orient**

Read the project map to understand structure. What counts as a map depends on project size:

| Project size | Map |
|-------------|-----|
| Small (single-digit files) | CLAUDE.md `## Key Paths` + `## Scope` is sufficient |
| Medium (10-50 files) | CLAUDE.md + `tree` output (directory-only, max 2 levels deep) |
| Large (50+ files) | Dedicated `ARCHITECTURE.md` — module overview, one-line description per directory |

The map should contain: file paths, module names, one-line descriptions. Not full source code.

**Step 2: Target**

Before reading any source file, output an explicit list:
> "To complete this task, I need to read these N files: [file paths]. These are the only files I will touch."

This forces the agent to make a deliberate scoping decision. It also lets the human catch scope errors early ("No, you also need to read the auth middleware" or "Don't touch the billing module").

**Maintaining the map:**

- For small/medium projects: `## Key Paths` in CLAUDE.md is the map. Keep it current.
- For large projects: generate `ARCHITECTURE.md` once, update it when modules are added or reorganized. A stale map is worse than no map.

**Anti-pattern to avoid:**
- Don't use `grep -r` as a substitute for reading the map. Grep finds occurrences but doesn't tell you which files matter.

---

## 4. Quick Reference

### Common Commands

| Command | Purpose |
|------|------|
| `/init` | Generate CLAUDE.md for the current project |
| `/config` | Modify Claude Code configuration (theme, model, etc.) |
| `/review` | Review current changes |
| `/security-review` | Security review of changes on the current branch |
| `/simplify` | Review code for reusability and quality |
| `/clear` | Clear current session context |
| `/compact` | Compress conversation context (preserves key info) |
| `/loop` | Run a task on a recurring interval |
| `! command` | Execute a command directly in the terminal |

### Tool Decision Tree

```
Need to search code?
├── Know the file path → Read
├── Know the symbol name → Bash: grep -r
├── Open-ended search → Explore Agent
└── Complex multi-step research → general-purpose Agent

Need to implement a feature?
├── Trivial (one or two lines) → Edit directly
├── Non-trivial → Plan Mode → Review → Implement
└── Uncertainties → Explore first → Then Plan

Need to track progress?
├── Single step → Just do it
└── Multi-step (≥3) → TaskCreate to break down
```

### One-Sentence Summary

> **Plan before you code. Explore before you plan. Review before you commit.**

---

*This document itself is a living reference — keep updating it as your experience with Claude Code deepens.*
