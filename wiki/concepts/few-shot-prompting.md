---
type: concept
title: Few-shot prompting（in-context learning）
sources: [wei2022-chain-of-thought, yao2022-react, schick2023-toolformer]
related: [concepts/chain-of-thought.md, concepts/reasoning-and-acting.md]
updated: 2026-11-17
---

# Few-shot prompting

## 定義

不 finetune 模型，只在 prompt 裡放幾個「輸入–輸出」範例示範任務，模型就能照著做；Wei et al. 稱之為由 Brown et al.（2020）推廣的 standard few-shot prompting [@wei2022-chain-of-thought, §3.1]。

## 各論文怎麼做

- **[CoT](../papers/wei2022-chain-of-thought.md)**：在範例的輸入和輸出之間加入推理過程。作者指出傳統 few-shot prompting 在推理任務上表現差，而且模型變大也不太會進步 [@wei2022-chain-of-thought, §1]。
- **[ReAct](../papers/yao2022-react.md)**：範例是人寫的「想法＋行動＋觀察」完整軌跡。HotpotQA 用 6 個、FEVER 用 3 個範例，作者發現範例再多也不會更好 [@yao2022-react, §3.2]。

- **對照：[Toolformer](../papers/schick2023-toolformer.md)** 測試時刻意用 zero-shot（不給任何範例），想看使用者沒事先說明怎麼用工具時，模型能不能自己決定 [@schick2023-toolformer, §4.2]；但產生訓練資料時，每個 API 仍需要幾個示範 [@schick2023-toolformer, Abstract]。

## 優點與限制

- **優點**：不需要大量訓練資料，一個模型就能做很多任務 [@wei2022-chain-of-thought, §1]。
- **限制**：對範例敏感——換範例順序，GPT-3 在 SST-2 的準確率可以從 54.3% 到 93.4%（Wei et al. 引用 Zhao et al. 2021）[@wei2022-chain-of-thought, §3.4]。
- **限制**：複雜任務需要更多範例，容易超過輸入長度上限 [@yao2022-react, §6]。

## 相關頁面

- [Chain-of-Thought](chain-of-thought.md)
- [Reasoning and Acting](reasoning-and-acting.md)
