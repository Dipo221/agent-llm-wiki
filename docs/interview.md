# 建 Wiki 前的訪談紀錄（先討論、後生成）

日期：2026-11-17　工具：Claude Code（Claude Opus 5.5）

流程：先請 AI 解釋 LLM Wiki → AI 一次問一題（共 10 題，選項由 AI 提出、我選擇）→ AI 整理需求摘要 → 我確認後才建立 AGENTS.md 與資料夾。

## 問答

| # | AI 的問題 | 我的回答 |
|---|---|---|
| Q1 | 這個 LLM Wiki 要整理什麼主題？ | AI Agents 論文 |
| Q2 | Wiki 主要給誰看？（決定內容深度） | 自己研究用 |
| Q3 | 要 ingest 哪些論文？ | Agent 經典 6 篇：CoT、ReAct、Toolformer、Reflexion、Generative Agents、LLM-based Agents Survey |
| Q4 | 要有哪些頁面類型？ | 論文頁、概念頁、比較頁、Benchmark／資料集頁 |
| Q5 | 語言？技術名詞與數學式？ | 繁中內文＋英文術語，數學用 LaTeX |
| Q6 | 出處要標多細？ | 論文＋章節／表號 |
| Q7 | 論文說法不一致怎麼辦？ | 並列＋標註差異（⚠ 區塊，記入 log） |
| Q8 | Ingest 節奏？ | 先 1–2 篇試做，確認後再一篇一篇補 |
| Q9 | Lint 要檢查什麼？ | 連結與孤兒頁、出處覆蓋、數字對得回原文、格式與矛盾 |
| Q10 | 之後要產出什麼？ | 教學簡報「AI Agents 是什麼？」入門，給用過 ChatGPT 的大學生 |

## AI 額外提議、我確認採用的補充規則

- arXiv 連結由 AI 自行下載 PDF 到 `raw/papers/`，並轉成 `.txt` 供數字比對腳本使用；raw 只讀不改。
- 論文頁命名「第一作者＋年份＋方法名」（如 `yao2022-react`）；其他頁用英文 kebab-case。
- 每頁開頭欄位：type、sources、updated、related。
- Wiki 與簡報分層：wiki 可以技術，降低難度交給簡報流程。
- `CLAUDE.md` 只寫 `@AGENTS.md`，只維護一份手冊。
- 公開 repo `Dipo221/agent-llm-wiki`，簡報用 GitHub Pages。

## 和 Karpathy 原版不同／特別考量的地方

1. **讀者分層**：Karpathy 的 wiki 只服務查詢；這裡明確規定 wiki 給自己（技術），簡報給新手（白話），避免為了簡報把 wiki 改淺。
2. **數字可驗證**：原版只要求標出處；這裡要求數字跟原文「一字不差」，並保存 pdftotext 全文，讓 lint 腳本能自動比對。
3. **矛盾不下結論**：並列＋⚠ 區塊＋log 紀錄，而不是由 AI 判斷誰對。
4. **個人評論隔離**：自己的想法放在 `> 💭 筆記：` 區塊，簡報流程不可引用，確保簡報「只用論文說過的話」。
5. **Lint 寫成腳本**：原版的 lint 是請 LLM 讀一遍；這裡能用程式檢查的（連結、出處、數字）都改成腳本，LLM 只負責腳本做不到的部分。
