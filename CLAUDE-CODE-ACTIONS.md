# Claude Code 行动指南

按时机组织的操作清单。你只需要在脑子里记住"什么时候该做什么"，具体细节 Claude 会配合你执行。

---

## 1. 项目第一天（一次性搭建）

### 1.1 复制 CLAUDE 模板

```
cp CLAUDE-TEMPLATE.md ./新项目/CLAUDE.md
```

### 1.2 访谈式定制 CLAUDE.md

对 Claude 说：

> "read this CLAUDE.md template, then interview me to fill in the Tech Stack, Conventions, Key Paths, and Constraints sections. Ask me one section at a time."

等你回答完后，Claude 会填好上半部分，下半部分的 Workflow 规则原样保留。

### 1.3 搭基础设施

按顺序完成：

| 动作 | 怎么说 |
|------|--------|
| 初始化 git | "git init，创建 .gitignore" |
| 配置 hooks | "配置 Stop hook 播放提示音，PermissionRequest hook 播放另一个提示音" |
| 设权限 | "把常用的安全命令加到 allow list，deny rm -rf / sudo" |
| 初次 commit | "commit these changes" |

---

## 2. 日常开发循环

根据你要做的事情，选择正确的路径：

### 2.1 判断树

```
你打算做的事情...

├── 改一行 / typo / 加个 log？
│   └── 直接说 → Claude 直接改
│
├── 新功能 / 重构 / 改 >2 个文件？
│   └── "我们先 Plan 一下" → Plan Mode → 审方案 → 实现
│
├── 有 3+ 个步骤的复杂任务？
│   └── "拆成 Tasks，设好依赖" → 一个接一个完成
│
├── 需要搜代码但不知道文件在哪？
│   └── "帮我查一下 X 在哪里" → Explore Agent
│
└── 改完了？
    └── "Review 一下改动" → 检查 → "commit"
```

### 2.2 什么时候存 Memory

**原则：对重要的项目决策，显式说比依赖自动检测更可靠。**

Claude 会在你纠正它时自动保存 feedback memory。但 project memory（架构决策、废弃的方案、为什么选了 A 而不是 B）不会自动触发 — 这些你需要显式告诉它。

| 场景 | 怎么说 |
|------|--------|
| Claude 犯了一个方向性错误，你纠正了 | "记住这个" |
| 你发现了一个重要的项目约束 | "把这个记到 project memory" |
| 你觉得某个偏好以后都用得上 | "存成 user memory" |
| 放弃了一个方案 / 功能方向 | "记住我们为什么放弃了 X，存成 project memory" |
| 更新了 CLAUDE.md 的 Scope / Active Decisions，移除了某项 | 同时把移除的*原因*存成 project memory |

**自然触发点：** 每次更新 CLAUDE.md 的 `## Scope` 或 `## Active Decisions` 时，有东西被移除 — 问自己"六个月后我还记得为什么放弃它吗？"不确定就存 memory。

**信息放哪 — 速查：**

| 放哪 | 适合什么 | 加载时机 |
|------|---------|---------|
| CLAUDE.md | 当前技术栈、约定、Scope、Active Decisions、Constraints | 每次会话 |
| Memory (project) | 废弃方案的原因、历史决策、架构选择理由 | 按需检索 |
| Memory (feedback) | 用户纠正和偏好 | 按需检索 |
| Task | 当前会话的工作进度 | 仅当前会话 |

不需要存的：当前任务进度细节（用 Task）、能从代码读出来的东西（读代码就行）。

### 2.3 什么时候更新 CLAUDE.md

| 触发事件 | 怎么说 |
|----------|--------|
| 团队确定了新的编码约定 | "更新 CLAUDE.md，加一条约定" |
| 发现一个不能改的模块 | "更新 CLAUDE.md 的 Constraints" |
| 换了技术栈 | "更新 CLAUDE.md 的 Tech Stack" |

**原则**：每次 Claude 因为"不知道约定"而犯错，就把那条约定写进 CLAUDE.md。

---

## 3. 验证与纠错

### 3.1 让 Claude 验证自己的工作

Claude 说"完成了"不代表真的完成了。你必须主动要求：

| 场景 | 怎么说 |
|------|--------|
| 改前端代码 | "启动 dev server，在浏览器里测试" |
| 改后端逻辑 | "跑相关测试" |
| 改 CLI 工具 | "用几个不同输入跑一下看看输出" |
| 改了配置 | "验证配置能正确加载" |

### 3.2 当 Claude 走偏了

不要忍着一轮一轮纠。发现方向问题立刻打断：

| 问题 | 怎么说 |
|------|--------|
| 过度工程 | "太复杂了，保持简单。三个相似行 > 过早抽象" |
| 遗漏边界情况 | "也考虑一下 X 场景" |
| 方向完全错了 | "不对，应该用 Y 方案，因为 Z。重来。" |
| 幻觉 / 编造 API | "那个 API 不存在，先查文档确认" |

### 3.3 权限渐进策略

开始项目时用默认权限（确认弹窗多）。用了一周后：

> "帮我用 fewer-permission-prompts skill 分析，把高频安全命令加到 allow list"

不要一开始就 `allow: ["Bash(*)"]`。

---

## 4. 会话管理

| 信号 | 行动 |
|------|------|
| Claude 回复明显变慢 | `/compact` — 压缩上下文 |
| 话题完全换了 | `/clear` — 清空会话，重开 |
| 上下文用了很久，当前任务已完成 | `/compact` — 清理掉无关历史 |
| Claude 开始表现出"记忆错乱" | `/clear` 然后重新描述当前任务 |

**规则**：`/clear` = 全新开始；`/compact` = 保留关键信息，丢掉过程细节。

---

## 5. 收尾与提交

```
改动做完了
  → "review 一下这些改动"（检查边界、安全、过度工程）
  → "跑测试"（如果项目有测试）
  → "commit these changes"（提供 commit message 方向）
  → 推送到远程（如果有）
```

### Commit 格式

```
<type>: <简短描述>
         ^— feat / fix / chore / docs / refactor / test

Body 写"为什么改"，不是"改了什么"

Co-Authored-By: Claude Code <noreply@anthropic.com>
```

Claude 会自动追加 `Co-Authored-By` 行。

---

## 6. 学习记录

### 已实践过的概念（2026-05-05，cc_test 项目）

| 概念 | 怎么学的 | 掌握程度 |
|------|---------|---------|
| CLAUDE.md | 手写了项目指令，做了模板 | ✅ 会用 |
| Plan Mode | 设计 markdown 预览器 | ✅ 会用 |
| Task 系统 | 4 个 Task + 依赖关系 | ✅ 会用 |
| Memory | 存了 user_role，理解了隔离 | ✅ 理解 |
| Hooks（Stop + PermissionRequest） | 配了双提示音 | ✅ 会用 |
| Git 工作流 | init / ignore / commit | ✅ 会用 |
| Agent（Explore/Plan/general-purpose） | 理论了解了 | 🟡 理论 OK，没实际用过 |
| 权限配置 | 基础的 allow/deny | 🟡 用过但没系统调优 |
| /compact / /clear | 理论了解了 | 🟡 还没实践过 |

### 待学习清单

准备在**更复杂的项目**中练习：

- **Explore Agent 实战** — 在陌生代码库里搜索、定位功能
- **多次 Plan-Implement-Review 循环** — 迭代式开发
- **中断与恢复** — 长任务被中断后如何让 Claude 继续
- **Hooks 进阶** — PostToolUse 自动 format、PreToolUse 阻断危险操作
- **多 Agent 并行** — 同时搜索多个方面
- **PR 工作流** — 分支、推送、PR 描述

### 什么时候回来看这份清单

- 接手一个新项目，不知道该从哪开始
- 遇到一个复杂功能，不确定流程
- 发现某个概念（如 Agent）只在理论层面理解，想找机会实践
