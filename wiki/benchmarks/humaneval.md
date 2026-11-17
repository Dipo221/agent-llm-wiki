---
type: benchmark
title: HumanEval（程式生成）
sources: [shinn2023-reflexion]
related: [papers/shinn2023-reflexion.md, concepts/self-reflection.md]
updated: 2026-11-17
---

# HumanEval

## 在測什麼

給自然語言的函式說明，讓模型寫出函式本體，衡量程式生成的正確率；MBPP 也是同類型的 benchmark [@shinn2023-reflexion, §4.3]。Reflexion 也用 MultiPL-E 把題目翻成 Rust [@shinn2023-reflexion, §4.3]。

## 任務形式

以 pass@1 計分：只交一次答案，通過隱藏測試就算對。Reflexion 不看隱藏測試，而是用自己產生的 unit test（最多 6 個）判斷要不要重試，所以仍符合 pass@1 的規則 [@shinn2023-reflexion, §4.3]。

## 用過它的論文與成績

| 論文 | 方法 | pass@1 | 出處 |
|---|---|---|---|
| [Reflexion](../papers/shinn2023-reflexion.md) | CodeT + GPT-3.5（先前最佳） | 65.8 | [@shinn2023-reflexion, Table 1] |
| [Reflexion](../papers/shinn2023-reflexion.md) | GPT-4 | 80.1 | [@shinn2023-reflexion, Table 1] |
| [Reflexion](../papers/shinn2023-reflexion.md) | Reflexion（Table 1 沒有明寫底層模型） | 91.0 | [@shinn2023-reflexion, Table 1] |

GPT-4 baseline 在同一篇論文有 80%／80.1／82% 三種寫法，見 [Reflexion 論文頁](../papers/shinn2023-reflexion.md) 的 ⚠ 區塊 [@shinn2023-reflexion, Abstract／Table 1／§4.3]。
