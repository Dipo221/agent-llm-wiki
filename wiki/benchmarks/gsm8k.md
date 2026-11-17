---
type: benchmark
title: GSM8K（小學數學應用題）
sources: [wei2022-chain-of-thought]
related: [papers/wei2022-chain-of-thought.md, concepts/chain-of-thought.md]
updated: 2026-11-17
---

# GSM8K

## 在測什麼

多步驟的數學應用題（math word problems），測模型的算術推理能力；出自 Cobbe et al.（2021）[@wei2022-chain-of-thought, §3.1]。在 CoT 論文的五個算術資料集中，它是 baseline 最低（最難）的 [@wei2022-chain-of-thought, §3.2]。

## 任務形式

輸入一題文字應用題，輸出數字答案，以 solve rate（答對率 %）計分 [@wei2022-chain-of-thought, Table 2]。

## 用過它的論文與成績

| 論文 | 設定 | 成績（solve rate %） | 出處 |
|---|---|---|---|
| [CoT](../papers/wei2022-chain-of-thought.md) | PaLM 540B，standard prompting | 17.9 | [@wei2022-chain-of-thought, Table 2] |
| [CoT](../papers/wei2022-chain-of-thought.md) | PaLM 540B，CoT prompting（8 個範例） | 56.9 | [@wei2022-chain-of-thought, Table 2] |
| [CoT](../papers/wei2022-chain-of-thought.md) | Codex，CoT prompting | 63.1 | [@wei2022-chain-of-thought, Table 2] |
