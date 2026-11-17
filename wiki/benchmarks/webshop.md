---
type: benchmark
title: WebShop（網路購物環境）
sources: [yao2022-react]
related: [papers/yao2022-react.md, benchmarks/alfworld.md]
updated: 2026-11-17
---

# WebShop

## 在測什麼

模擬線上購物網站，有 1.18M 個真實商品、12k 條人類指令；agent 要依照使用者的需求（例如「有抽屜、鎳色、低於 140 美元的床頭櫃」）透過搜尋和點選買到對的商品 [@yao2022-react, §4]。

## 任務形式

用 500 條測試指令評估兩個指標：Score（選到的商品符合多少需求屬性的平均百分比）和 SR（success rate，完全符合所有需求的比例）[@yao2022-react, §4]。

## 用過它的論文與成績

| 論文 | 方法 | Score | SR | 出處 |
|---|---|---|---|---|
| [ReAct](../papers/yao2022-react.md) | IL（模仿學習） | 59.9 | 29.1 | [@yao2022-react, Table 4] |
| [ReAct](../papers/yao2022-react.md) | IL+RL | 62.4 | 28.7 | [@yao2022-react, Table 4] |
| [ReAct](../papers/yao2022-react.md) | Act | 62.3 | 30.1 | [@yao2022-react, Table 4] |
| [ReAct](../papers/yao2022-react.md) | ReAct | 66.6 | 40.0 | [@yao2022-react, Table 4] |
| [ReAct](../papers/yao2022-react.md) | 人類專家 | 82.1 | 59.6 | [@yao2022-react, Table 4] |
