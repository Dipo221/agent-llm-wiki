---
type: benchmark
title: FEVER（事實查核）
sources: [yao2022-react]
related: [papers/yao2022-react.md, benchmarks/hotpotqa.md]
updated: 2026-11-17
---

# FEVER

## 在測什麼

事實查核（fact verification）：判斷一句陳述是 SUPPORTS、REFUTES 還是 NOT ENOUGH INFO，依據是否有 Wikipedia 段落能驗證 [@yao2022-react, §3.1]。

## 任務形式

和 HotpotQA 一樣用 question-only 設定，以準確率（Acc）計分 [@yao2022-react, Table 1]。SUPPORTS 和 REFUTES 的陳述可能只差一點點，所以去查準確、最新的知識特別重要 [@yao2022-react, §3.3]。

## 用過它的論文與成績

| 論文 | 方法（PaLM-540B） | Acc | 出處 |
|---|---|---|---|
| [ReAct](../papers/yao2022-react.md) | CoT | 56.3 | [@yao2022-react, Table 1] |
| [ReAct](../papers/yao2022-react.md) | ReAct | 60.9 | [@yao2022-react, Table 1] |
| [ReAct](../papers/yao2022-react.md) | CoT-SC → ReAct | 64.6 | [@yao2022-react, Table 1] |
| [ReAct](../papers/yao2022-react.md) | Supervised SoTA | 89.5 | [@yao2022-react, Table 1] |
