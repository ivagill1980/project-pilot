# 参考来源与致谢 / Credits

## Augmented Coding Patterns

Project Pilot 的「模式路由器（Pattern Router）」（`references/pattern-router.md`）与「病因诊断」（`references/diagnosis.md`）两节，其策略标签来自
[**Augmented Coding Patterns**](https://github.com/lexler/augmented-coding-patterns)，
作者 **[@lexler](https://github.com/lexler)**。

> 该项目是一个持续演进的、关于「用 LLM 开发软件」的模式与反模式集合。
> 在线阅读：<https://lexler.github.io/augmented-coding-patterns/>

本项目对它的使用方式仅限于：

- **引用模式名称**作为 Agent 内部的策略标签（strategy labels），用于在特定情境下选择行为策略；
- 未复制、未翻译、未转载其任何模式正文、示例或文档内容。

模式名称在本项目中仅作为「何时采用何种行为策略」的索引，Agent 不会向用户输出这些标签。

### 引用清单

下表列出 `references/pattern-router.md`（由 `SKILL.md` 按需引用）中出现的全部模式标签及其触发情境，链接指向上游对应条目。

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

### 病因层标签（`references/diagnosis.md`）

下表列出病因诊断中用于归因的标签、对应的可观察症状，以及上游条目。

| 可观察症状 | 标签 | 类型 | 上游条目 |
| --- | --- | --- | --- |
| 规则写下来仍被无视 | Selective Hearing | 障碍 | [selective-hearing](https://lexler.github.io/augmented-coding-patterns/obstacles/selective-hearing/) |
| 会话越长表现越差 | Context Rot | 障碍 | [context-rot](https://lexler.github.io/augmented-coding-patterns/obstacles/context-rot/) |
| 同样的指令每个会话都要重复 | Cannot Learn | 障碍 | [cannot-learn](https://lexler.github.io/augmented-coding-patterns/obstacles/cannot-learn/) |
| 同一个 bug 反复「修好」，越修越乱 | Sunk Cost | 反模式 | [sunk-cost](https://lexler.github.io/augmented-coding-patterns/anti-patterns/sunk-cost/) |
| 两份文档对「项目是什么」各说各话 | Silent Misalignment | 反模式 | [silent-misalignment](https://lexler.github.io/augmented-coding-patterns/anti-patterns/silent-misalignment/) |
| 开了一堆，一个都没收口 | Cognitive Overload | 反模式 | [cognitive-overload](https://lexler.github.io/augmented-coding-patterns/anti-patterns/cognitive-overload/) |
| 交付没有人能评审 | Flying Blind | 反模式 | [flying-blind](https://lexler.github.io/augmented-coding-patterns/anti-patterns/flying-blind/) |
| 对库或 API 的断言自信但错误 | Perfect Recall Fallacy | 反模式 | [perfect-recall-fallacy](https://lexler.github.io/augmented-coding-patterns/anti-patterns/perfect-recall-fallacy/) |
| 一次事故被升格为全局规则 | Obsess Over Rules | 反模式 | [obsess-over-rules](https://lexler.github.io/augmented-coding-patterns/anti-patterns/obsess-over-rules/) |

### 上游许可状态与使用立场

截至 2026-09-02，上游仓库 `lexler/augmented-coding-patterns`：

- GitHub API 的 `license` 字段为 `null`；
- 根目录不存在 `LICENSE` / `LICENSE.md` / `COPYING`；
- README 与 CONTRIBUTE.md 均未声明任何许可证。

按 GitHub 服务条款，未声明许可证的公开仓库**默认保留全部权利（all rights reserved）**。

本项目的立场：

1. **本地自用** —— 本 skill 为个人本地使用，不做二次分发、不商业化。上面记录上游的许可
   状态，是为了把事实写清楚，不是为了设置使用门槛。
2. **只借标签，不搬运正文** —— 模式名称在这里充当行为策略的索引；上游的正文、示例与文档
   是上游自己的表达，本项目不转载。
3. **完整署名并链接回上游** —— 见上表与本文件。上游名称是这一领域最省认知成本的共同词汇，
   本项目不把「替换为自有名称」当作方向。
4. 若上游作者提出异议，或要求调整署名方式，本项目将**立即配合处理**。

### 其他

- `SKILL.md` 的 14 条 Core Invariants、`references/diagnosis.md` 的病因层归因、BUILD / RECONCILE / RESCUE 三种模式、
  `.project-pilot/` 状态文件约定、命令集与 HUD 格式，均为本项目原创内容，
  以 [MIT](./LICENSE) 发布。
- `project-pilot-guide.html` 为本项目原创的可视化指南（单文件、零依赖）。
