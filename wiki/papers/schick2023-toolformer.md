---
type: paper
title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
sources: [schick2023-toolformer]
related: [concepts/tool-use.md, concepts/few-shot-prompting.md, papers/yao2022-react.md, benchmarks/math-word-problems.md]
arxiv: 2302.04761
authors: Timo Schick et al.（Meta AI Research）
venue: arXiv（NeurIPS 2023）
updated: 2026-11-17
---

# Toolformer（Schick et al., 2023）

## 一句話

讓語言模型**自己教自己**在文字中插入 API 呼叫（計算機、問答系統、Wikipedia 搜尋、翻譯、日曆），只需要每個 API 幾個示範，再用「這個呼叫有沒有讓下文更好預測」來篩選，最後 finetune 模型 [@schick2023-toolformer, Abstract]。

## 要解決的問題

- 大模型很會做新任務，卻在算術、查事實這類「小模型或簡單工具就能做好」的基本功能上表現差 [@schick2023-toolformer, Abstract]。
- 其他限制：拿不到最新資訊、容易幻覺、低資源語言理解差、不會精確計算、不知道現在是什麼時間 [@schick2023-toolformer, §1]。
- 既有的工具使用方法不是要大量人工標註，就是只能用在特定任務 [@schick2023-toolformer, §1]。
- 目標：(1) 用 self-supervised 方式學會用工具，不靠大量人工標註；(2) 不失去通用能力，**模型自己決定何時、怎麼用哪個工具** [@schick2023-toolformer, §1]。

## 方法

**API 呼叫的文字表示**：把呼叫線性化成文字插進句子裡 [@schick2023-toolformer, §2]
$$e(c, r) = \texttt{<API>}\; a_c(i_c) \rightarrow r \;\texttt{</API>}$$
例：`Out of 1400 participants, 400 (or [Calculator(400 / 1400) → 0.29] 29%) passed the test.`（Figure 1）

**三個步驟**（Figure 2）[@schick2023-toolformer, §2]：
1. **取樣 API 呼叫**：用 in-context learning 的 prompt（每個 API 只要幾個示範）讓模型在大量文本中標出「可能可以呼叫 API」的位置與參數。
2. **執行 API 呼叫**：真的去呼叫，拿到回傳文字 $r_i$。
3. **篩選**：比較「給模型看呼叫＋結果」和「不呼叫／只有呼叫沒有結果」兩種情況下，後面 token 的 loss。只保留讓 loss 至少降低 $\tau_f$ 的呼叫：$L_i^- - L_i^+ \ge \tau_f$。

最後把留下來的呼叫插回原文，用一般的 language modeling 目標 finetune 模型。因為除了 API 呼叫以外內容和原資料完全一樣，模型不會失去原本的能力 [@schick2023-toolformer, §2]。

**推論時**：模型產生 `→` 時暫停解碼，真的去呼叫 API，把結果插回去再繼續 [@schick2023-toolformer, §2]。

**五個工具** [@schick2023-toolformer, §3]：問答系統（Atlas）、計算機（只有四則運算，結果取到小數點後兩位）、Wikipedia 搜尋（BM25）、翻譯（NLLB，翻成英文）、日曆（回傳今天日期）。

**基底模型**：GPT-J 6.7B [@schick2023-toolformer, §1]。測試一律 **zero-shot**（不給範例），每個輸入最多呼叫一次 API，避免模型一直呼叫 API 卡在迴圈 [@schick2023-toolformer, §4.2]。

## 實驗與結果

Toolformer 以 GPT-J 為基底，比較對象 GPT-3 約大 25 倍 [@schick2023-toolformer, §4.1]：

| 任務 | Toolformer | GPT-3 | 主要用的工具 | 出處 |
|---|---|---|---|---|
| LAMA T-REx（補事實） | 53.5 | 39.8 | 問答系統（98.1% 的例子） | [@schick2023-toolformer, Table 3] |
| ASDiv（數學） | 40.4 | 14.0 | 計算機（97.9% 的例子） | [@schick2023-toolformer, Table 4] |
| SVAMP（數學） | 29.4 | 10.0 | 計算機 | [@schick2023-toolformer, Table 4] |
| MAWPS（數學） | 44.0 | 19.8 | 計算機 | [@schick2023-toolformer, Table 4] |
| WebQS（問答） | 26.3 | 29.0 | Wikipedia 搜尋（99.3%） | [@schick2023-toolformer, Table 5] |
| TriviaQA（問答） | 48.8 | 65.9 | Wikipedia 搜尋 | [@schick2023-toolformer, Table 5] |
| DATESET（日期推算） | 27.3 | 0.8 | 日曆（54.8%） | [@schick2023-toolformer, Table 7] |

- **LAMA、數學**：6.7B 的 Toolformer 贏過大很多的 OPT（66B）和 GPT-3（175B）[@schick2023-toolformer, §4.2]。
- **數學**：允許呼叫 API 讓所有數學任務的表現都增加超過一倍 [@schick2023-toolformer, §4.2]。
- **問答**：贏過同尺寸模型，但輸給 GPT-3。原因是搜尋引擎太簡單，而且 Toolformer 不能改寫查詢、不能翻看多筆結果 [@schick2023-toolformer, §4.2]。
- **TempLAMA**：雖然有進步，但日曆工具只用在 0.2% 的例子，進步主要來自搜尋和問答工具 [@schick2023-toolformer, §4.2]。
- **不傷語言能力**：關掉 API 時，perplexity 和沒加 API 訓練的模型一樣 [@schick2023-toolformer, §4.3]。
- **規模**：用工具的能力大約在 775M 參數才出現，更小的模型有沒有工具表現都差不多 [@schick2023-toolformer, §4.4]。

## 限制

作者列出的限制 [@schick2023-toolformer, §7]：
1. **不能串接工具**（把一個工具的輸出當另一個工具的輸入），因為每個工具的訓練資料是分開產生的。
2. **不能互動式使用工具**：例如瀏覽多筆搜尋結果或改寫查詢。
3. 決定要不要呼叫 API 時，對輸入的措辭很敏感。
4. 有些工具很沒效率：處理超過一百萬份文件，只得到幾千個有用的計算機呼叫。
5. 不考慮呼叫工具的計算成本。

## 和其他論文的關係

- 和 [ReAct](yao2022-react.md) 同樣讓模型使用外部工具（ReAct 用 Wikipedia API），但做法不同：ReAct 靠 few-shot prompting、可以多步互動；Toolformer 靠 finetune、zero-shot、每次最多一個呼叫。見 [Tool use](../concepts/tool-use.md)。
- 數學資料集和 [CoT](wei2022-chain-of-thought.md) 有重疊，但成績差異很大，見 [數學應用題 benchmark](../benchmarks/math-word-problems.md) 的 ⚠ 區塊。

> 💭 筆記：Toolformer 的限制 1、2（不能串接、不能互動）正好是 ReAct 式 agent 擅長的地方。
