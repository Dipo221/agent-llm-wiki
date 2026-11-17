---
type: paper
title: "Generative Agents: Interactive Simulacra of Human Behavior"
sources: [park2023-generative-agents]
related: [concepts/agent-memory.md, concepts/self-reflection.md, papers/shinn2023-reflexion.md]
arxiv: 2304.03442
authors: Joon Sung Park et al.（Stanford University、Google Research、Google DeepMind）
venue: UIST 2023
updated: 2026-11-17
---

# Generative Agents（Park et al., 2023）

## 一句話

用 LLM 打造 25 個會起床、上班、聊天、交朋友、辦派對的虛擬居民，住在一個像 The Sims 的小鎮 Smallville；關鍵是一套「**記憶流 → 反思 → 計畫**」的 agent 架構 [@park2023-generative-agents, Abstract]。

## 要解決的問題

- LLM 能模擬「某一個時間點」的人類行為，但要長時間保持一致，需要能管理不斷增加的記憶，並處理多個 agent 之間連鎖的社交互動 [@park2023-generative-agents, §1]。
- 把所有經歷摘要後塞進 prompt 行不通：記憶太多會讓模型分心，也放不進 context window [@park2023-generative-agents, §4.1]。

## 方法

架構有三個元件，底層模型是 gpt3.5-turbo 版本的 ChatGPT [@park2023-generative-agents, §4]。

**1. 記憶流（memory stream）與檢索** [@park2023-generative-agents, §4.1]
- 用自然語言完整記錄 agent 的所有經歷；每筆記憶有文字描述、建立時間、最近存取時間。最基本的記憶是「觀察」（例：冰箱是空的）。
- 檢索時，每筆記憶依三個分數加權排序：
  $$\text{score} = \alpha_{\text{recency}}\cdot\text{recency} + \alpha_{\text{importance}}\cdot\text{importance} + \alpha_{\text{relevance}}\cdot\text{relevance}$$
  - **Recency**：越近期存取的越高分，用指數衰減，衰減係數 0.995 [@park2023-generative-agents, §4.1]。
  - **Importance**：直接請 LLM 打 1–10 分（例：打掃房間 2 分、約暗戀對象出去 8 分） [@park2023-generative-agents, §4.1]。
  - **Relevance**：記憶和目前情境的 embedding cosine similarity。

**2. 反思（reflection）** [@park2023-generative-agents, §4.2]
- 只有原始觀察時，agent 很難歸納（例：Klaus 只會選「最常碰面」的人，而不是「志趣相投」的人）。
- 最近事件的 importance 分數總和超過門檻（150）時觸發反思，大約一天 2–3 次 [@park2023-generative-agents, §4.2]。
- 步驟：拿最近 100 筆記憶，請 LLM 提出 3 個最值得問的高層問題 → 用問題去檢索 → 請 LLM 歸納 5 個 insight，並**引用作為證據的記憶編號** → 存回記憶流 [@park2023-generative-agents, §4.2]。
- 反思也可以針對反思，形成「反思樹」：葉子是觀察，越往上越抽象。

**3. 計畫與反應（planning and reacting）** [@park2023-generative-agents, §4.3]
- 沒有計畫時，Klaus 會在 12 點、12 點半、1 點各吃一次午餐——只顧當下合理，長期就不合理 [@park2023-generative-agents, §4.3]。
- 計畫包含地點、開始時間、長度，先產生一天的粗略計畫，再遞迴拆成細節；計畫也存回記憶流。

## 實驗與結果

**受控評估（訪談 agent）** [@park2023-generative-agents, §6]：
- 100 位受試者比較 5 種條件的回答「像不像真人」並排序，用 TrueSkill 計分 [@park2023-generative-agents, §6.1]。
- 結果（TrueSkill 平均 μ）[@park2023-generative-agents, §6.5.1]：

| 條件 | μ | 出處 |
|---|---|---|
| 完整架構 | 29.89 | [@park2023-generative-agents, §6.5.1] |
| 沒有反思 | 26.88 | [@park2023-generative-agents, §6.5.1] |
| 沒有反思、沒有計畫 | 25.64 | [@park2023-generative-agents, §6.5.1] |
| 人類群眾外包寫的回答 | 22.95 | [@park2023-generative-agents, §6.5.1] |
| 沒有記憶、反思、計畫（代表過去的做法） | 21.21 | [@park2023-generative-agents, §6.5.1] |

- 完整架構比「過去的做法」好 8 個標準差（Cohen's d = 8.16）[@park2023-generative-agents, §6.5.1]。
- 反思對需要歸納的問題特別重要：沒有反思時，Maria 說不知道 Wolfgang 喜歡什麼；有反思時，她知道他喜歡數學作曲 [@park2023-generative-agents, §6.5.3]。

**端對端模擬（兩個遊戲日）** [@park2023-generative-agents, §7.1.2]：
- **資訊擴散**：知道 Sam 參選鎮長的 agent 從 1 個（4%）增加到 8 個（32%）；知道情人節派對的從 1 個（4%）增加到 13 個（52%），全程沒有使用者介入 [@park2023-generative-agents, §7.1.2]。
- **建立關係**：社交網路密度從 0.167 增加到 0.74；453 個關於「認不認識某人」的回答中，1.3% 是幻覺 [@park2023-generative-agents, §7.1.2]。
- **協調**：被邀請的 12 個 agent 中，有 5 個在情人節準時出現在派對 [@park2023-generative-agents, §7.1.2]。

## 限制

- **記憶錯誤**：會檢索不到正確記憶、只拿到片段，或在知識上「加油添醋」（例如把鄰居 Adam Smith 說成寫《國富論》的人）[@park2023-generative-agents, §6.5.2]。
- **怪異行為**：記憶越多越難選對地點（跑去酒吧吃午餐）；不懂物理規範（多人擠單人浴室、店家 5 點打烊後還進去）；instruction tuning 讓 agent 過度禮貌、過度配合 [@park2023-generative-agents, §7.2]。
- **成本**：模擬 25 個 agent 兩天，花了數千美元的 token 費用、跑了好幾天 [@park2023-generative-agents, §8.2]。
- **穩健性未知**：可能被 prompt hacking、memory hacking 攻擊，也會繼承底層 LLM 的偏見 [@park2023-generative-agents, §8.2]。
- **倫理**：使用者可能和 agent 建立不恰當的類社會關係；作者建議 agent 要明確揭露自己是電腦程式 [@park2023-generative-agents, §8.3]。

## 和其他論文的關係

- 和 [Reflexion](shinn2023-reflexion.md) 都有「reflection」和長期記憶，但用途不同，見 [Self-reflection](../concepts/self-reflection.md) 和 [Agent memory](../concepts/agent-memory.md)。

> 💭 筆記：反思步驟「歸納 insight 並引用記憶編號」很像這個 wiki 的出處規則——結論要能追回證據。
