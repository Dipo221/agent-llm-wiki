---
type: comparison
title: 用 Survey 的四模組架構對照五篇論文
sources: [wang2023-agent-survey, wei2022-chain-of-thought, yao2022-react, schick2023-toolformer, shinn2023-reflexion, park2023-generative-agents]
related: [papers/wang2023-agent-survey.md, concepts/planning.md, concepts/agent-memory.md, concepts/tool-use.md, concepts/self-reflection.md]
updated: 2026-11-17
---

# 用 Survey 的四模組架構對照五篇論文

## 比較什麼

[Survey](../papers/wang2023-agent-survey.md) 把 agent 拆成 Profile、Memory、Planning、Action 四個模組 [@wang2023-agent-survey, §2.1]。這頁把 wiki 裡另外五篇論文放進去，看每篇主要補強哪一塊。

| 論文（arXiv） | 主要貢獻在哪個模組 | 做法 | 出處 |
|---|---|---|---|
| [CoT](../papers/wei2022-chain-of-thought.md)（2201.11903） | Planning（沒有回饋，single-path） | 範例裡寫出推理步驟 | [@wang2023-agent-survey, §2.1.3]、[@wei2022-chain-of-thought, §1] |
| [ReAct](../papers/yao2022-react.md)（2210.03629） | Planning（環境回饋）＋ Action | Thought → Action → Observation 迴圈 | [@wang2023-agent-survey, §2.1.3]、[@yao2022-react, §2] |
| [Toolformer](../papers/schick2023-toolformer.md)（2302.04761） | Action（外部工具） | self-supervised 學會何時呼叫 API | [@wang2023-agent-survey, §2.1.4]、[@schick2023-toolformer, §2] |
| [Reflexion](../papers/shinn2023-reflexion.md)（2303.11366） | Planning（模型回饋）＋ Memory（hybrid） | 失敗後寫文字反省，存進長期記憶 | [@wang2023-agent-survey, §2.1.2]、[@shinn2023-reflexion, §3] |
| [Generative Agents](../papers/park2023-generative-agents.md)（2304.03442） | Profile（手寫角色）＋ Memory（hybrid、反思）＋ Planning | 記憶流、反思、日程計畫 | [@wang2023-agent-survey, §2.1.1]、[@park2023-generative-agents, §4] |

**依時間順序看**（arXiv 編號的前四碼是年月）：CoT（2201）→ ReAct（2210）→ Toolformer（2302）→ Reflexion（2303）→ Generative Agents（2304）→ Survey（2308）[@wei2022-chain-of-thought, p.1]、[@yao2022-react, p.1]、[@schick2023-toolformer, p.1]、[@shinn2023-reflexion, p.1]、[@park2023-generative-agents, p.1]、[@wang2023-agent-survey, p.1]。Survey 的 Fig. 1 也把 CoT、Toolformer、Generative Agent 標在 2022–2023 年的成長曲線上 [@wang2023-agent-survey, Fig. 1]。

## 觀察

- 五篇正好各補一塊：先學會「想」（CoT），再「邊想邊做」（ReAct），再「用工具」（Toolformer），再「從失敗學習」（Reflexion），最後「長期記憶與生活」（Generative Agents）。
- 後面的論文直接把前面的當零件：Reflexion 的 Actor 用 CoT 和 ReAct [@shinn2023-reflexion, §3]；ReAct 拿 CoT 當 baseline 並結合使用 [@yao2022-react, §3.2]。
- 共同的挑戰：幻覺 [@wang2023-agent-survey, §6.4]、每個動作要多次呼叫 LLM 的效率問題 [@wang2023-agent-survey, §6.6]。

> 💭 筆記：「想 → 做 → 用工具 → 反省 → 記憶」這條線是我自己排的教學順序，不是 Survey 的說法；簡報如果用這條故事線，要說明這是整理方式，不是論文結論。
