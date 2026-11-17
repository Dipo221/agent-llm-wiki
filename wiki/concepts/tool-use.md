---
type: concept
title: Tool use（工具使用）
sources: [schick2023-toolformer, yao2022-react, wang2023-agent-survey]
related: [papers/schick2023-toolformer.md, papers/yao2022-react.md, concepts/reasoning-and-acting.md]
updated: 2026-11-17
---

# Tool use（工具使用）

## 定義

讓語言模型呼叫外部工具（搜尋引擎、計算機、日曆、翻譯等），彌補它拿不到最新資訊、容易幻覺、不會精確計算、不知道時間等先天限制 [@schick2023-toolformer, §1]。

Survey 把 agent 的動作空間分成「外部工具」和「LLM 內部知識」兩類；使用外部工具是為了彌補 LLM 缺乏專業知識和幻覺的問題 [@wang2023-agent-survey, §2.1.4]。

## 各論文怎麼做

| 面向 | [ReAct](../papers/yao2022-react.md) | [Toolformer](../papers/schick2023-toolformer.md) | 出處 |
|---|---|---|---|
| 怎麼學會用工具 | few-shot prompting，範例是人寫的軌跡 | self-supervised 產生訓練資料再 finetune | [@yao2022-react, §2]、[@schick2023-toolformer, §2] |
| 工具 | Wikipedia API（search／lookup／finish），或遊戲、購物網站的動作 | 問答、計算機、Wikipedia 搜尋、翻譯、日曆 | [@yao2022-react, §3.1]、[@schick2023-toolformer, §3] |
| 一次任務呼叫幾次 | 多步互動，依觀察決定下一步 | 每個輸入最多一次 | [@yao2022-react, §2]、[@schick2023-toolformer, §4.2] |
| 有沒有明寫推理 | 有（Thought） | 沒有，直接在文字中插入呼叫 | [@yao2022-react, §2]、[@schick2023-toolformer, §2] |
| 基底模型 | PaLM-540B（凍結） | GPT-J 6.7B（finetune） | [@yao2022-react, §2]、[@schick2023-toolformer, §1] |

## 優點與限制

**優點**
- 小模型加工具可以贏大模型：Toolformer（6.7B）在 ASDiv 拿到 40.4，GPT-3（175B）是 14.0 [@schick2023-toolformer, Table 4]。
- 查外部資料能減少幻覺：ReAct 在 HotpotQA 的失敗案例中幻覺是 0%，CoT 是 56% [@yao2022-react, Table 2]。

**限制**
- 工具回傳的資訊不好時，會拖垮推理：ReAct 的錯誤有 23% 來自沒用的搜尋結果 [@yao2022-react, §3.3]。
- Toolformer 不能串接工具、不能互動式搜尋 [@schick2023-toolformer, §7]。
- 安全風險：連上外部環境可能查到不當資訊或做出有害行動 [@yao2022-react, Ethics Statement]。

## 相關頁面

- [Reasoning and Acting](reasoning-and-acting.md)
- [Agent 架構對照](../comparisons/agent-framework-map.md)
- [數學應用題 benchmark](../benchmarks/math-word-problems.md)
