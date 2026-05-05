# Claude Code 工程实践指南

## 目录

- [1. 项目结构](#1-项目结构)
  - [1.1 CLAUDE.md — 项目级指令文件](#11-claudemd--项目级指令文件)
  - [1.2 .claude/ 目录](#12-claude-目录)
  - [1.3 Memory 系统](#13-memory-系统)
- [2. 日常工作流](#2-日常工作流)
  - [2.1 核心循环：Plan → Implement → Review](#21-核心循环plan--implement--review)
  - [2.2 Plan Mode 的使用](#22-plan-mode-的使用)
  - [2.3 Task 管理](#23-task-管理)
  - [2.4 Agent 的使用](#24-agent-的使用)
  - [2.5 并行策略](#25-并行策略)
- [3. 习惯与技巧](#3-习惯与技巧)
  - [3.1 Prompt 写法](#31-prompt-写法)
  - [3.2 Agent vs 直接工具调用](#32-agent-vs-直接工具调用)
  - [3.3 权限配置](#33-权限配置)
  - [3.4 Hooks 机制](#34-hooks-机制)
  - [3.5 Git 工作流](#35-git-工作流)
  - [3.6 常见反模式](#36-常见反模式)
- [4. 速查表](#4-速查表)

---

## 1. 项目结构

### 1.1 CLAUDE.md — 项目级指令文件

`CLAUDE.md` 是放在项目根目录的指令文件，**Claude Code 每次启动都会自动加载它**。它告诉 Claude 这个项目的背景、约定、依赖和注意事项。

**一个典型的 CLAUDE.md 结构：**

```markdown
# Project Name

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

## Important Notes
- Never modify generated/ directory — it's auto-generated from OpenAPI spec
- Environment variables are documented in .env.example
- The auth middleware expects a JWT in the Authorization header
```

**写法要点：**
- 简短精炼，Claude 每次都会读，太长浪费 context
- 写"为什么"和"约束"，不要写能从代码里读出来的东西
- 更新要及时 — 约定变了 CLAUDE.md 也要跟着变
- 可以用 `/init` 命令让 Claude 自动生成初稿

### 1.2 .claude/ 目录

`.claude/` 是 Claude Code 的项目级配置目录，放在项目根目录下：

```
.claude/
├── settings.json       # 项目级配置（权限、hooks、环境变量等）
├── settings.local.json # 本地覆盖配置（不提交到 git）
└── memory/             # Memory 系统的持久化目录
    ├── MEMORY.md       # Memory 索引文件
    ├── user_role.md    # 用户相关记忆
    ├── feedback_xxx.md # 反馈相关记忆
    └── ...
```

**settings.json 的核心配置项：**

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

**settings.local.json** 用于本地私密配置（如个人 API key），应加入 `.gitignore`。

### 1.3 Memory 系统

Memory 是跨会话持久化的记忆系统，Claude 会根据相关性自动检索。有四种类型：

| 类型 | 用途 | 示例 |
|------|------|------|
| **user** | 用户的角色、偏好、知识背景 | "我是 Go 后端工程师，React 经验较少" |
| **feedback** | 用户给出的纠正和确认 | "别 mock 数据库，上次 mock 过的测试过了但生产迁移挂了" |
| **project** | 项目的事实、决策、时间线 | "Auth 中间件重写是因为合规要求，不是技术债清理" |
| **reference** | 外部资源的指针 | "Pipeline bugs 在 Linear 的 INGEST 项目里追踪" |

**写 Memory 的原则：**
- 不要写能从代码/git 里推导出来的东西（文件路径、代码模式、架构）
- 不要写临时任务状态（用 Task 管理即可）
- 写"为什么"和"上下文"，方便未来的 Claude 判断这条记忆是否仍然有效
- 反馈类 memory 要写清楚 **Why** 和 **How to apply**

**Memory 文件的格式：**

```markdown
---
name: prefer-real-db-in-tests
description: 集成测试必须连接真实数据库，禁止 mock
type: feedback
---

集成测试必须连接真实数据库，禁止 mock。
**Why:** 上次 mock 过的测试通过了但生产迁移挂了，mock/prod 差异没发现。
**How to apply:** 涉及数据库操作的测试，一律用真实 test database。
```

---

## 2. 日常工作流

### 2.1 核心循环：Plan → Implement → Review

使用 Claude Code 的推荐工作流是一个三层循环：

```
Plan（计划）→ Implement（实现）→ Review（审查）→ 循环
```

**Plan 阶段：**
- 对于**任何非 trivial 的改动**，先用 Plan Mode 让 Claude 探索代码、设计方案
- 你审核方案、拍板后，再让它动手写代码
- 这避免了"写了一大堆发现方向错了"的浪费

**Implement 阶段：**
- Claude 按计划逐步实现，每个步骤完成后你确认结果
- 复杂任务拆成多个 Task 来跟踪进度
- 每完成一个逻辑单元就运行测试/验证

**Review 阶段：**
- 用 `/review` 或直接要求 Claude review 改动
- 检查：逻辑正确性、安全漏洞、边界情况、是否有过度工程
- Review 通过后再提交

### 2.2 Plan Mode 的使用

**什么时候必须进 Plan Mode：**
- 新功能实现
- 多文件改动（>2-3 个文件）
- 有多种实现方案可选
- 架构层面的决策
- 需求不够明确需要先探索

**什么时候不需要：**
- 单行/几行的 bug fix、typo
- 已有非常明确、详细的指令
- 纯探索/研究性质的提问

**Plan Mode 的工作方式：**
1. Claude 先通过 Explore Agent 搜索代码，理解现有实现
2. 用 Plan Agent 设计方案
3. 写计划文件到 `.claude/plans/`
4. 你审核计划、提出修改意见
5. 确认后 Claude 退出 Plan Mode，开始实现

### 2.3 Task 管理

对于超过 3 个步骤的复杂任务，使用 Task 系统来跟踪进度：

```
TaskCreate → TaskUpdate(in_progress) → 做 → TaskUpdate(completed) → 下一个
```

**最佳实践：**
- Task subject 用祈使句，简短可执行（如 "Add JWT verification middleware"）
- 完成任务后**立即**标记 completed，不要积攒
- 用 `addBlocks` / `addBlockedBy` 表达任务依赖
- 遇到新发现的任务及时创建

**示例：**

```
Task 1: Add JWT middleware (pending)
Task 2: Protect /api/private routes (pending, blockedBy: 1)
Task 3: Add tests for auth flow (pending, blockedBy: 1)
```

### 2.4 Agent 的使用

Claude Code 有几种专门的 sub-agent，各有适用场景：

| Agent | 用途 | 何时使用 |
|-------|------|---------|
| **Explore** | 快速只读搜索 | 搜索代码、找文件、grep 符号、定位定义。**只做搜索，不改代码。** |
| **Plan** | 软件架构设计 | 设计实现方案、评估架构决策、输出分步计划。 |
| **general-purpose** | 通用多步任务 | 需要搜索 + 分析 + 可能还要改代码的复杂任务。 |
| **claude-code-guide** | Claude Code 本身的问题 | "Claude 能做什么"、"怎么配置 X"、"这个功能怎么用" |

**使用 Agent 的原则：**
- 如果文件路径已知，直接用 Read/Edit — 不要绕 Agent
- 如果只知道符号名/关键字，用 Explore Agent 搜索
- 如果是开放性探索（"这个项目里认证是怎么做的？"），用 Explore Agent（medium/very thorough）
- 如果 Agent 已经启动了、任务没跑完，用 **SendMessage** 继续同一个 Agent，**不要重新开一个**（新 Agent 没有之前的上下文）
- 明确告诉 Agent 你是要它**只做研究**还是**写完代码**，它不知道你的意图

### 2.5 并行策略

**可以并行的场景：**
- 多个**互相独立**的搜索/探索任务（同时启动多个 Explore Agent）
- 多个**互相独立**的 bash 命令（如同时跑 `git status` 和 `git diff`）
- 写文件 + 其他独立操作

**不能并行的场景：**
- 后续操作依赖前一个操作的结果
- Edit 之后需要先看效果再做下一个 Edit

**实践经验：**
```
# 好的并行 — 三个独立搜索
Explore("找认证中间件在哪里")
Explore("找所有 API route 定义")
Explore("找测试文件里的 auth mock 模式")

# 坏的并行 — 第二个依赖第一个的结果
Explore("找 auth middleware") + Explore("读 auth middleware 并解释")  ← 第二个需要知道第一个的结果
```

---

## 3. 习惯与技巧

### 3.1 Prompt 写法

**给 Agent 写 prompt 时，用下面的公式：**

> **目标 + 背景 + 已知约束 + 产出格式**

例子（好的 prompt）：

```
我们在重构 auth 中间件，要把 session token 存储从 cookie 改成 Authorization header。
项目用的是 Go + chi router。
现有的中间件在 internal/middleware/auth.go。
我需要一个 plan：修改哪些文件、每个文件改什么、迁移步骤、如何保证向后兼容。
输出分步计划，每步标注风险等级。
```

例子（不好的 prompt）：

```
看看 auth，告诉我怎么改
```

**关键要点：**
- 告诉 Agent **你为什么做这件事**（业务/技术背景），它才能做好的判断
- 说清楚**已知的限制**（不能改什么、必须兼容什么）
- 明确**产出格式**（"200 字以内的报告"、"分步计划"、"只给结论不给过程"）
- 不要在 prompt 里说"根据你的发现去改" — 这是把理解任务丢给了 Agent。你应该自己消化 Agent 的研究结果再写指令

### 3.2 Agent vs 直接工具调用

**一个简单的决策树：**

```
你知道文件路径吗？
├── 是 → 直接用 Read / Edit
└── 否 → 你知道要搜什么符号/关键字吗？
    ├── 是且范围明确 → 直接用 Bash: grep/find
    └── 否或范围不明确 → 用 Explore Agent
```

**具体场景：**

| 场景 | 工具 |
|------|------|
| 读一个已知路径的文件 | `Read` |
| 搜一个函数名在哪些文件里出现 | `Bash: grep -r "funcName" .` |
| 找到某个功能的完整实现链路 | Explore Agent（medium） |
| 搜索多种命名约定、多个相关概念 | Explore Agent（very thorough） |
| 复杂多步研究任务 | general-purpose Agent |

### 3.3 权限配置

Claude Code 的权限系统让你可以精确控制哪些操作需要确认、哪些自动放行。

**推荐的分层策略：**

```json
// .claude/settings.json — 项目级，提交到 git
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
// .claude/settings.local.json — 本地覆盖，不提交
{
  "permissions": {
    "allow": [
      "Bash(npm:install*)",
      "Bash(docker:*)"
    ]
  }
}
```

**原则：**
- 只 allow 你确信安全的操作
- `settings.local.json` 不提交到 git（加到 `.gitignore`）
- 用 `/config` 命令或 `update-config` skill 来改配置，比手动编辑更安全
- `deny` 优先级高于 `allow`

### 3.4 Hooks 机制

Hooks 让 Claude Code 在某些事件发生时自动执行命令。适合：**"每次 X 之后都做 Y"** 的自动化需求。

**常用 Hooks：**

| Hook | 触发时机 | 典型用途 |
|------|---------|---------|
| `PostToolUse` | 工具调用后 | 自动格式化、lint |
| `PreToolUse` | 工具调用前 | 阻止危险操作 |
| `Notification` | 通知事件 | 桌面通知 |
| `Stop` | Claude 响应结束 | 自动运行测试 |
| `UserPromptSubmit` | 用户发送消息 | 注入额外上下文 |

**示例 — 每次 Edit 后自动 format：**

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

**注意事项：**
- Hook 里的命令执行失败**不会**回滚操作 — 不要依赖 hook 做关键校验
- Hook 由 Claude Code harness 执行，不是 Claude 执行的 — 所以 memory 和 preferences 不能代替 hook
- 复杂 hook 逻辑写脚本文件，在 hook command 里调用脚本

### 3.5 Git 工作流

**Claude Code 的 Git 安全协议（系统自带）：**

Claude 内置了以下约束：
- 不会自动 `git push --force` 到 main/master
- 不会跳过 hooks（`--no-verify`, `--no-gpg-sign`）
- 不会做破坏性操作（`reset --hard`, `checkout .`, `clean -f`）除非你明确要求
- 不会主动提交 — 只有你明确要求时才 commit

**推荐的日常节奏：**

1. **开始工作前：** 确认分支干净、了解当前状态
2. **实现过程中：** 每个逻辑单元完成后验证（跑测试、检查 UI）
3. **完成后：** 让 Claude 做 self-review，确认没有遗留 debug 代码、敏感信息
4. **提交时：** 明确告诉 Claude "commit these changes"，提供 commit message 方向

**Commit message 规范：**

```
<type>: <short description>

<optional body — 为什么改，不是改了什么>

Co-Authored-By: Claude Code <noreply@anthropic.com>
```

Claude 会自动追加 `Co-Authored-By` 行，标识这是 AI 辅助的提交。

### 3.6 常见反模式

以下是使用 Claude Code 时容易踩的坑：

**1. 小改动也进 Plan Mode**
- 改一行 typo、加个 log 语句，不需要计划
- 原则：改动越简单，流程越轻

**2. 鸿篇大论的 Prompt**
- 堆砌大量上下文 = 淹没关键信息
- 精炼：目标、约束、产出格式，就够了

**3. 让 Agent 做"理解 + 执行"二合一**
- "Based on your findings, fix the bug" — 这是把理解任务丢给了 Agent
- 正确做法：先让 Agent 研究 → 你消化结果 → 再给精确指令

**4. 在 Agent 里做"再来一次"**
- Agent 看不到之前的对话。如果需要继续同一个 Agent 的任务，用 SendMessage，不要重新 spawn

**5. 不开 Plan Mode 就开始大改动**
- 多文件重构不先出方案 → 写一半发现架构有问题 → 推倒重来
- 5 分钟的 plan 省下半小时的 rework

**6. Memory 当 TODO list 用**
- Memory 是跨会话的长期记忆，不应存当前任务的状态
- 临时跟踪用 Task 系统

**7. 不验证就宣布完成**
- Claude 不会自动跑浏览器验证 UI — 如果你让它改了前端代码，明确要求它启动 dev server 并在浏览器里测试

**8. 过度抽象/提前优化**
- "Add a factory pattern for the email sender" — 但你现在只有一个 email sender
- Three similar lines > premature abstraction

**9. Hook 里做关键业务校验**
- Hook 失败不会阻止操作执行
- 关键校验放在 CI 里，不要放在 Claude Code hook 里

**10. 权限全部 Allow**
- 宽泛的 `"allow": ["Bash(*)"]` = 裸奔
- 用 denylist 守住底线（`rm -rf`, `sudo`, `curl | sh`）

---

## 4. 速查表

### 常用命令

| 命令 | 作用 |
|------|------|
| `/init` | 为当前项目生成 CLAUDE.md |
| `/config` | 修改 Claude Code 配置（主题、模型等） |
| `/review` | Review 当前改动 |
| `/security-review` | 安全审查当前分支的改动 |
| `/simplify` | 审查代码的复用性和质量 |
| `/clear` | 清空当前会话上下文 |
| `/compact` | 压缩对话上下文（不丢失关键信息） |
| `/loop` | 定时循环执行某个任务 |
| `! command` | 直接在终端执行命令 |

### 工具决策树

```
需要搜索代码？
├── 知道文件路径 → Read
├── 知道符号名 → Bash: grep -r
├── 开放性搜索 → Explore Agent
└── 复杂多步研究 → general-purpose Agent

需要实现功能？
├── trivial（改一两行）→ 直接 Edit
├── 非 trivial → Plan Mode → 审核 → 实现
└── 有不确定因素 → Explore 先研究 → 再 Plan

需要追踪进度？
├── 单一步骤 → 直接做
└── 多步骤（≥3）→ TaskCreate 拆分
```

### 一句话总结

> **Plan before you code. Explore before you plan. Review before you commit.**
>
> 写代码前先计划，做计划前先探索，提交前先审查。

---

*这份文档本身也是一个活的参考 — 随着你对 Claude Code 的使用深入，可以持续更新里面的内容。*
