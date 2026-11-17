---
type: concept
title: Self-reflection（自我反省）
sources: [shinn2023-reflexion, yao2022-react, park2023-generative-agents]
related: [papers/shinn2023-reflexion.md, concepts/reasoning-and-acting.md]
updated: 2026-11-17
---

# Self-reflection（自我反省）

## 定義

Agent 把環境給的簡單回饋（成功／失敗、分數）**放大成文字反省**：指出哪一步做錯、下次該怎麼做，存進記憶，作為下一次嘗試的額外脈絡。Reflexion 把這種反省稱為「語意上的梯度訊號」[@shinn2023-reflexion, §1]。

## 各論文怎麼做

- **[Reflexion](../papers/shinn2023-reflexion.md)**：Actor 嘗試 → Evaluator 評分 → Self-Reflection 寫反省 → 加進長期記憶 → 再嘗試 [@shinn2023-reflexion, §3]。
- **對照：[ReAct](../papers/yao2022-react.md)** 只在單次嘗試內思考；失敗時常重複產生之前的想法和動作，跳不出迴圈 [@yao2022-react, §3.3]。Reflexion 在 ALFWorld 用 heuristic 偵測這種重複，偵測到就觸發反省 [@shinn2023-reflexion, §4.1]。

- **[Generative Agents](../papers/park2023-generative-agents.md) 的 reflection 意思不同**：不是針對失敗反省，而是定期把大量觀察**歸納成高層推論**（例：「Klaus 很投入他的研究」），並引用作為證據的記憶 [@park2023-generative-agents, §4.2]。觸發條件是最近事件的重要性總和超過 150，而不是任務失敗 [@park2023-generative-agents, §4.2]。

## 優點與限制

**優點**
- 不用 finetune，只靠文字記憶就能跨嘗試進步 [@shinn2023-reflexion, §1]。
- 反省內容是人看得懂的文字，可以在 agent 使用工具前先檢查它的意圖 [@shinn2023-reflexion, §6]。

**限制**
- 依賴 LLM 自我評估的能力，沒有成功保證 [@shinn2023-reflexion, §1]。
- 小模型做不到：starchat-beta 加上 Reflexion 沒有進步 [@shinn2023-reflexion, Table 4]。
- 評估器不準時會誤導：程式任務中測試太弱，錯的程式也會通過 [@shinn2023-reflexion, §4.3]。

## 相關頁面

- [Reasoning and Acting](reasoning-and-acting.md)
- [Agent memory](agent-memory.md)
- [HumanEval](../benchmarks/humaneval.md)
