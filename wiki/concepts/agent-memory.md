---
type: concept
title: Agent memory（agent 的記憶）
sources: [park2023-generative-agents, shinn2023-reflexion, yao2022-react]
related: [papers/park2023-generative-agents.md, papers/shinn2023-reflexion.md, concepts/self-reflection.md]
updated: 2026-11-17
---

# Agent memory（agent 的記憶）

## 定義

讓 agent 在 context window 之外保存經歷，需要時再取回來影響行為。Reflexion 把記憶分成短期（這次的軌跡）和長期（累積的反省）[@shinn2023-reflexion, §3]；Generative Agents 用「記憶流」完整記錄所有經歷，再依情境檢索 [@park2023-generative-agents, §4.1]。

## 各論文怎麼做

| 面向 | [ReAct](../papers/yao2022-react.md) | [Reflexion](../papers/shinn2023-reflexion.md) | [Generative Agents](../papers/park2023-generative-agents.md) | 出處 |
|---|---|---|---|---|
| 存什麼 | 只有本次的想法／行動／觀察軌跡 | 短期：軌跡；長期：自我反省文字 | 觀察、反思、計畫都存進記憶流 | [@yao2022-react, §2]、[@shinn2023-reflexion, §3]、[@park2023-generative-agents, §4] |
| 存多少 | 受 context 長度限制 | 長期記憶最多 Ω 筆（通常 1–3） | 全部保存，靠檢索挑選 | [@yao2022-react, §6]、[@shinn2023-reflexion, §3]、[@park2023-generative-agents, §4.1] |
| 怎麼取用 | 整段放進 prompt | 整段放進 prompt | recency＋importance＋relevance 加權排序 | [@park2023-generative-agents, §4.1] |

## 優點與限制

**優點**
- 移除記憶會明顯變差：Generative Agents 拿掉記憶、反思、計畫後，TrueSkill μ 從 29.89 掉到 21.21 [@park2023-generative-agents, §6.5.1]。
- 只給「上一次的軌跡」不夠，加上反省文字才有額外 8% 進步 [@shinn2023-reflexion, §4.2]。

**限制**
- 記憶越多越難檢索對的內容 [@park2023-generative-agents, §7.2]。
- 可能被 memory hacking 植入沒發生過的事件 [@park2023-generative-agents, §8.2]。
- Reflexion 的記憶只是有上限的滑動視窗，作者建議改用向量資料庫或 SQL 資料庫 [@shinn2023-reflexion, §5]。

## 相關頁面

- [Self-reflection](self-reflection.md)
