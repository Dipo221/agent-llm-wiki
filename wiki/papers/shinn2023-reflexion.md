---
type: paper
title: "Reflexion: Language Agents with Verbal Reinforcement Learning"
sources: [shinn2023-reflexion]
related: [concepts/self-reflection.md, papers/yao2022-react.md, papers/wei2022-chain-of-thought.md, benchmarks/alfworld.md, benchmarks/hotpotqa.md, benchmarks/humaneval.md]
arxiv: 2303.11366
authors: Noah Shinn et al.（Northeastern University、MIT、Princeton University）
venue: NeurIPS 2023
updated: 2026-11-17
---

# Reflexion（Shinn et al., 2023）

## 一句話

Agent 失敗後**用文字反省**「哪裡做錯、下次怎麼做」，把反省存進記憶，下一次嘗試時帶著這些經驗重來；不更新模型權重，而是用語言回饋來「強化」agent [@shinn2023-reflexion, Abstract]。

## 要解決的問題

- LLM agent 很難從試誤中快速學習：傳統強化學習需要大量訓練樣本和昂貴的 finetune [@shinn2023-reflexion, Abstract]。
- 大模型參數太多，過去只能靠 in-context 範例教 agent [@shinn2023-reflexion, §1]。
- 純數字的獎勵（成功／失敗）很難做 credit assignment：不知道是長軌跡中的哪一步錯了 [@shinn2023-reflexion, §1]。

## 方法

**三個模組** [@shinn2023-reflexion, §3]：
- **Actor**：產生文字與行動的 LLM，可以是 [CoT](wei2022-chain-of-thought.md) 或 [ReAct](yao2022-react.md)。
- **Evaluator**：替 Actor 的軌跡打分數。推理任務用 exact match；決策任務用預先寫好的 heuristic，或讓另一個 LLM 判斷；程式任務用自己產生的 unit test。
- **Self-Reflection**：LLM 讀「軌跡＋分數＋過去記憶」，寫出具體的文字反省，存進記憶。

**兩種記憶** [@shinn2023-reflexion, §3]：短期記憶＝這次的軌跡；長期記憶＝累積的反省文字。為了不超過 context 長度，長期記憶只保留最多 Ω 筆（通常 1–3 筆）。

**流程（Algorithm 1）**：嘗試 → 評分 → 反省 → 把反省加進記憶 → 再嘗試，直到 Evaluator 判定通過或達到最大嘗試次數 [@shinn2023-reflexion, §3]。

**和傳統強化學習比的優點**：不需要 finetune、回饋更細緻（可以指出要改哪個動作）、記憶是看得懂的文字、對下一次的行動給出明確提示 [@shinn2023-reflexion, §1]。

## 實驗與結果

| 任務 | 設定 | 結果 | 出處 |
|---|---|---|---|
| ALFWorld（134 個環境） | ReAct + Reflexion（heuristic 評估） | 完成 130 個 | [@shinn2023-reflexion, §4.1] |
| HotpotQA（100 題） | ReAct + gpt-4 | 0.39 → 0.51 | [@shinn2023-reflexion, Table 5] |
| HotpotQA（100 題） | CoT (GT) + gpt-4 | 0.68 → 0.80 | [@shinn2023-reflexion, Table 5] |
| HumanEval Python | Reflexion pass@1 | 91.0（GPT-4 為 80.1） | [@shinn2023-reflexion, Table 1] |
| Leetcode Hard Python | Reflexion pass@1 | 15.0（GPT-4 為 7.5） | [@shinn2023-reflexion, Table 1] |
| MBPP Python | Reflexion pass@1 | 77.1（GPT-4 為 80.1，**唯一輸的**） | [@shinn2023-reflexion, Table 1] |

- **整體提升**：比強 baseline 在 ALFWorld 多 22%、HotpotQA 多 20%、HumanEval 多 11% [@shinn2023-reflexion, §4]。
- **ALFWorld**：heuristic 很簡單——同一個動作得到同樣回應超過 3 次，或動作數超過 30 次，就觸發反省 [@shinn2023-reflexion, §4.1]。只用 ReAct 的 agent 在第 6–7 次嘗試後就不再進步，幻覺率停在 22% [@shinn2023-reflexion, §4.1]。
- **常見錯誤**：agent 以為自己拿到某個物品，其實沒有，接著在長軌跡中一錯到底；反省能把長軌跡濃縮成「下次的提示」[@shinn2023-reflexion, §4.1]。
- **HotpotQA**：baseline（ReAct-only、CoT-only）在後續嘗試中完全沒有解出第一次失敗的題目；Reflexion 會持續重試，直到同一題連續失敗 3 次 [@shinn2023-reflexion, §4.2]。
- **Ablation（HotpotQA）**：只給「上一次的軌跡」（episodic memory）不夠，加上自我反省再多 8% [@shinn2023-reflexion, §4.2]。
- **Ablation（HumanEval Rust 最難 50 題）**：拿掉 test generation 只剩 52%（比 baseline 的 60% 還差）；拿掉自我反省則沒有進步（60%）；兩者都有才到 0.68 [@shinn2023-reflexion, Table 3]。

> ⚠ 說法不一致：同一篇論文對 GPT-4 在 HumanEval Python 的 baseline 有三種寫法——摘要寫 80% [@shinn2023-reflexion, Abstract]，Table 1 寫 80.1 [@shinn2023-reflexion, Table 1]，§4.3 分析段落寫 82% [@shinn2023-reflexion, §4.3]。可能原因：80% 是 80.1 的四捨五入；82% 可能來自另一次執行或不同設定，論文沒有說明。引用時以 Table 1 為準並註明來源。

## 限制

- 本質上是用自然語言做 policy optimization，仍可能卡在非最佳的局部解 [@shinn2023-reflexion, §5]。
- 長期記憶只是有上限的滑動視窗，作者建議未來用向量資料庫或 SQL 資料庫 [@shinn2023-reflexion, §5]。
- 程式任務依賴自己寫的測試：測試太弱會讓錯的程式全部通過（false positive）。MBPP Python 的 false positive 率是 16.3%，HumanEval Python 只有 1.4% [@shinn2023-reflexion, §4.3]。
- 自我修正是「較強、較大模型」才有的湧現能力：小模型 starchat-beta 用 Reflexion 沒有進步（0.26 → 0.26）[@shinn2023-reflexion, Table 4]。
- 產生的程式在執行前沒有驗證，建議在隔離環境中執行 [@shinn2023-reflexion, §8]。

## 和其他論文的關係

- Actor 直接用 [ReAct](yao2022-react.md)（決策、問答）和 [CoT](wei2022-chain-of-thought.md)（推理），ALFWorld 沿用 ReAct 的 few-shot 範例 [@shinn2023-reflexion, §4.1]。
- 概念見 [Self-reflection](../concepts/self-reflection.md)。
- Benchmark：[ALFWorld](../benchmarks/alfworld.md)、[HotpotQA](../benchmarks/hotpotqa.md)、[HumanEval](../benchmarks/humaneval.md)。

> 💭 筆記：Reflexion 的「嘗試 → 評分 → 反省 → 重試、最多 N 次」就是第十講講的 loop（有審查、有停止條件）。
