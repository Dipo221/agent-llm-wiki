---
type: comparison
title: CoT vs Act vs ReAct
sources: [wei2022-chain-of-thought, yao2022-react]
related: [papers/wei2022-chain-of-thought.md, papers/yao2022-react.md, concepts/chain-of-thought.md, concepts/reasoning-and-acting.md]
updated: 2026-11-17
---

# CoT vs Act vs ReAct

## 比較什麼

「只推理」「只行動」「邊想邊做」三種 prompting 方式的差別。數字都來自 ReAct 論文的同一組實驗（PaLM-540B）。

| 面向 | CoT（只推理） | Act（只行動） | ReAct（推理＋行動） | 出處 |
|---|---|---|---|---|
| 會不會查外部資料 | 不會，只用模型內部知識 | 會 | 會 | [@yao2022-react, §1] |
| 會不會寫推理 | 會 | 不會 | 會 | [@yao2022-react, §3.2] |
| HotpotQA EM | 29.4 | 25.7 | 27.4 | [@yao2022-react, Table 1] |
| FEVER Acc | 56.3 | 58.9 | 60.9 | [@yao2022-react, Table 1] |
| 主要失敗原因（HotpotQA） | Hallucination 56% | – | Reasoning error 47% | [@yao2022-react, Table 2] |
| ALFWorld 最佳成功率 | – | 45% | 71% | [@yao2022-react, §4] |

## 觀察

- 沒有一種方法全面勝出：HotpotQA 上 CoT 略好，FEVER 上 ReAct 較好 [@yao2022-react, §3.3]。
- 失敗方式互補：CoT 會編造事實，ReAct 會卡在推理或搜尋，所以作者把兩者結合，HotpotQA 最佳 35.1（ReAct → CoT-SC），FEVER 最佳 64.6（CoT-SC → ReAct）[@yao2022-react, Table 1]。
- CoT 論文本身只測「不需要外部資訊」的推理任務（算術、常識、符號），沒有和行動型方法比較 [@wei2022-chain-of-thought, §3–§5]。

> 💭 筆記：給新手的講法可以是「CoT＝閉卷考時把算式寫出來，ReAct＝開書考，可以邊想邊翻書」。這是我的比喻，不是論文說法，簡報若要用必須另外標明。
