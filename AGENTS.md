# AGENTS.md — AI Agents 論文 LLM Wiki 員工手冊

> 本手冊依 `docs/interview.md` 的訪談與需求摘要產生（先討論、後生成）。
> 修改規則前先更新需求摘要，再改這份手冊，兩邊保持一致。

## 1. 專案目的

- 依 Karpathy 的 LLM Wiki 構想，整理 **AI Agents 相關論文**，讓知識一篇一篇累積，不用每次重新讀原文。
- **Wiki 的讀者是我自己（研究用）**：可以寫得技術，保留方法細節、數字與 benchmark。
- Wiki 之後的產出：教學 HTML 簡報「AI Agents 是什麼？」（流程見 `workflows/topic-slides.md`）。
  **降低難度是簡報流程的工作，不要為了簡報回頭把 wiki 改淺。**

## 2. 資料夾結構

```
AGENTS.md            本手冊（CLAUDE.md 只有一行 @AGENTS.md）
raw/papers/          原始論文：<slug>.pdf ＋ pdftotext 轉出的 <slug>.txt（只讀不改）
wiki/
  index.md           目錄：每頁一行（連結＋一句話），依頁面類型分組
  log.md             紀錄：每次 ingest / lint / 修正，一筆一段，新的放最上面
  papers/            論文頁
  concepts/          概念頁（跨論文的觀念）
  comparisons/       比較頁（對照表、時間軸）
  benchmarks/        Benchmark／資料集頁
scripts/lint.py      Wiki 健檢腳本
workflows/           簡報 workflow（之後建立）
docs/                訪談紀錄、作業說明
```

## 3. 命名規則

- **論文 slug**：`第一作者姓小寫 + 年份 + 方法名`，用 `-` 連接。例：`yao2022-react`。
  `raw/papers/<slug>.pdf`、`raw/papers/<slug>.txt`、`wiki/papers/<slug>.md` 三者同名。
- **年份**用 arXiv 第一版的年份。
- **概念頁、比較頁、Benchmark 頁**：英文 kebab-case。例：`concepts/tool-use.md`、`benchmarks/hotpotqa.md`。
- 檔名一律小寫英文，不用中文、不用空白。

## 4. 語言與格式

- 內文**繁體中文**；技術名詞保留英文（ReAct、in-context learning、few-shot、benchmark）。
- 數學式用 LaTeX：行內 `$...$`，獨立 `$$...$$`。
- 頁面之間用**相對路徑的 Markdown 連結**，例如 `[ReAct](../papers/yao2022-react.md)`。GitHub 和 Obsidian 都能點。

## 5. 頁面開頭欄位（每頁必填）

```yaml
---
type: paper | concept | comparison | benchmark
title: 頁面標題
sources: [yao2022-react, wei2022-chain-of-thought]   # 本頁內容來自哪些論文 slug
related: [concepts/reasoning-and-acting.md]           # 相關頁面（相對於 wiki/）
updated: YYYY-MM-DD
---
```

論文頁另外加：`arxiv:`（編號）、`authors:`（第一作者 et al.）、`venue:`（發表處，不確定就寫 arXiv）。

## 6. 出處規則（最重要）

- 每個**關鍵說法**、每個**數字**，都要在同一段（或同一列表項／表格列）標出處：
  `[@<slug>, §<章節>]` 或 `[@<slug>, Table <n>]` 或 `[@<slug>, Fig. <n>]`。
  例：`ReAct 在 ALFWorld 的成功率比 Act-only 高 [@yao2022-react, Table 3]`。
- 數字必須能在 `raw/papers/<slug>.txt` 找到**一模一樣的寫法**（34% 就寫 34%，不要自己換算或四捨五入）。
  需要換算時，寫出原始數字並註明「（由原文數字換算）」。
- 不知道章節就去 txt 找；找不到就不要寫這個說法。
- **只寫論文裡有的東西**。自己的評論放在 `> 💭 筆記：` 開頭的引用區塊，簡報不可引用這種區塊。

## 7. 論文之間說法不一致

- 兩種說法**並列**，各自標出處。
- 加一個區塊說明可能原因（模型、設定、資料集版本不同），不替讀者下結論：
  ```
  > ⚠ 說法不一致：A 說……[@a, §x]；B 說……[@b, Table y]。可能原因：……
  ```
- 同時在 `log.md` 記一筆「矛盾」。

## 8. 各類頁面的固定段落

**論文頁**（`wiki/papers/`）
1. `## 一句話` — 這篇做了什麼
2. `## 要解決的問題`
3. `## 方法` — 核心機制，必要時附 prompt 格式或演算法步驟
4. `## 實驗與結果` — 用了哪些 benchmark、關鍵數字（每個都要出處）
5. `## 限制` — 作者自己承認的限制優先
6. `## 和其他論文的關係` — 連到其他論文頁／概念頁

**概念頁**：`## 定義` → `## 各論文怎麼做` → `## 優點與限制` → `## 相關頁面`
**比較頁**：`## 比較什麼` → 對照表（每列有出處）→ `## 觀察`
**Benchmark 頁**：`## 在測什麼` → `## 任務形式` → `## 用過它的論文與成績`（表格，每列有出處）

## 9. 工作流程

### Ingest（加入一篇論文）
1. 收到 PDF 存到 `raw/papers/<slug>.pdf`；收到 arXiv 連結就**自己下載 PDF**，再 `pdftotext -layout` 轉成 `<slug>.txt`。
2. 讀全文，寫 `wiki/papers/<slug>.md`。
3. 更新（或新建）相關的概念頁、比較頁、Benchmark 頁。**新建概念頁的門檻：至少兩篇論文會用到，或是這篇的核心機制。**
4. 檢查新內容和既有頁面有沒有矛盾，有就照第 7 節處理。
5. 更新 `wiki/index.md`、在 `wiki/log.md` 最上面加一筆（日期、論文、新增/修改了哪些頁）。
6. 跑 `python3 scripts/lint.py`，全部通過才算完成。
7. 一篇論文一個 commit：`git commit -m "ingest: <slug>"`。

### Query（問問題）
先讀 `wiki/index.md` 決定要讀哪幾頁，只根據 wiki 回答並附出處。
值得留下的答案，經我同意後存成比較頁或概念頁。

### Lint（健檢）
`python3 scripts/lint.py` 會檢查：
- 開頭欄位齊全（type、title、sources、updated）
- 頁面連結指向的檔案存在；沒有孤兒頁（每頁都列在 index.md，且至少被一頁連到）
- 含數字的段落有 `[@slug, ...]` 出處；引用的 slug 在 `raw/papers/` 存在
- 數字能在被引用論文的 txt 裡找到
- 有 ⚠ 區塊的頁面，log.md 有對應紀錄
lint 沒過就修，修不了的寫進 log.md 並告訴我。

## 10. 不能做的事

- 不改 `raw/` 裡的任何檔案。
- 不用自己的知識補 wiki 內容；論文沒寫的就不寫。
- 不在 repo 放 API key、密碼、個資。
- 未經我同意，不刪除既有 wiki 頁面、不改這份手冊。

## 11. 完成檢查清單（每次改完 wiki 都要對一次）

- [ ] 新頁面開頭欄位齊全
- [ ] 每個數字、關鍵說法都有出處
- [ ] index.md、log.md 已更新
- [ ] `python3 scripts/lint.py` 全部通過
- [ ] 已 commit
