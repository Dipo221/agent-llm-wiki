---
type: benchmark
title: 數學應用題（ASDiv、SVAMP、MAWPS）
sources: [wei2022-chain-of-thought, schick2023-toolformer]
related: [benchmarks/gsm8k.md, papers/wei2022-chain-of-thought.md, papers/schick2023-toolformer.md]
updated: 2026-11-17
---

# 數學應用題：ASDiv、SVAMP、MAWPS

## 在測什麼

文字敘述的數學應用題：SVAMP 的題目結構有變化，ASDiv 題型多樣，MAWPS 是一組應用題 benchmark [@wei2022-chain-of-thought, §3.1]。難度較高的 GSM8K 另見 [GSM8K](gsm8k.md)。

## 任務形式

輸入應用題，輸出數字答案。兩篇論文的評分方式不同：CoT 論文用 few-shot prompting 算 solve rate [@wei2022-chain-of-thought, §3.1]；Toolformer 用 zero-shot，只看模型輸出的第一個數字，評分較寬鬆 [@schick2023-toolformer, §4.2]。

## 用過它的論文與成績

| 論文 | 模型與設定 | ASDiv | SVAMP | MAWPS | 出處 |
|---|---|---|---|---|---|
| [CoT](../papers/wei2022-chain-of-thought.md) | PaLM 540B，CoT（few-shot） | 73.9 | 79.0 | 93.3 | [@wei2022-chain-of-thought, Table 2] |
| [CoT](../papers/wei2022-chain-of-thought.md) | GPT-3 175B（text-davinci-002），standard（few-shot） | 70.3 | 65.7 | 72.7 | [@wei2022-chain-of-thought, Table 2] |
| [Toolformer](../papers/schick2023-toolformer.md) | GPT-3 175B（davinci），zero-shot | 14.0 | 10.0 | 19.8 | [@schick2023-toolformer, Table 4] |
| [Toolformer](../papers/schick2023-toolformer.md) | Toolformer（GPT-J 6.7B＋計算機），zero-shot | 40.4 | 29.4 | 44.0 | [@schick2023-toolformer, Table 4] |

> ⚠ 說法不一致：同樣叫「GPT-3 175B」，在 SVAMP 上 CoT 論文報告 standard prompting 65.7 [@wei2022-chain-of-thought, Table 2]，Toolformer 論文報告 10.0 [@schick2023-toolformer, Table 4]。可能原因：(1) 模型版本不同——CoT 論文用 text-davinci-002（推測對應 InstructGPT）[@wei2022-chain-of-thought, §3.1]，Toolformer 用沒有 instruction finetune 的原始 davinci [@schick2023-toolformer, §4.1]；(2) CoT 論文是 few-shot，Toolformer 是 zero-shot [@schick2023-toolformer, §4.2]。因此兩篇的數字不能直接比較，也不能說「Toolformer 6.7B 比 PaLM 540B＋CoT 強或弱」。
