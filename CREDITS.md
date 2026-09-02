# 参考来源与致谢 / Credits

## Augmented Coding Patterns

Project Pilot 的「模式路由器（Pattern Router）」一节，其策略标签来自
[**Augmented Coding Patterns**](https://github.com/lexler/augmented-coding-patterns)，
作者 **[@lexler](https://github.com/lexler)**。

> 该项目是一个持续演进的、关于「用 LLM 开发软件」的模式与反模式集合。
> 在线阅读：<https://lexler.github.io/augmented-coding-patterns/>

本项目对它的使用方式仅限于：

- **引用模式名称**作为 Agent 内部的策略标签（strategy labels），用于在特定情境下选择行为策略；
- 未复制、未翻译、未转载其任何模式正文、示例或文档内容。

模式名称在本项目中仅作为「何时采用何种行为策略」的索引，Agent 不会向用户输出这些标签。

### 引用清单

下表列出 `SKILL.md` 中出现的全部模式标签及其触发情境，链接指向上游对应条目。

| 触发情境 | 模式标签 | 上游条目 |
| --- | --- | --- |
| 复杂度正在导致失败 | Chain of Small Steps | [chain-of-small-steps](https://lexler.github.io/augmented-coding-patterns/patterns/chain-of-small-steps/) |
| 复杂度正在导致失败 | Chunking | [chunking](https://lexler.github.io/augmented-coding-patterns/patterns/chunking/) |
| 复杂度正在导致失败 | Focused Agent | [focused-agent](https://lexler.github.io/augmented-coding-patterns/patterns/focused-agent/) |
| 复杂度正在导致失败 | Phased Delivery | [phased-delivery](https://lexler.github.io/augmented-coding-patterns/patterns/phased-delivery/) |
| 上下文正在衰减 | Context Management | [context-management](https://lexler.github.io/augmented-coding-patterns/patterns/context-management/) |
| 上下文正在衰减 | Ground Rules | [ground-rules](https://lexler.github.io/augmented-coding-patterns/patterns/ground-rules/) |
| 上下文正在衰减 | Reference Docs | [reference-docs](https://lexler.github.io/augmented-coding-patterns/patterns/reference-docs/) |
| 上下文正在衰减 | Knowledge Checkpoint | [knowledge-checkpoint](https://lexler.github.io/augmented-coding-patterns/patterns/knowledge-checkpoint/) |
| 上下文正在衰减 | Extract Knowledge | [extract-knowledge](https://lexler.github.io/augmented-coding-patterns/patterns/extract-knowledge/) |
| 上下文正在衰减 | Learning Loop | [learning-loop](https://lexler.github.io/augmented-coding-patterns/patterns/learning-loop/) |
| 上下文正在衰减 | Semantic Zoom | [semantic-zoom](https://lexler.github.io/augmented-coding-patterns/patterns/semantic-zoom/) |
| 上下文正在衰减 | Noise Cancellation | [noise-cancellation](https://lexler.github.io/augmented-coding-patterns/patterns/noise-cancellation/) |
| 工作不可靠或不确定 | Feedback Loop | [feedback-loop](https://lexler.github.io/augmented-coding-patterns/patterns/feedback-loop/) |
| 工作不可靠或不确定 | Constrained Tests | [constrained-tests](https://lexler.github.io/augmented-coding-patterns/patterns/constrained-tests/) |
| 工作不可靠或不确定 | Offload Deterministic | [offload-deterministic](https://lexler.github.io/augmented-coding-patterns/patterns/offload-deterministic/) |
| 工作不可靠或不确定 | Hooks | [hooks](https://lexler.github.io/augmented-coding-patterns/patterns/hooks/) |
| 工作不可靠或不确定 | Approved Scenarios | [approved-scenarios](https://lexler.github.io/augmented-coding-patterns/patterns/approved-scenarios/) |
| 工作不可靠或不确定 | Approved Logs | [approved-logs](https://lexler.github.io/augmented-coding-patterns/patterns/approved-logs/) |
| 人与 Agent 可能不同频 | Check Alignment | [check-alignment](https://lexler.github.io/augmented-coding-patterns/patterns/check-alignment/) |
| 人与 Agent 可能不同频 | Active Partner | [active-partner](https://lexler.github.io/augmented-coding-patterns/patterns/active-partner/) |
| 人与 Agent 可能不同频 | ROSE Feedback | [rose-feedback](https://lexler.github.io/augmented-coding-patterns/patterns/rose-feedback/) |
| 需要探索方案空间 | Cast Wide | [cast-wide](https://lexler.github.io/augmented-coding-patterns/patterns/cast-wide/) |
| 需要探索方案空间 | Parallel Implementations | [parallel-implementations](https://lexler.github.io/augmented-coding-patterns/patterns/parallel-implementations/) |
| 需要探索方案空间 | Softest Prototype | [softest-prototype](https://lexler.github.io/augmented-coding-patterns/patterns/softest-prototype/) |
| 需要探索方案空间 | Take All Paths | [take-all-paths](https://lexler.github.io/augmented-coding-patterns/patterns/take-all-paths/) |
| 需要探索方案空间 | Refinement Loop | [refinement-loop](https://lexler.github.io/augmented-coding-patterns/patterns/refinement-loop/) |
| 支线任务威胁主线 | Yak Shave Delegation | [yak-shave-delegation](https://lexler.github.io/augmented-coding-patterns/patterns/yak-shave-delegation/) |
| 需要多 Agent 吞吐 | Background Agent | [background-agent](https://lexler.github.io/augmented-coding-patterns/patterns/background-agent/) |
| 需要多 Agent 吞吐 | Orchestrator | [orchestrator](https://lexler.github.io/augmented-coding-patterns/patterns/orchestrator/) |
| 需要多 Agent 吞吐 | Overnight Batch | [overnight-batch](https://lexler.github.io/augmented-coding-patterns/patterns/overnight-batch/) |
| 成本 / 智能路由 | Smart Plan, Cheap Execution | [smart-plan-cheap-execution](https://lexler.github.io/augmented-coding-patterns/patterns/smart-plan-cheap-execution/) |
| 成本 / 智能路由 | Advisor Strategy | [advisor-strategy](https://lexler.github.io/augmented-coding-patterns/patterns/advisor-strategy/) |

### 许可证状态（重要）

截至 2026-09-02，上游仓库 `lexler/augmented-coding-patterns`：

- GitHub API 的 `license` 字段为 `null`；
- 根目录不存在 `LICENSE` / `LICENSE.md` / `COPYING`；
- README 与 CONTRIBUTE.md 均未声明任何许可证。

按 GitHub 服务条款，未声明许可证的公开仓库**默认保留全部权利（all rights reserved）**。

因此本项目的立场是：

1. **仅引用模式名称，不复制内容** —— 模式名称在本项目中充当行为策略的索引标签，
   不构成对其表达内容的再发布；
2. **完整署名并链接回上游** —— 见上表与本文件；
3. 若上游作者提出异议，或要求移除/调整署名方式，本项目将**立即配合处理**。

若你打算对本 skill 进行二次分发或商业化，请先向上游确认授权状态，或考虑移除
`SKILL.md` 中的 Pattern Router 一节（该节为可选增强，删除后 skill 的核心
12 条 invariants 与三种模式工作流不受影响）。

### 其他

- `SKILL.md` 的 12 条 Core Invariants、BUILD / RECONCILE / RESCUE 三种模式、
  `.project-pilot/` 状态文件约定、命令集与 HUD 格式，均为本项目原创内容，
  以 [MIT](./LICENSE) 发布。
- `project-pilot-guide.html` 为本项目原创的可视化指南（单文件、零依赖）。
