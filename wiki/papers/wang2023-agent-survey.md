---
type: paper
title: "A Survey on Large Language Model based Autonomous Agents"
sources: [wang2023-agent-survey]
related: [comparisons/agent-framework-map.md, concepts/planning.md, concepts/agent-memory.md, concepts/tool-use.md]
arxiv: 2308.11432
authors: Lei Wang et al.（中國人民大學高瓴人工智慧學院）
venue: Frontiers of Computer Science（2025）
updated: 2026-11-17
---

# LLM-based Autonomous Agents Survey（Wang et al., 2023）

## 一句話

整理 LLM-based autonomous agent 的研究，提出一個涵蓋大多數既有研究的**統一架構：Profile（角色）、Memory（記憶）、Planning（規劃）、Action（行動）四個模組**，並整理應用、評估方式與挑戰 [@wang2023-agent-survey, §1]。

## 要解決的問題

- 過去的 agent 多半依賴簡單的策略，在封閉受限的環境中學習，和人類學習方式差很多，很難做出像人的決策 [@wang2023-agent-survey, Abstract]。
- LLM 從大量網路資料學到知識，展現接近人類智慧的潛力，帶動 LLM-based agent 研究爆發；但這些模型各自提出，很少有人整體比較 [@wang2023-agent-survey, §1]。
- 和強化學習的 agent 相比，LLM-based agent 有更完整的世界知識，沒有針對特定領域訓練也能行動，而且提供自然語言介面、更好解釋 [@wang2023-agent-survey, §1]。

## 方法（統一架構）

**Agent 的定義**（引用 Franklin and Graesser 1997）：autonomous agent 是位於環境之中、感知環境並對其行動的系統，長期追求自己的目標，並影響自己之後感知到的東西 [@wang2023-agent-survey, §1]。

**四個模組**（Fig. 2）[@wang2023-agent-survey, §2.1]：

| 模組 | 負責什麼 | 出處 |
|---|---|---|
| Profile | 決定 agent 的角色（例如程式設計師、老師、領域專家），通常寫進 prompt | [@wang2023-agent-survey, §2.1.1] |
| Memory | 記住過去的行為與觀察 | [@wang2023-agent-survey, §2.1.2] |
| Planning | 把複雜任務拆成子任務、規劃未來行動 | [@wang2023-agent-survey, §2.1.3] |
| Action | 把決策轉成具體輸出 | [@wang2023-agent-survey, §2.1.4] |

Profile 影響 Memory 和 Planning，三者一起影響 Action [@wang2023-agent-survey, §2.1]。作者把架構比喻成 agent 的「硬體」，把能力取得比喻成「軟體」[@wang2023-agent-survey, §2.2]。

**Memory 模組** [@wang2023-agent-survey, §2.1.2]：
- 參考人類記憶：短期記憶像 context window 裡的內容，長期記憶像可以隨時查詢的外部向量儲存。
- *Unified memory*：只有短期記憶，直接寫在 prompt 裡；受 context window 限制。
- *Hybrid memory*：短期＋長期，例如 Generative Agents、Reflexion。
- 記憶操作有三種：讀（reading）、寫（writing）、反思（reflection）。Generative Agents 的反思被歸類為「記憶反思」。

**Planning 模組** [@wang2023-agent-survey, §2.1.3]：
- *沒有回饋*：single-path（CoT、Zero-shot-CoT）、multi-path（CoT-SC、Tree of Thoughts）、外部 planner。
- *有回饋*：環境回饋（ReAct 的 thought-act-observation）、人類回饋、模型回饋（Reflexion 的文字回饋）。

**Action 模組** [@wang2023-agent-survey, §2.1.4]：從目標、怎麼產生、動作空間、影響四個角度看。動作空間分成「外部工具」和「LLM 內部知識」；Toolformer 被列為用 self-supervised 學習決定何時、怎麼呼叫工具的例子。

**能力取得** [@wang2023-agent-survey, §2.2]：
- *要 finetune*：用人工標註、LLM 生成或真實世界的資料集。
- *不用 finetune*：prompt engineering（如 CoT）和 mechanism engineering（試誤、多 agent 辯論、經驗累積、自我演化）。

**評估** [@wang2023-agent-survey, §4]：主觀評估（人類評分，適合沒有資料集或很難量化的情境）和客觀評估（量化指標、benchmark）。

## 實驗與結果

這是 survey，沒有自己的實驗。Fig. 1 統計了 2021 年 1 月到 2023 年 8 月累積的論文數，呈現快速成長 [@wang2023-agent-survey, Fig. 1]。

## 限制（作者整理的領域挑戰）

[@wang2023-agent-survey, §6]
1. **角色扮演能力**：網路上少見或新出現的角色，LLM 演不好。
2. **廣義的人類對齊**：做社會模擬時，可能需要 agent 呈現人類的負面特質，但現有模型都對齊同一套價值觀。
3. **Prompt 穩健性**：agent 有好幾個模組，每個模組的 prompt 會互相影響，換模型又要重調。
4. **幻覺**：agent 也會很有自信地產生錯誤資訊，例如寫出錯誤的程式。
5. **知識邊界**：模擬一般人時，LLM 知道的遠超過一般人，會影響模擬的真實性。
6. **效率**：每個動作可能要呼叫 LLM 好幾次（讀記憶、做計畫），推論速度慢。

## 和其他論文的關係

- 這篇把 wiki 裡另外 5 篇論文都放進四模組架構中，對照表見 [Agent 架構對照](../comparisons/agent-framework-map.md)。
- 概念頁：[Planning](../concepts/planning.md)、[Agent memory](../concepts/agent-memory.md)、[Tool use](../concepts/tool-use.md)。
