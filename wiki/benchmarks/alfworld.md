---
type: benchmark
title: ALFWorld（文字版居家任務遊戲）
sources: [yao2022-react]
related: [papers/yao2022-react.md, concepts/reasoning-and-acting.md, benchmarks/webshop.md]
updated: 2026-11-17
---

# ALFWorld

## 在測什麼

合成的文字遊戲，對應具身（embodied）的 ALFRED benchmark：agent 要在模擬的房子裡用文字指令（go to、take、use）完成高層目標，例如「在檯燈下檢查紙張」[@yao2022-react, §4]。

## 任務形式

- 6 種任務類型；一個任務可能有超過 50 個地點，專家也要超過 50 步才能完成 [@yao2022-react, §4]。
- 需要規劃與追蹤子目標、有系統地探索，也要用常識判斷物品可能在哪（檯燈多半在書桌上）[@yao2022-react, §4]。
- ReAct 在 134 個沒看過的遊戲上評估成功率 [@yao2022-react, §4]。

## 用過它的論文與成績

| 論文 | 方法 | 整體成功率（%） | 出處 |
|---|---|---|---|
| [ReAct](../papers/yao2022-react.md) | BUTLER（模仿學習，best of 8） | 37 | [@yao2022-react, Table 3] |
| [ReAct](../papers/yao2022-react.md) | Act（best of 6） | 45 | [@yao2022-react, Table 3] |
| [ReAct](../papers/yao2022-react.md) | ReAct-IM（best of 6） | 53 | [@yao2022-react, Table 3] |
| [ReAct](../papers/yao2022-react.md) | ReAct（best of 6） | 71 | [@yao2022-react, Table 3] |
