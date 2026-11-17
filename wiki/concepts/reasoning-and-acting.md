---
type: concept
title: Reasoning and Acting（邊想邊做）
sources: [yao2022-react, wei2022-chain-of-thought]
related: [papers/yao2022-react.md, concepts/chain-of-thought.md, comparisons/cot-vs-react.md]
updated: 2026-11-17
---

# Reasoning and Acting

## 定義

讓語言模型**交錯**產生推理軌跡（thought）和任務相關的行動（action）：推理幫助建立、追蹤、更新行動計畫並處理例外（reason to act）；行動從外部環境取得新資訊再拿來推理（act to reason）[@yao2022-react, §1]。

形式上是把 agent 的動作空間從 $\mathcal{A}$ 擴成 $\mathcal{A} \cup \mathcal{L}$，語言動作不改變環境、只更新脈絡 [@yao2022-react, §2]。

## 各論文怎麼做

- **[ReAct](../papers/yao2022-react.md)**：`Thought → Action → Observation` 迴圈。知識型任務每步都想（dense），決策型任務只在關鍵處想（sparse）[@yao2022-react, §2]。
- **對照組**：[CoT](../papers/wei2022-chain-of-thought.md) 只推理不行動；ReAct 論文中的 Act baseline 只行動不推理 [@yao2022-react, §3.2]。

## 優點與限制

**優點**
- 比只行動好：ALFWorld 最佳成功率 71% vs Act 45% [@yao2022-react, §4]。
- 比只推理更有根據：HotpotQA 成功案例中 false positive 只有 6%，CoT 是 14% [@yao2022-react, Table 2]。
- 人看得懂決策依據，也能直接修改 thought 來控制 agent [@yao2022-react, §2]。

**限制**
- 推理彈性變差，reasoning error 較多，會重複同樣的想法和動作 [@yao2022-react, §3.3]。
- 很依賴搜尋品質：沒用的搜尋結果佔錯誤的 23% [@yao2022-react, §3.3]。

## 相關頁面

- [Tool use](tool-use.md)
- [CoT vs ReAct](../comparisons/cot-vs-react.md)
- [ALFWorld](../benchmarks/alfworld.md)、[HotpotQA](../benchmarks/hotpotqa.md)
