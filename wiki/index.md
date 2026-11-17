# AI Agents 論文 Wiki — 目錄

> 每頁一行：連結 — 一句話。新增頁面時一併更新。規則見 [AGENTS.md](../AGENTS.md)。

## 論文頁

- [Wei 2022 — Chain-of-Thought Prompting](papers/wei2022-chain-of-thought.md) — few-shot 範例加上推理過程，大模型的推理能力大幅提升
- [Yao 2022 — ReAct](papers/yao2022-react.md) — 交錯產生想法與行動，邊推理邊查外部資料
- [Shinn 2023 — Reflexion](papers/shinn2023-reflexion.md) — 失敗後寫文字反省存進記憶，下次帶著經驗重試
- [Park 2023 — Generative Agents](papers/park2023-generative-agents.md) — 記憶流＋反思＋計畫，25 個 agent 模擬小鎮生活
- [Wang 2023 — Agent Survey](papers/wang2023-agent-survey.md) — Profile／Memory／Planning／Action 四模組統一架構與挑戰
- [Schick 2023 — Toolformer](papers/schick2023-toolformer.md) — 模型自己標註並篩選 API 呼叫，學會何時用哪個工具

## 概念頁

- [Chain-of-Thought](concepts/chain-of-thought.md) — 先寫中間推理步驟再回答
- [Few-shot prompting](concepts/few-shot-prompting.md) — 不 finetune，只在 prompt 放範例
- [Reasoning and Acting](concepts/reasoning-and-acting.md) — 推理引導行動、行動回饋推理
- [Tool use](concepts/tool-use.md) — 呼叫外部工具補足 LLM 的先天限制
- [Self-reflection](concepts/self-reflection.md) — 把成功／失敗訊號放大成文字反省（另注意 Generative Agents 的不同用法）
- [Agent memory](concepts/agent-memory.md) — 短期／長期記憶、記憶流與檢索
- [Planning](concepts/planning.md) — 有沒有回饋的規劃方式（CoT、ReAct、Reflexion）

## 比較頁

- [CoT vs Act vs ReAct](comparisons/cot-vs-react.md) — 只推理／只行動／邊想邊做的成績與失敗模式
- [Agent 架構對照](comparisons/agent-framework-map.md) — 用 Survey 四模組對照五篇論文＋時間軸

## Benchmark 頁

- [GSM8K](benchmarks/gsm8k.md) — 小學數學應用題（算術推理）
- [ASDiv、SVAMP、MAWPS](benchmarks/math-word-problems.md) — 較簡單的數學應用題；⚠ 兩篇論文的 GPT-3 數字不一致
- [HotpotQA](benchmarks/hotpotqa.md) — 多跳問答
- [FEVER](benchmarks/fever.md) — 事實查核
- [ALFWorld](benchmarks/alfworld.md) — 文字版居家任務遊戲
- [WebShop](benchmarks/webshop.md) — 網路購物環境
- [HumanEval](benchmarks/humaneval.md) — 程式生成（pass@1）
