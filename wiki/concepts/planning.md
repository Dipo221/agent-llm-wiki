---
type: concept
title: Planning（規劃）
sources: [wang2023-agent-survey, wei2022-chain-of-thought, yao2022-react, shinn2023-reflexion, park2023-generative-agents]
related: [papers/wang2023-agent-survey.md, concepts/chain-of-thought.md, concepts/reasoning-and-acting.md, concepts/self-reflection.md]
updated: 2026-11-17
---

# Planning（規劃）

## 定義

把複雜任務拆成較簡單的子任務、逐一解決，就像人類面對複雜任務的做法 [@wang2023-agent-survey, §2.1.3]。Survey 依「規劃過程中有沒有收到回饋」分成兩大類 [@wang2023-agent-survey, §2.1.3]。

## 各論文怎麼做

| 類別 | 代表做法 | 說明 | 出處 |
|---|---|---|---|
| 沒有回饋：single-path | [CoT](../papers/wei2022-chain-of-thought.md) | 推理步驟一步接一步，只有一條路 | [@wang2023-agent-survey, §2.1.3] |
| 沒有回饋：multi-path | CoT-SC | 產生多條推理路徑，取出現最多次的答案 | [@wang2023-agent-survey, §2.1.3] |
| 有回饋：環境回饋 | [ReAct](../papers/yao2022-react.md) | 下一個 thought 受到上一個 observation 影響，計畫更能適應環境 | [@wang2023-agent-survey, §2.1.3] |
| 有回饋：模型回饋 | [Reflexion](../papers/shinn2023-reflexion.md) | evaluator 讀軌跡產生文字回饋，而不只是分數 | [@wang2023-agent-survey, §2.1.3] |
| 長時間的日程計畫 | [Generative Agents](../papers/park2023-generative-agents.md) | 先排一天的粗略計畫，再遞迴拆成細節，計畫存回記憶 | [@park2023-generative-agents, §4.3] |

## 優點與限制

- 沒有回饋的規劃，很難一開始就產生完美計畫，因為要考慮很多複雜的前提條件 [@wang2023-agent-survey, §2.1.3]。
- 沒有計畫時，Generative Agents 的角色會一小時內吃三次午餐：當下合理，長期不合理 [@park2023-generative-agents, §4.3]。
- 有環境回饋也有代價：ReAct 會重複之前的想法和動作，跳不出迴圈 [@yao2022-react, §3.3]；Reflexion 只用 ReAct 時，第 6–7 次嘗試後就不再進步 [@shinn2023-reflexion, §4.1]。

## 相關頁面

- [Chain-of-Thought](chain-of-thought.md)、[Reasoning and Acting](reasoning-and-acting.md)、[Self-reflection](self-reflection.md)
- [Agent 架構對照](../comparisons/agent-framework-map.md)
