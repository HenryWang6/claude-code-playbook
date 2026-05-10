# Claude Code Action Guide

A checklist organized by timing. Just remember "what to do when" — Claude will help you execute the details.

---

## 1. Project Day One (One-Time Setup)

### 1.0 Set Up Iron Triangle Agents (One-Time, First Project Only)

The decision tree in Section 2.1 references three subagents: Architect, Developer, Reviewer. These must exist before you can dispatch them. Create them once at user scope — they'll be available across all your projects.

| Agent | File to create |
|-------|---------------|
| Architect | `~/.claude/agents/architect.md` |
| Developer | `~/.claude/agents/developer.md` |
| Reviewer | `~/.claude/agents/reviewer.md` |

**What to say:**

> "Create the three Iron Triangle subagents at my user scope (~/.claude/agents/). Use the System Prompt templates from CLAUDE-CODE-SUBAGENTS.md Section 2 for Architect, Developer, and Reviewer. Add appropriate YAML frontmatter to each."

Claude will create three agent files with YAML frontmatter (`name`, `description`, `model: inherit`, `memory: user`) and the System Prompt body from SUBAGENTS.md Sections 2.1–2.3.

After creation, verify with: **"list my user-scope agents"**

> **Note:** This is a one-time setup. You don't repeat this for each new project — user-scope agents are available everywhere.

### 1.1 Copy the CLAUDE Template

```
cp CLAUDE-TEMPLATE.md ./new-project/CLAUDE.md
```

### 1.2 Interview-Style CLAUDE.md Customization

Tell Claude:

> "read this CLAUDE.md template, then interview me to fill in the Tech Stack, Conventions, Key Paths, and Constraints sections. Ask me one section at a time."

After you answer, Claude will fill in the top half. The Workflow rules in the bottom half stay as-is.

### 1.3 Set Up Infrastructure

Complete in order:

| Action | What to Say |
|------|--------|
| Initialize git | "git init, create .gitignore" |
| Configure hooks | "Configure a Stop hook to play a sound, and a PermissionRequest hook to play a different sound" |
| Set permissions | "Add commonly used safe commands to the allow list, deny rm -rf / sudo" |
| First commit | "commit these changes" |

---

## 2. Daily Development Cycle

Choose the right path based on what you need to do:

### 2.1 Decision Tree

```
What you're planning to do...

├── Fix a typo / one-liner / add a log?
│   └── Just say it → Claude fixes it directly
│
├── New feature / refactor / changes to >2 files?
│   └── "Let's Plan first" → Plan Mode → Review design → Implement
│
├── New feature, unclear architecture?
│   └── Architect subagent → produces SPEC.md + TODO.md → you review → then Developer
│
├── Spec is clear, ready to code?
│   └── Developer subagent → produces code + DONE.md → you review → then Reviewer
│
├── Code written, want independent quality check?
│   └── Reviewer subagent → appends review to DONE.md → fix or proceed
│
├── Complex task with 3+ steps?
│   └── "Break into Tasks, set up dependencies" → Complete one by one
│
├── Need to search code but don't know which file?
│   └── "Help me find where X is" → Explore Agent
│
└── Done with changes?
    └── "Review the changes" → Check → "commit"
```

> **Subagent workflow**: See [CLAUDE-CODE-SUBAGENTS.md](CLAUDE-CODE-SUBAGENTS.md) for the full Iron Triangle pattern — Architect → Developer → Reviewer, with copy-paste System Prompt templates.

### 2.2 When to Save to Memory

**Principle: For important project decisions, explicitly stating is more reliable than relying on auto-detection.**

Claude automatically saves feedback memory when you correct it. But project memory (architecture decisions, abandoned approaches, why you chose A over B) won't trigger automatically — you need to explicitly tell it.

| Scenario | What to Say |
|------|--------|
| Claude made a directional mistake, you corrected it | "Remember this" |
| You discovered an important project constraint | "Save this to project memory" |
| You have a preference that should apply going forward | "Save as user memory" |
| You abandoned an approach / feature direction | "Remember why we abandoned X, save as project memory" |
| You updated CLAUDE.md Scope / Active Decisions, removed something | Also save the *reason* for removal as project memory |

**Natural trigger:** Every time you update CLAUDE.md `## Scope` or `## Active Decisions` and something is removed — ask yourself "Will I remember why I dropped this six months from now?" If unsure, apply the litmus test: would another developer need it? → `docs/decisions/`. Only Claude needs it? → Memory.

**Where to put information — Quick reference:**

| Where | Best For | When Loaded |
|------|---------|---------|
| CLAUDE.md | Current tech stack, conventions, Scope, Active Decisions, Constraints | Every session |
| docs/decisions/ | Settled architecture decisions with full rationale, team-visible design docs | When the topic area surfaces |
| Memory (project) | Reasons for abandoned approaches, historical decisions, architecture rationale | On-demand retrieval |
| Memory (feedback) | User corrections and preferences | On-demand retrieval |
| Task | Work progress for the current session | Current session only |

**Litmus test:** *"Would another developer joining tomorrow need this to avoid wasting time?"* If yes → `docs/decisions/`. If only Claude needs it to assist you better → Memory.

Don't save: current task progress details (use Tasks), things you can read from the code (just read the code).

### 2.3 When to Update CLAUDE.md

| Trigger Event | What to Say |
|----------|--------|
| Team agreed on a new coding convention | "Update CLAUDE.md, add a convention" |
| Discovered a module that must not be changed | "Update CLAUDE.md Constraints" |
| Changed the tech stack | "Update CLAUDE.md Tech Stack" |

**Principle**: Every time Claude makes a mistake because it "didn't know a convention," add that convention to CLAUDE.md.

---

## 3. Verification and Course Correction

### 3.1 Expect Micro-Verification — Don't Let Claude Skip It

Claude should auto-verify after each logical unit (see [Micro-Verification Loops](../CLAUDE.md#micro-verification-loops)). You should not need to ask. If Claude finishes a task without showing verification output, it skipped a step — call it out:

| Scenario | If Claude skipped verification, say |
|------|--------|
| UI changes | "I didn't see you test this in the browser. Start the dev server and verify." |
| Backend logic changes | "You didn't run the tests for this change. Run them now." |
| CLI tool changes | "Run it with a few different inputs and show me the output." |
| Config changes | "Verify the config loads correctly before claiming done." |
| Any change | "Show me the verification output — compile, run, test — for each unit you changed." |

### 3.2 When Claude Goes Off Track

Don't tolerate it and correct round after round. Interrupt immediately when you spot a direction problem:

| Problem | What to Say |
|------|--------|
| Over-engineering | "Too complex, keep it simple. Three similar lines > premature abstraction" |
| Missing edge cases | "Also consider scenario X" |
| Completely wrong direction | "No, should use approach Y, because Z. Start over." |
| Hallucination / made-up API | "That API doesn't exist, check the docs first" |

### 3.3 Permission Strategy: Gradual

Start with default permissions (more confirmation prompts). After using it for a week:

> "Use the fewer-permission-prompts skill to analyze and add high-frequency safe commands to the allow list"

Don't start with `allow: ["Bash(*)"]`.

---

## 4. Session Management

| Signal | Action |
|------|------|
| Claude's responses are noticeably slow | `/compact` — compress context |
| Topic completely changed | `/clear` — clear session, start fresh |
| Context has grown large, current task is done | `/compact` — clean up irrelevant history |
| Claude starts showing "memory confusion" | `/clear` then re-describe the current task |

**Rule**: `/clear` = brand new start; `/compact` = keep key info, discard process details.

---

## 5. Finishing Up and Committing

```
All logical units implemented
  → Verify micro-checks ran: did Claude compile/run/test after each unit?
    (If no evidence → "show me the verification output for each unit")
  → "review these changes" (check edge cases, security, over-engineering)
  → "run the full test suite" (final confirmation — units already passed individually)
  → "commit these changes" (provide commit message direction)
  → push to remote (if applicable)
```

> **Note:** Tests should have run throughout implementation, not just at the end. The final `run tests` is a safety net, not the primary verification. If you're running tests for the first time at this stage, the micro-verification loop was skipped.

### Subagent Commit Discipline

When using subagents (Architect / Developer / Reviewer), every agent session must end with a commit. This is non-negotiable — agent work without a paper trail is lost work.

| Agent | Commit Message Pattern |
|-------|----------------------|
| Architect | `docs: add spec and task list` |
| Developer | `feat: <task description>` (one commit per task) |
| Reviewer | `review: <what was reviewed>` (if fixes applied) |
| Bootstrap | `chore: bootstrap development environment` |

If a subagent finishes without committing, remind it: "Commit your changes before moving on."

### Commit Format

```
<type>: <short description>
         ^— feat / fix / chore / docs / refactor / test

Body explains "why the change," not "what changed"

Co-Authored-By: Claude Code <noreply@anthropic.com>
```

Claude will automatically append the `Co-Authored-By` line.

---

## 6. Learning Log

### Concepts Practiced (2026-05-09, playbook refinement)

| Concept | How Learned | Proficiency |
|------|---------|---------|
| CLAUDE.md | Hand-wrote project instructions, made templates | ✅ Proficient |
| Plan Mode | Designed a markdown previewer | ✅ Proficient |
| Task System | 4 Tasks + dependencies | ✅ Proficient |
| Memory | Saved user_role, understood isolation | ✅ Proficient |
| Hooks (Stop + PermissionRequest) | Configured dual notification sounds | ✅ Proficient |
| Git Workflow | init / ignore / commit | ✅ Proficient |
| Agents (Explore/Plan/general-purpose) | Theory + Iron Triangle subagent design | ✅ Proficient |
| Permission Configuration | Basic allow/deny | 🟡 Used but not systematically tuned |
| /compact / /clear | Theory learned | 🟡 Haven't practiced yet |
| Subagent Iron Triangle | Designed Architect/Developer/Reviewer pattern with SPEC/TODO/DONE files | ✅ Proficient |
| Micro-Verification Loops | Integrated into CLAUDE.md and subagent prompts as a core workflow rule | 🟡 Theory designed, needs battle-testing in real projects |
| Repository Mapping | Added two-step fetch rule to prevent context dilution | 🟡 Theory designed, needs battle-testing in real projects |

### To-Learn List

Plan to practice in a **more complex project**:

- **Micro-Verification Loops in practice** — observe whether agents self-correct effectively when feedback radius is small
- **Repository Mapping in practice** — tune the map format (CLAUDE.md Key Paths vs ARCHITECTURE.md) for different project sizes
- **Circuit breaker behavior** — does the 3-failure rule prevent death spirals or fire too aggressively?
- **Advanced Hooks** — PostToolUse auto-format, PreToolUse to block dangerous operations
- **Multi-Agent parallelism** — search multiple areas simultaneously, parallel independent verifications
- **PR workflow** — branching, pushing, PR descriptions

### When to Revisit This List

- After 2-3 real projects using the micro-verification + repo-mapping patterns
- When a subagent gets stuck in a fix loop despite the circuit breaker rule
- When context dilution still occurs despite two-step fetch
