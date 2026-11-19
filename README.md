# AI Agents 論文 LLM Wiki

依 Karpathy 的 LLM Wiki 構想，把 6 篇 AI Agents 經典論文整理成可以持續累積的知識庫，再**只用這份 Wiki** 產生一份教學簡報「AI Agents 是什麼？」，對象是用過 ChatGPT 的大學生。

- 📽 **教學簡報**：https://dipo221.github.io/agent-llm-wiki/slides/ （右上角可以切換 3 種風格；← → 換頁）
- 📚 **Wiki 目錄**：[`wiki/index.md`](wiki/index.md)
- 🔀 **簡報 workflow（graph）與反思**：[`docs/workflow-design.md`](docs/workflow-design.md)
- 🧾 **一次實際執行的檢查紀錄**：[`runs/ai-agents-intro/report.md`](runs/ai-agents-intro/report.md)

## 收錄的論文（6 篇）

| 論文 | Wiki 頁 |
|---|---|
| Wei et al. 2022 — Chain-of-Thought Prompting | [papers/wei2022-chain-of-thought](wiki/papers/wei2022-chain-of-thought.md) |
| Yao et al. 2022 — ReAct | [papers/yao2022-react](wiki/papers/yao2022-react.md) |
| Schick et al. 2023 — Toolformer | [papers/schick2023-toolformer](wiki/papers/schick2023-toolformer.md) |
| Shinn et al. 2023 — Reflexion | [papers/shinn2023-reflexion](wiki/papers/shinn2023-reflexion.md) |
| Park et al. 2023 — Generative Agents | [papers/park2023-generative-agents](wiki/papers/park2023-generative-agents.md) |
| Wang et al. 2023 — A Survey on LLM-based Autonomous Agents | [papers/wang2023-agent-survey](wiki/papers/wang2023-agent-survey.md) |

另有 7 個概念頁、2 個比較頁、7 個 Benchmark 頁，共 22 頁。每個數字都標了論文章節或表號，並由 `scripts/lint.py` 對照原文逐字比對。

## 怎麼做出來的

1. **先討論、後生成**：AI 先一次問一題，問完 10 題後整理成需求摘要，我確認後才寫 [`AGENTS.md`](AGENTS.md)。訪談紀錄見 [`docs/interview.md`](docs/interview.md)。
2. **Ingest**：先試做 2 篇並 commit，確認沒問題後再一篇一篇補完（一篇一個 commit）。每次 ingest 都跑 lint，紀錄寫在 [`wiki/log.md`](wiki/log.md)。
3. **簡報 workflow**：檢索 → 證據卡 → 大綱 → 人工確認 → 逐頁稿 → 程式渲染。中間共有 5 道檢查關卡，其中 1 道由人確認大綱，其他用腳本、Chrome 量測或 AI 審查。說明見 [`workflows/topic-slides.md`](workflows/topic-slides.md)。

## 資料夾

```
AGENTS.md / CLAUDE.md   Wiki 手冊（CLAUDE.md 只有 @AGENTS.md）
raw/papers/             原始論文 PDF ＋ pdftotext 轉出的 txt（只讀）
wiki/                   index.md、log.md、papers/、concepts/、comparisons/、benchmarks/
workflows/              簡報 workflow 定義
scripts/                lint.py、G1–G5 檢查腳本、render_deck.py（渲染）、measure.py（Chrome 量測）
runs/ai-agents-intro/   一次執行的中間產物：sources、cards、outline、drafts、reviews、screenshots、report
slides/                 簡報模板、自己畫的 SVG 圖、index.html（成品）
docs/                   訪談紀錄、workflow 設計與反思
```

## 常用指令

```bash
python3 scripts/lint.py                               # Wiki 健檢
python3 scripts/g4_drafts.py runs/ai-agents-intro     # 逐頁稿忠實度＋版面量測（需要 Chrome）
python3 scripts/render_deck.py runs/ai-agents-intro   # 產生 slides/index.html
python3 scripts/g5_render.py runs/ai-agents-intro     # 3 種風格渲染檢查＋截圖
```

## AI 使用說明

這份作業用 Claude Code（Claude Opus 5.5）完成。主題、論文、Wiki 規則、簡報對象與風格由我決定，大綱也經過我確認，反思由我自己回答。Wiki 頁面、腳本、簡報稿與圖由 AI 依規則產生，再經過腳本與 AI 審查檢查。論文著作權屬原作者，`raw/papers/` 只作為比對出處用。
