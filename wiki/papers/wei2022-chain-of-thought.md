---
type: paper
title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
sources: [wei2022-chain-of-thought]
related: [concepts/chain-of-thought.md, concepts/few-shot-prompting.md, papers/yao2022-react.md, comparisons/cot-vs-react.md, benchmarks/gsm8k.md]
arxiv: 2201.11903
authors: Jason Wei et al.（Google Research, Brain Team）
venue: NeurIPS 2022
updated: 2026-11-17
---

# Chain-of-Thought Prompting（Wei et al., 2022）

## 一句話

在 few-shot prompt 的每個範例裡，加上「一步一步推理的中間過程」（chain of thought），大型語言模型就會跟著先推理再回答，數學、常識、符號推理的表現都明顯提升 [@wei2022-chain-of-thought, §1]。

## 要解決的問題

- 光把模型變大，在算術、常識、符號推理這類需要多步驟的任務上仍然不夠 [@wei2022-chain-of-thought, §1]。
- 兩條舊路各有缺點：用「推理過程（rationale）」來訓練或 finetune 模型，需要大量高品質的推理標註，成本高；傳統 few-shot prompting（只給 input–output 範例）在推理任務上表現差，而且模型變大也不太會進步 [@wei2022-chain-of-thought, §1]。
- 這篇把兩者結合：不 finetune，只在 prompt 範例裡放推理過程 [@wei2022-chain-of-thought, §1]。

## 方法

- 每個 few-shot 範例由三部分組成：`⟨input, chain of thought, output⟩`。chain of thought 是「一連串導向最終答案的自然語言中間推理步驟」[@wei2022-chain-of-thought, §1]。
- 範例（Figure 1）：
  ```
  Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
     Each can has 3 tennis balls. How many tennis balls does he have now?
  A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls.
     5 + 6 = 11. The answer is 11.
  ```
- 數學題用作者手寫的 8 個範例（AQuA 例外，用 4 個）；範例**沒有經過 prompt engineering** [@wei2022-chain-of-thought, §3.1]。
- 作者列出 chain of thought 的四個優點 [@wei2022-chain-of-thought, §2]：
  1. 把多步驟問題拆成中間步驟，需要多推理的題目就多分配一些計算。
  2. 提供「看進模型行為的窗口」，可以除錯推理在哪裡走偏。
  3. 原則上適用於任何人類能用語言解決的任務。
  4. 只要在 few-shot 範例裡放 chain of thought，就能從夠大的現成模型引出這種推理。

## 實驗與結果

**測試範圍**：算術（GSM8K、SVAMP、ASDiv、AQuA、MAWPS）、常識（CSQA、StrategyQA、Date、Sports、SayCan）、符號（Last letter concatenation、Coin flip）[@wei2022-chain-of-thought, §3.1]。模型有 GPT-3、LaMDA、PaLM、UL2 20B、Codex，用 greedy decoding [@wei2022-chain-of-thought, §3.1]。

**三個主要發現** [@wei2022-chain-of-thought, §3.2]：
1. **規模湧現（emergent ability）**：模型小的時候 CoT 沒有幫助，到約 100B 參數才開始有效；小模型會寫出「流暢但不合邏輯」的推理，反而比 standard prompting 差 [@wei2022-chain-of-thought, §3.2]。
2. **題目越難，效益越大**：GSM8K（baseline 最低的資料集）上，最大的 GPT 和 PaLM 表現提升超過一倍；只需一步的 SingleOp 幾乎沒進步甚至變差 [@wei2022-chain-of-thought, §3.2]。
3. **能和 finetune 的方法比**：PaLM 540B ＋ CoT 在 GSM8K、SVAMP、MAWPS 達到新的 state of the art [@wei2022-chain-of-thought, §3.2]。

**GSM8K 關鍵數字**（solve rate %，standard → CoT）：

| 模型 | Standard | CoT | 出處 |
|---|---|---|---|
| PaLM 540B | 17.9 | 56.9 | [@wei2022-chain-of-thought, Table 2] |
| GPT-3 175B（text-davinci-002） | 15.6 | 46.9 | [@wei2022-chain-of-thought, Table 2] |
| LaMDA 137B | 6.5 | 14.3 | [@wei2022-chain-of-thought, Table 2] |
| PaLM 8B（小模型：CoT 反而較差） | 4.9 | 4.1 | [@wei2022-chain-of-thought, Table 2] |

**錯誤分析**：LaMDA 137B 在 GSM8K 答錯的 50 題中，46% 的推理「幾乎正確」（計算錯、少一步），54% 有語意理解或連貫性的大錯 [@wei2022-chain-of-thought, §3.2]。

**Ablation**（證明「有效的是自然語言推理本身」）[@wei2022-chain-of-thought, §3.3]：
- *Equation only*（只輸出算式）：對 GSM8K 幫助不大，題意太複雜，沒辦法直接翻成算式。
- *Variable compute only*（輸出一串點點 `...` 佔位，給模型多一點計算）：和 baseline 差不多 → 單純多算幾個 token 不是原因。
- *Chain of thought after answer*（先答再解釋）：和 baseline 差不多 → 推理必須在答案**之前**。

**穩健性**：換不同人寫的範例、換風格精簡的範例、從 GSM8K 訓練集隨機抽範例，都大幅贏過 standard prompting [@wei2022-chain-of-thought, §3.4]。

**常識推理**：PaLM 540B ＋ CoT 在 StrategyQA 超越先前最佳（75.6% vs 69.4%），在 Sports Understanding 贏過沒有輔助的運動迷（95.4% vs 84%）；CSQA 的進步很小 [@wei2022-chain-of-thought, §4]。

**符號推理**：CoT 能做到 length generalization——範例只有 2 個字的名字，測試時對更長的輸入（OOD）也能有往上的 scaling 曲線；standard prompting 在 OOD 兩個任務都失敗 [@wei2022-chain-of-thought, §5]。

## 限制

作者自己列出的四點 [@wei2022-chain-of-thought, §6]：
1. 模仿人類的思考過程，不代表神經網路真的在「推理」，這是開放問題。
2. few-shot 的標註成本很小，但若要拿來 finetune，標註成本可能過高。
3. **不保證推理路徑正確**，可能推出對的答案，也可能推出錯的答案。
4. 只在大模型上湧現，實際服務成本高。

## 和其他論文的關係

- [ReAct](yao2022-react.md) 把 CoT 當作「只推理、不行動」的 baseline，指出 CoT 是「靜態黑盒子」，不接觸外部世界，容易出現 fact hallucination 與錯誤累積 [@yao2022-react, §1]。比較見 [CoT vs ReAct](../comparisons/cot-vs-react.md)。
- 概念整理見 [Chain-of-Thought](../concepts/chain-of-thought.md)、[Few-shot prompting](../concepts/few-shot-prompting.md)；資料集見 [GSM8K](../benchmarks/gsm8k.md)。

> 💭 筆記：這篇的範例全部是「人手寫的推理過程」。之後 ReAct 也沿用「人手寫軌跡當範例」的作法，只是把行動和觀察也寫進去。
