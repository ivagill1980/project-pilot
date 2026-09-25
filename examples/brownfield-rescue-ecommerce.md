# Example: brownfield rescue

User:

> 这个项目做了半年，越来越乱。接管并梳理一下。

Project Pilot:

```text
🎯 PROJECT
最终目标：正在从现有资料和代码重建

🛟 MODE
RESCUE → Project Archaeology

📍 CURRENT STATUS
Map confidence: low
Code changes: none during archaeology

🔎 OBSERVING NOW
先确认仓库事实：结构、构建方式、测试、近期 Git 历史、现有 roadmap/AGENTS/docs。

我会把“文档声称完成”和“代码/测试证明确实完成”分开。

🔨 NOW
建立 Reality Snapshot，然后重建项目地图。
```

After archaeology:

```text
🎯 FINAL GOAL
Public Beta：用户可注册、导入数据、完成分析并导出报告

📊 RECONSTRUCTED PROGRESS
Project: 61% (milestone-weighted; 4 critical unknowns remain)
Recovery: 0%

📍 REAL LOCATION
MVP → Billing & Integration → Subscription Webhook

🩺 PROJECT HEALTH
核心产品已存在，但 CI、Billing 和 roadmap 彼此不一致，继续增加 feature 会扩大失控。

🚨 TOP 3 CONTROL PROBLEMS
1. 8 个主线测试失败，但 roadmap 把对应 milestone 标成完成。
2. Billing UI、API、schema 都存在，但 webhook 未接通：FALSE COMPLETION。
3. 两份 roadmap 对当前优先级互相矛盾。

🧭 RECOMMENDED ROUTE
进入 Stabilization：恢复可信 CI → 收尾 Billing → 重建 baseline → 返回 Dashboard 主线。

↩ RETURN TO
MVP → Dashboard → Chart Rendering → Step 4

🔨 NEXT
先定位 8 个失败测试是否来自同一个基础设施问题。
```
