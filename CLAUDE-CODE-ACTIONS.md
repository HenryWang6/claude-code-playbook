# Claude Code Action Guide

A checklist organized by timing. Just remember "what to do when" — Claude will help you execute the details.

---

## 1. Project Day One (One-Time Setup)

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
├── Complex task with 3+ steps?
│   └── "Break into Tasks, set up dependencies" → Complete one by one
│
├── Need to search code but don't know which file?
│   └── "Help me find where X is" → Explore Agent
│
└── Done with changes?
    └── "Review the changes" → Check → "commit"
```

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

**Natural trigger:** Every time you update CLAUDE.md `## Scope` or `## Active Decisions` and something is removed — ask yourself "Will I remember why I dropped this six months from now?" If unsure, save to memory.

**Where to put information — Quick reference:**

| Where | Best For | When Loaded |
|------|---------|---------|
| CLAUDE.md | Current tech stack, conventions, Scope, Active Decisions, Constraints | Every session |
| Memory (project) | Reasons for abandoned approaches, historical decisions, architecture rationale | On-demand retrieval |
| Memory (feedback) | User corrections and preferences | On-demand retrieval |
| Task | Work progress for the current session | Current session only |

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

### 3.1 Make Claude Verify Its Own Work

Claude saying "done" doesn't mean it's actually done. You must actively ask:

| Scenario | What to Say |
|------|--------|
| UI changes | "Start the dev server and test in the browser" |
| Backend logic changes | "Run the relevant tests" |
| CLI tool changes | "Run it with a few different inputs and check the output" |
| Config changes | "Verify the config loads correctly" |

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
Changes are done
  → "review these changes" (check edge cases, security, over-engineering)
  → "run tests" (if the project has tests)
  → "commit these changes" (provide commit message direction)
  → push to remote (if applicable)
```

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

### Concepts Practiced (2026-05-05, cc_test project)

| Concept | How Learned | Proficiency |
|------|---------|---------|
| CLAUDE.md | Hand-wrote project instructions, made templates | ✅ Proficient |
| Plan Mode | Designed a markdown previewer | ✅ Proficient |
| Task System | 4 Tasks + dependencies | ✅ Proficient |
| Memory | Saved user_role, understood isolation | ✅ Understands |
| Hooks (Stop + PermissionRequest) | Configured dual notification sounds | ✅ Proficient |
| Git Workflow | init / ignore / commit | ✅ Proficient |
| Agents (Explore/Plan/general-purpose) | Theory learned | 🟡 Theory OK, no hands-on practice yet |
| Permission Configuration | Basic allow/deny | 🟡 Used but not systematically tuned |
| /compact / /clear | Theory learned | 🟡 Haven't practiced yet |

### To-Learn List

Plan to practice in a **more complex project**:

- **Explore Agent hands-on** — search and locate features in unfamiliar codebases
- **Multiple Plan-Implement-Review cycles** — iterative development
- **Interruption and recovery** — how to have Claude continue after a long task is interrupted
- **Advanced Hooks** — PostToolUse auto-format, PreToolUse to block dangerous operations
- **Multi-Agent parallelism** — search multiple areas simultaneously
- **PR workflow** — branching, pushing, PR descriptions

### When to Revisit This List

- Starting a new project and not sure where to begin
- Facing a complex feature and uncertain about the workflow
- Realizing a concept (like Agents) is only understood at a theoretical level, looking for hands-on opportunities
