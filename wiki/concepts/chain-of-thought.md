---
type: concept
title: Chain-of-Thought（思維鏈推理）
sources: [wei2022-chain-of-thought, yao2022-react]
related: [papers/wei2022-chain-of-thought.md, papers/yao2022-react.md, concepts/few-shot-prompting.md, comparisons/cot-vs-react.md]
updated: 2026-11-17
---

# Chain-of-Thought（CoT）

## 定義

Chain of thought 是「一連串導向最終答案的自然語言中間推理步驟」；chain-of-thought prompting 是在 few-shot 範例裡附上這種推理過程，讓模型跟著先推理再回答 [@wei2022-chain-of-thought, §1]。

## 各論文怎麼做

- **[Wei et al. 2022](../papers/wei2022-chain-of-thought.md)**：提出 CoT prompting。範例格式 `⟨input, chain of thought, output⟩`，數學題用 8 個手寫範例 [@wei2022-chain-of-thought, §3.1]。
- **[Yao et al. 2022（ReAct）](../papers/yao2022-react.md)**：把 CoT 當「只推理」的 baseline；另用 CoT-SC（取 21 條 CoT、temperature 0.7、多數決）當更強的 baseline，並設計 ReAct ↔ CoT-SC 的切換規則 [@yao2022-react, §3.2]。

## 優點與限制

**優點**
- 把多步驟問題拆開，難題可以多花計算；可解釋、可除錯；只靠 prompting，不用 finetune [@wei2022-chain-of-thought, §2]。
- 題目越難效益越大，GSM8K 上最大的 GPT 和 PaLM 表現提升超過一倍 [@wei2022-chain-of-thought, §3.2]。

**限制**
- 規模湧現：約 100B 參數以上才有效，小模型會寫出流暢但不合邏輯的推理 [@wei2022-chain-of-thought, §3.2]。
- 不保證推理路徑正確 [@wei2022-chain-of-thought, §6]。
- 只用內部知識，不接觸外部世界 → 容易幻覺；在 HotpotQA 的失敗案例中，幻覺佔 56% [@yao2022-react, Table 2]。

## 相關頁面

- [Few-shot prompting](few-shot-prompting.md)
- [Reasoning and Acting](reasoning-and-acting.md)
- [CoT vs ReAct](../comparisons/cot-vs-react.md)
- [GSM8K](../benchmarks/gsm8k.md)
