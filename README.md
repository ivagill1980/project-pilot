# Project Pilot

> 给 AI 编码 Agent 的**项目控制层**：让大型、长期、甚至已经混乱的项目始终保持
> **「全局可见 + 单点聚焦」**。

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Format](https://img.shields.io/badge/format-Agent%20Skills%20%2F%20SKILL.md-orange)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen)
![Stack](https://img.shields.io/badge/deps-none-lightgrey)

[English](./README_EN.md) · [可视化指南](./project-pilot-guide.html) · [更新日志](./CHANGELOG.md) · [参与贡献](./CONTRIBUTING.md)

---

## 目录

- [它解决什么问题](#它解决什么问题)
- [核心模型](#核心模型)
- [每轮导航 HUD](#每轮导航-hud)
- [三种模式](#三种模式)
- [安装](#安装)
- [命令速查](#命令速查)
- [它会在项目里留下什么](#它会在项目里留下什么)
- [状态词汇表](#状态词汇表)
- [和其他方案的区别](#和其他方案的区别)
- [仓库结构](#仓库结构)
- [适用场景 / 不适用场景](#适用场景--不适用场景)
- [路线图](#路线图)
- [参考来源与致谢](#参考来源与致谢)
- [许可证](#许可证)

---

## 它解决什么问题

Agent 在长周期项目里失败，通常不是因为写不好代码，而是因为**失去了坐标**：

| 症状 | 本质 |
| --- | --- |
| 做了一堆局部正确的事，但与最终目标脱节 | 局部执行与全局目标断开 |
| 隔几天回来，不知道自己做到哪了 | 没有可恢复的持久状态 |
| 老项目越改越乱，文档说一套代码是另一套 | 声明状态 ≠ 观测状态 |
| UI / API / schema 都在，功能却跑不通 | 假完成（False Completion） |
| 为了一个小问题绕出去，再也回不来 | 绕路没有返回点（Return Target） |
| 进度"感觉做了一半"，但说不出依据 | 进度不是从证据算出来的 |

Project Pilot 不改你的技术栈，也不生成代码。它给 Agent 加一层**项目控制纪律**：
一次只推进一件事，但每一刻都把这件事放回整张地图里显示。

> **One Thing in Context**
> 一次只执行一件事，同时始终显示这件事在整个项目中的位置，以及它如何推动项目前进。

---

## 核心模型

工作被建模成四层稳定层级，进度由叶子节点逐级向上汇总：

```text
PROJECT
└── PHASE
    └── MILESTONE
        └── TASK
            └── STEP   ← 唯一活跃执行点
```

设计要点：

- **高层地图全局可见，细节按需展开**——只深度规划当前或下一个里程碑，避免维护一份 500 步的死计划。
- **只有一个活跃执行点**——后台 Agent 可以并行，但用户面向的主线坐标必须唯一且稳定。
- **进度来自证据**——每个节点的状态必须由构建 / 测试 / 运行时行为等证据支撑，不允许凭感觉填百分比。

---

## 每轮导航 HUD

每一次实质性项目推进，Agent 都会在回答顶部给出固定结构的导航头：

```text
🎯 PROJECT
上线一个可注册、分析财报、生成报告并可收费的 MVP
Overall: 38%

📍 YOU ARE HERE
Discovery → Product Definition → Target User → Step 1/3

🧭 WHY THIS MATTERS
目标用户决定数据流程、报告深度和产品边界。先定它可以避免架构提前发散。

🔨 NOW
选择第一类目标用户。

✅ DONE WHEN
- 目标用户写入项目基线
- 能据此定义首个核心用户旅程
```

绕路时额外显示返回点：

```text
↩ RETURN TO
MVP → Dashboard → Chart Rendering → Step 4
```

默认配重：**10–20% 全局定位 + 80–90% 当前工作**。隐藏无关细节，但绝不隐藏目的地和你所在的位置。

---

## 三种模式

| 模式 | 触发时机 | 做什么 |
| --- | --- | --- |
| **BUILD** | 新项目，或状态基本连贯 | `Orient → Map → Select → Align → Act → Verify → Record → Navigate` 循环推进 |
| **RECONCILE** | 怀疑项目在漂移，但还没烂透 | 冻结"未经验证的断言"，比对期望 vs 观测，识别漂移并分级（NORMAL / RECONCILE / RESCUE） |
| **RESCUE** | 老项目接管、严重漂移、反复修不好、计划过期 | 项目考古：`observe → verify → reconstruct → diagnose → rebaseline → stabilize → continue` |

### Rescue 模式的两条硬规矩

1. **先观察，再动手。** 除非是必须立即止血的生产事故且用户明确要求，考古阶段一律只读，不改代码。
2. **重建基线，而不是假装老计划还有效。** 老计划作为历史保留（移至 `plans/abandoned/`），新基线从今天验证过的现实出发。

Rescue 会按固定优先级止血：

```text
1. 阻止数据 / 安全 / 生产损害
2. 恢复可信的 build / test / CI 信号
3. 收尾危险的半成品功能
4. 解决关键路径上的阻塞
5. 修复项目地图与持久知识
6. 回到产品交付
```

### 漂移检测清单

Rescue 会逐项检查：计划漂移、文档漂移、架构漂移、范围漂移、TODO 漂移、
**假完成**、验证漂移、决策漂移。

---

## 安装

本项目是标准的 [Agent Skills](https://github.com/anthropics/skills) 格式，
核心只有一个 `SKILL.md`，**无依赖、无构建步骤、无网络调用**。

### Codex CLI

```bash
# 用户级：所有项目可用
git clone https://github.com/ivagill1980/project-pilot.git ~/.codex/skills/project-pilot

# 项目级：随仓库提交，团队共享
mkdir -p .codex/skills
cp -r project-pilot .codex/skills/
```

### 其他 Agent

SKILL.md 是跨 Agent 的通用格式，放到对应目录即可，无需任何修改：

| Agent | 用户级路径 | 项目级路径 |
| --- | --- | --- |
| Codex CLI | `~/.codex/skills/` | `.codex/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` | `.workbuddy/skills/` |

> 目录名即技能名，目录内必须直接包含 `SKILL.md`。
> 安装后**重启 / 新建会话**，Agent 会重新扫描技能目录。

### 验证

```bash
ls ~/.codex/skills/project-pilot/SKILL.md
```

然后直接对 Agent 说一句人话即可触发，不需要记命令：

- 「接管并梳理一下这个项目」
- 「我乱了」
- 「继续」

---

## 命令速查

全部支持自然语言等价说法，不必记英文。

| 命令 | 作用 |
| --- | --- |
| `继续` / `continue` | 接受当前推荐路径，推进到下一个安全动作 |
| `我乱了` / `where am I?` | **空间恢复**：重建并展示目标、进度、路线、当前坐标、返回点、最近完成项、下一步 |
| `看全局` / `zoom out` | 展示阶段/里程碑级全局地图、风险、关键路径 |
| `看当前` / `zoom in` | 聚焦当前任务与步骤、相关文件、阻塞项、验收门槛 |
| `为什么` / `why` | 只解释当前动作为什么存在、解锁了什么 |
| `我不懂` / `explain simpler` | 用更简单的语言重讲当前步骤，不改计划 |
| `换一个` / `alternative` | 提供最多三条实质不同的路线，含推荐与权衡 |
| `先放着` / `park it` | 丢进 Parking Lot，注意力回到主线 |
| `接管项目` / `rescue` / `梳理项目` | 进入 RESCUE 模式，开始项目考古 |
| `校准` / `reconcile` | 比对期望状态与现实，但不自动重建整张路线图 |
| `重新基线` / `rebaseline` | 从当前现实出发建立新基线 |
| `暂停` / `checkpoint` | 写入检查点，让新会话以最小代价恢复 |
| `今天收尾` / `wrap up` | 跑 Learning Loop：总结、沉淀、更新状态、写检查点、给出干净的再入点 |

决策负担也有规矩：需要决策时，给出**一个推荐默认值 + 最多两个备选**，
说明推荐理由和对地图的影响，`继续` 即可接受。

---

## 它会在项目里留下什么

若项目中尚无等价约定，Skill 会在 `.project-pilot/` 下维护一组持久控制文件：

```text
.project-pilot/
├── STATE.md          # 目标、当前坐标、下一步、健康度
├── MAP.md            # Phase → Milestone → Task → Step 层级与状态
├── HEALTH.md         # 项目控制健康（与产品完成度分开统计）
├── RECOVERY.md       # Rescue 期间的证据、矛盾、稳定化里程碑
├── PARKING_LOT.md    # 暂存灵感，不静默占用主线范围
├── DECISIONS.md      # 决策日志
├── SESSION_LOG.md    # 会话日志
├── plans/
│   ├── active/
│   ├── completed/
│   └── abandoned/    # 老计划作为历史保留，不静默覆盖
└── snapshots/
```

若仓库已有 `AGENTS.md`、`docs/` 等约定，Skill 会优先复用现有结构，不制造重复的 competing 结构。

状态 schema（YAML 摘要）：

```yaml
project:  { name, final_goal, success_criteria, mode, baseline_id, baseline_date, overall_progress }
location: { phase, milestone, task, step, return_to }
current:  { purpose, done_when, blockers, next_action }
health:   { build, tests, ci, docs_alignment, architecture_alignment }
recent:   { completed, decisions, discoveries }
```

> 需要把项目状态提交进 Git 就提交；不想污染仓库就加进 `.gitignore`。
> 本仓库的默认 `.gitignore` 忽略了 `.project-pilot/`。

---

## 状态词汇表

进度必须由证据推导，不允许拍脑袋填百分比。

| 标记 | 状态 | 含义 |
| --- | --- | --- |
| ✅ | `VERIFIED` | 有证据证明已完成 |
| ◐ | `PARTIAL` | 已实质实现但未完成 |
| ⚠ | `AT RISK` | 存在但不可靠、正在漂移或被阻塞 |
| ✕ | `BROKEN` | 已知不可用 |
| ○ | `NOT STARTED` | 有意未开始 |
| ? | `UNKNOWN` | 证据不足 |

规则：

- 父节点百分比由子节点汇总，`UNKNOWN` 不得被静默当作已完成。
- 无权重信息时，同层级等权，并明确声明当前采用的权重策略。
- **不知道就写 `UNKNOWN`**，并为影响规划的关键未知建立调查步骤。

证据优先级（冲突时自上而下）：

```text
运行行为 / 生产证据 > 测试 / CI / 类型检查 / lint > 当前代码与配置
  > 近期已接受的提交 > 已接受的 ADR / 规格 > 维护中的文档 > 旧 roadmap / TODO > 假设与记忆
```

---

## 和其他方案的区别

| | TODO / 任务列表 | 一次性规划 Prompt | **Project Pilot** |
| --- | --- | --- | --- |
| 产出 | 任务清单 | 一份文档 | 持续维护的项目控制状态 |
| 全局定位 | 无 | 生成时有，之后消失 | **每轮显示在顶部** |
| 进度来源 | 手动勾选 | 估算 | **证据推导** |
| 中断恢复 | 靠记忆 | 重读文档 | **`我乱了` 一键重建坐标** |
| 老项目接管 | 不适用 | 容易照抄过期文档 | **只读考古 + 重新基线** |
| 范围控制 | 无 | 无 | **Parking Lot + Return Target** |

---

## 仓库结构

```text
project-pilot/
├── SKILL.md                  # 技能本体：Agent 读取的全部指令（唯一必需文件）
├── project-pilot-guide.html  # 中文可视化指南，单文件、零依赖，浏览器直接打开
├── README.md                 # 本文件
├── README_EN.md              # English README
├── CHANGELOG.md              # 遵循 Keep a Changelog
├── CONTRIBUTING.md           # 贡献指引
├── CREDITS.md                # 第三方模式名称归属与上游授权状态
├── LICENSE                   # MIT
└── .gitignore
```

想先建立直觉，直接打开 `project-pilot-guide.html`：核心模型、HUD、三种模式、
命令、状态文件、对话演示都在里面。

---

## 适用场景 / 不适用场景

**适合**

- 多阶段、长周期、规模较大的项目
- 接手别人（或半年前的自己）留下的 brownfield 项目
- 容易被打断、需要低成本重返的长期工作
- 需要"可信进度"而不是"感觉差不多"的场合
- 多个后台 Agent 并行时的外层编排与收口

**不适合**

- 一次性脚本、单文件小改动
- 纯问答、纯查资料
- 已经很小且完全在脑子里的任务——此时导航头是纯噪音

---

## 路线图

v0.2 方向（欢迎 PR，见 [CONTRIBUTING.md](./CONTRIBUTING.md)）：

- [ ] 与上游 `augmented-coding-patterns` 确认授权状态，或改为零外部依赖的自有策略标签
- [ ] `.project-pilot/` 各状态文件的可复制模板
- [ ] 可选的 init / 校验脚本，把确定性工作从 Agent 手里卸下来
- [ ] 更细的进度权重策略（关键路径加权）
- [ ] 更完整的中英文命令别名覆盖
- [ ] 更多 Rescue 真实案例与对照样本

---

## 设计意图

Project Pilot 算成功的标准是：

> 用户停一天、一周、甚至一个月再回来，项目叙事不断线；
> 局部工作永远不与最终目标失去连接；
> 一个混乱的仓库可以被重新进入，而不必假装那些过期的文档就是现实。

它要让一个大项目**感觉可导航**，而不是让它**看起来很小**。

---

## 参考来源与致谢

`SKILL.md` 中的「模式路由器（Pattern Router）」一节，策略标签来自
[**Augmented Coding Patterns**](https://github.com/lexler/augmented-coding-patterns)（作者 [@lexler](https://github.com/lexler)），
一个关于「用 LLM 开发软件」的模式与反模式集合，在线阅读：<https://lexler.github.io/augmented-coding-patterns/>

本项目**只引用模式名称**作为 Agent 内部的策略索引，未复制、未翻译、未转载其任何正文内容。
完整的引用清单（含每个模式的触发情境与上游链接）见 [CREDITS.md](./CREDITS.md)。

> ⚠️ **上游许可证状态**：截至 2026-09-02，上游仓库未声明任何许可证
> （GitHub API `license` 为 `null`，根目录无 `LICENSE` 文件），
> 按 GitHub 服务条款默认**保留全部权利**。
> 若你打算二次分发或商业化本 skill，请先确认授权，或直接移除 `SKILL.md` 的
> Pattern Router 一节 —— 该节为可选增强，移除后 12 条 invariants 与三种模式工作流不受影响。
> 详见 [CREDITS.md](./CREDITS.md)。

除 Pattern Router 外，`SKILL.md` 的其余内容（12 条 Core Invariants、三种模式、
`.project-pilot/` 约定、命令集、HUD 格式）以及 `project-pilot-guide.html` 均为本项目原创。

---

## 许可证

[MIT](./LICENSE) © 2026 Project Pilot contributors

第三方模式名称的归属与上游授权状态见 [CREDITS.md](./CREDITS.md)。
