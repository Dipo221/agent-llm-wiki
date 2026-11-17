---
type: paper
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
sources: [yao2022-react]
related: [concepts/reasoning-and-acting.md, concepts/tool-use.md, papers/schick2023-toolformer.md, concepts/chain-of-thought.md, concepts/few-shot-prompting.md, comparisons/cot-vs-react.md, benchmarks/hotpotqa.md, benchmarks/fever.md, benchmarks/alfworld.md, benchmarks/webshop.md]
arxiv: 2210.03629
authors: Shunyu Yao et al.（Princeton University、Google Research）
venue: ICLR 2023
updated: 2026-11-17
---

# ReAct（Yao et al., 2022）

## 一句話

讓 LLM **交錯產生「想法（Thought）」和「行動（Action）」**：想法幫助擬定與調整計畫，行動去外部（Wikipedia API、文字遊戲、購物網站）取得資訊，觀察結果再回饋給下一步推理 [@yao2022-react, Abstract]。

## 要解決的問題

- 過去「推理」（如 [chain-of-thought](wei2022-chain-of-thought.md)）和「行動」（如行動計畫生成）是分開研究的 [@yao2022-react, Abstract]。
- CoT 是「靜態黑盒子」：只用模型內部知識推理，沒有接觸外部世界，所以會有 fact hallucination 和錯誤沿著推理累積的問題 [@yao2022-react, §1]。
- 只會行動的方法則不會對高層目標做抽象推理，也沒有維護 working memory 來支援行動 [@yao2022-react, §1]。

## 方法

- **擴充動作空間**：原本 agent 在時間 $t$ 根據脈絡 $c_t$ 選動作 $a_t \in \mathcal{A}$。ReAct 把動作空間擴成 $\hat{\mathcal{A}} = \mathcal{A} \cup \mathcal{L}$，$\mathcal{L}$ 是語言空間。語言動作（thought）**不影響環境、沒有觀察回饋**，只是把推理結果加進脈絡，幫助之後推理或行動 [@yao2022-react, §2]。
- Thought 的用途：拆解目標、擬定計畫、注入常識、從觀察中抽取重點、追蹤進度、處理例外並調整計畫 [@yao2022-react, §2]。
- 一段軌跡的格式：`Thought → Action → Observation → Thought → …`。
- **知識型任務**（HotpotQA、FEVER）：每一步都有 thought（dense thought）。**決策型任務**（ALFWorld、WebShop）：thought 只稀疏出現在關鍵位置，由模型自己決定何時思考 [@yao2022-react, §2]。
- 主要設定：凍結的 PaLM-540B，用 few-shot 範例 prompting，每個範例是人寫的「想法＋行動＋觀察」軌跡 [@yao2022-react, §2]。
- **Wikipedia API** 只有三個動作 [@yao2022-react, §3.1]：
  - `search[entity]`：回傳該條目前 5 句，找不到就建議 5 個相似條目
  - `lookup[string]`：回傳頁面中下一個含該字串的句子（模擬 Ctrl+F）
  - `finish[answer]`：交出答案
- **結合內外部知識**：ReAct → CoT-SC（ReAct 在步數上限內沒給答案就改用 CoT-SC）；CoT-SC → ReAct（CoT-SC 多數決答案出現不到一半就改用 ReAct）[@yao2022-react, §3.2]。

## 實驗與結果

**HotpotQA（EM）與 FEVER（Acc）**，PaLM-540B prompting [@yao2022-react, Table 1]：

| 方法 | HotpotQA | FEVER | 出處 |
|---|---|---|---|
| Standard | 28.7 | 57.1 | [@yao2022-react, Table 1] |
| CoT | 29.4 | 56.3 | [@yao2022-react, Table 1] |
| CoT-SC | 33.4 | 60.4 | [@yao2022-react, Table 1] |
| Act（只行動） | 25.7 | 58.9 | [@yao2022-react, Table 1] |
| ReAct | 27.4 | 60.9 | [@yao2022-react, Table 1] |
| CoT-SC → ReAct | 34.2 | 64.6 | [@yao2022-react, Table 1] |
| ReAct → CoT-SC | 35.1 | 62.0 | [@yao2022-react, Table 1] |
| Supervised SoTA | 67.5 | 89.5 | [@yao2022-react, Table 1] |

- ReAct 在兩個任務都贏 Act，證明推理能引導行動 [@yao2022-react, §3.3]。
- ReAct 在 FEVER 贏 CoT（60.9 vs 56.3），但在 HotpotQA 略輸 CoT（27.4 vs 29.4）[@yao2022-react, §3.3]。
- 最好的是兩者結合：HotpotQA 最佳是 ReAct → CoT-SC，FEVER 最佳是 CoT-SC → ReAct；結合法只用 3–5 個樣本就達到 CoT-SC 用 21 個樣本的表現 [@yao2022-react, §3.3]。

**錯誤分析（HotpotQA，人工標註 200 條軌跡）**[@yao2022-react, Table 2]：

| 類型 | ReAct | CoT | 出處 |
|---|---|---|---|
| 成功：True positive | 94% | 86% | [@yao2022-react, Table 2] |
| 成功：False positive（推理或事實是幻覺） | 6% | 14% | [@yao2022-react, Table 2] |
| 失敗：Reasoning error | 47% | 16% | [@yao2022-react, Table 2] |
| 失敗：Search result error | 23% | – | [@yao2022-react, Table 2] |
| 失敗：Hallucination | 0% | 56% | [@yao2022-react, Table 2] |
| 失敗：Label ambiguity | 29% | 28% | [@yao2022-react, Table 2] |

- **幻覺是 CoT 的主要失敗原因**（56%）；ReAct 因為有外部知識庫而更 grounded [@yao2022-react, §3.3]。
- ReAct 的交錯結構降低了推理彈性，reasoning error 比 CoT 多；常見錯誤是**重複產生之前的想法和動作，跳不出迴圈** [@yao2022-react, §3.3]。
- 搜尋到沒用的資訊（23% 的錯誤）會讓推理脫軌、很難恢復 [@yao2022-react, §3.3]。

**Finetune**：用 3,000 條正確軌跡 finetune 小模型後，ReAct 變成四種方法中最好的；PaLM-8B finetune 後的 ReAct 贏過所有 PaLM-62B prompting 方法 [@yao2022-react, §3.3]。

**決策型任務** [@yao2022-react, §4]：
- **ALFWorld**：最佳 ReAct 成功率 71%，最佳 Act 45%，BUTLER（模仿學習）37%；連最差的 ReAct（48%）都贏過兩者的最佳 [@yao2022-react, §4]。
- **WebShop**：ReAct 成功率 40.0，Act 30.1，IL+RL 28.7；人類專家 59.6，仍有差距 [@yao2022-react, Table 4]。
- 只用 1–2 個 in-context 範例，就贏過用 $10^3$–$10^5$ 個任務訓練的模仿學習／強化學習方法 [@yao2022-react, §1]。
- ReAct-IM（只回報環境狀態的「內心獨白」）整體成功率 53，ReAct 是 71 → 高層目標拆解和常識推理很重要 [@yao2022-react, §4]。

## 限制

- 複雜、動作空間大的任務需要更多範例，容易超過 in-context learning 的輸入長度上限 [@yao2022-react, §6]。
- 用 prompting 時，小模型（PaLM-8/62B）的 ReAct 是四種方法中最差的，因為很難從範例同時學會推理和行動 [@yao2022-react, §3.3]。
- 容易陷入重複的想法／動作迴圈；作者懷疑和 greedy decoding 有關 [@yao2022-react, §3.3]。
- 倫理：讓 LLM 連上外部環境可能查到不當／私人資訊或做出有害行動，實驗刻意只限 Wikipedia 和 WebShop，且不能真的購買或編輯 [@yao2022-react, Ethics Statement]。

## 和其他論文的關係

- 把 [CoT](wei2022-chain-of-thought.md) 當「只推理」baseline，並和它結合（ReAct ↔ CoT-SC）。比較見 [CoT vs ReAct](../comparisons/cot-vs-react.md)。
- 概念見 [Reasoning and Acting](../concepts/reasoning-and-acting.md)、[Few-shot prompting](../concepts/few-shot-prompting.md)。
- 同樣讓模型使用工具的 [Toolformer](schick2023-toolformer.md) 改用 finetune、每次最多一個呼叫；比較見 [Tool use](../concepts/tool-use.md)。
- Benchmark：[HotpotQA](../benchmarks/hotpotqa.md)、[FEVER](../benchmarks/fever.md)、[ALFWorld](../benchmarks/alfworld.md)、[WebShop](../benchmarks/webshop.md)。
