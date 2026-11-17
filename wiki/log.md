# Wiki 紀錄

> 新的放最上面。格式：`## YYYY-MM-DD 動作：對象`，下面列新增／修改的頁面與備註。

## 2026-11-17 ingest：park2023-generative-agents
- 新增：papers/park2023-generative-agents.md、concepts/agent-memory.md
- 更新：concepts/self-reflection.md、papers/shinn2023-reflexion.md、index.md
- 術語衝突（不是數字矛盾）：「reflection」在 Reflexion 指針對失敗的反省，在 Generative Agents 指把觀察歸納成高層推論。已在 self-reflection.md 分開說明，避免簡報混用。
- 無標準 benchmark（評估是人類評分 believability），因此沒有新增 benchmark 頁。
- lint 第 1 次：8 個問題——出處只標在上層標題，底下列表項目的數字沒有各自出處（違反第 6 節「同一段」規則）。逐項補上後通過。

## 2026-11-17 ingest：shinn2023-reflexion
- 新增：papers/shinn2023-reflexion.md、concepts/self-reflection.md、benchmarks/humaneval.md
- 更新：benchmarks/alfworld.md、benchmarks/hotpotqa.md（補 Reflexion 結果並註明不可直接比較）、papers/yao2022-react.md、concepts/reasoning-and-acting.md、index.md
- **矛盾**：shinn2023-reflexion.md——GPT-4 在 HumanEval Python 的 baseline，摘要 80%、Table 1 80.1、§4.3 82%（同一篇論文內）。並列＋⚠，引用以 Table 1 為準。
- lint 第 1 次：1 個問題——humaneval.md 提到 80%／80.1／82% 但沒附出處，補上後通過。
- 注意：Reflexion 的 HotpotQA／ALFWorld 數字（100 題、多次嘗試、GPT 系列模型）和 ReAct 論文（全部題目、單次、PaLM）設定不同，benchmark 頁已加註「不能直接比較」。

## 2026-11-17 ingest：schick2023-toolformer
- 新增：papers/schick2023-toolformer.md、concepts/tool-use.md、benchmarks/math-word-problems.md
- 更新：papers/yao2022-react.md（連到 Toolformer）、concepts/few-shot-prompting.md（zero-shot 對照）、concepts/reasoning-and-acting.md、benchmarks/gsm8k.md、index.md
- **矛盾**：math-word-problems.md——GPT-3 175B 在 SVAMP，CoT 論文報 65.7（text-davinci-002、few-shot），Toolformer 論文報 10.0（原始 davinci、zero-shot）。依規則並列兩種說法並加 ⚠ 區塊，不下結論。
- lint 第 1 次：5 個問題——3 頁沒列入 index（流程順序：先寫頁面、後更新 index）、表頭「6.7B／175B」沒出處、⚠ 區塊未記 log。修正後通過。

## 2026-11-17 ingest：yao2022-react
- 新增：papers/yao2022-react.md、concepts/reasoning-and-acting.md、comparisons/cot-vs-react.md、benchmarks/hotpotqa.md、fever.md、alfworld.md、webshop.md
- 更新：concepts/chain-of-thought.md（補 CoT-SC 與幻覺比例）、concepts/few-shot-prompting.md（補 ReAct 範例數）
- 矛盾檢查：無矛盾。ReAct 在 HotpotQA 略輸 CoT（27.4 vs 29.4）是同一篇論文內的結果，不是跨論文矛盾。
- lint：全部通過。

## 2026-11-17 ingest：wei2022-chain-of-thought
- 新增：papers/wei2022-chain-of-thought.md、concepts/chain-of-thought.md、concepts/few-shot-prompting.md、benchmarks/gsm8k.md
- lint 第 1 次：1 個問題——「（§3.2）」章節編號被當成沒出處的數字。修正：改成 [@slug, §3.2] 格式，並讓 lint.py 忽略 §／Table／Fig. 編號。
- lint 自我測試：故意把 GSM8K 的 56.9 改成 58.1，lint 正確抓出「原文找不到」，還原後通過。
- lint 第 2 次：全部通過。

## 2026-11-17 建立：Wiki 骨架
- 依訪談需求摘要建立 AGENTS.md、資料夾、index.md、log.md、scripts/lint.py。
- raw/papers/ 下載 6 篇論文 PDF 並轉 txt。
