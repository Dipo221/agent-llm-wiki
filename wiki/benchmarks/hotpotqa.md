---
type: benchmark
title: HotpotQA（多跳問答）
sources: [yao2022-react, shinn2023-reflexion]
related: [papers/yao2022-react.md, benchmarks/fever.md]
updated: 2026-11-17
---

# HotpotQA

## 在測什麼

多跳（multi-hop）問答：答案需要跨兩篇以上 Wikipedia 段落推理 [@yao2022-react, §3.1]。

## 任務形式

ReAct 用 question-only 設定：模型只拿到問題、拿不到支援段落，必須靠內部知識或透過 Wikipedia API（search／lookup／finish）自己查 [@yao2022-react, §3.1]。以 EM（exact match）計分 [@yao2022-react, Table 1]。作者也發現部分題目的標準答案已經過時 [@yao2022-react, §3.3]。

## 用過它的論文與成績

| 論文 | 方法（PaLM-540B） | EM | 出處 |
|---|---|---|---|
| [ReAct](../papers/yao2022-react.md) | CoT | 29.4 | [@yao2022-react, Table 1] |
| [ReAct](../papers/yao2022-react.md) | ReAct | 27.4 | [@yao2022-react, Table 1] |
| [ReAct](../papers/yao2022-react.md) | ReAct → CoT-SC | 35.1 | [@yao2022-react, Table 1] |
| [ReAct](../papers/yao2022-react.md) | Supervised SoTA | 67.5 | [@yao2022-react, Table 1] |

[Reflexion](../papers/shinn2023-reflexion.md) 只用 100 題、以多次嘗試後的正確率計算：ReAct + gpt-4 從 0.39 進步到 0.51 [@shinn2023-reflexion, Table 5]。題數、模型、計分方式都和 ReAct 論文不同，不能和上表直接比較。
