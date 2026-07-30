# Bard Comics 經典文學漫畫

把經典文學做成漫畫的 side project。從莎劇起頭，第一部：《馬克白》。

> 起心動念：小說大家不愛看，但故事本身不該被埋沒。

## 專案緣起

原本只是個讀書計畫（四大奇書、世說新語，後來把莎劇也加進清單），
讀著讀著發現：這些故事本身很好看，只是「小說」這個形式大家不愛啃——那就改成漫畫。

**為什麼從莎劇開始**：原文早已公版、劇本天生就是「對白＋場景」結構，幾乎不用改編就能直接轉分鏡，戲劇衝突強、畫面感足。
**為什麼第一部是《馬克白》**：莎劇裡最短、情節最緊湊、視覺元素最強（女巫、血、幻象、黑暗城堡），改漫畫最不吃力。

**MVP 策略**：不一開始就畫整部，先挑《馬克白》最經典的幾場——女巫預言、弒君之夜、夫人夢遊、最終決戰——每場做成 4-8 頁短漫，用這個量驗證產製流程（腳本 → 分鏡 → 生圖 → 排版上字 → 校稿）。

## 選題路線

1. **莎劇**（進行中）：馬克白 → 哈姆雷特、李爾王、仲夏夜之夢等代表作
2. **世說新語**：每則本來就是獨立小故事，適合 4 格/單頁短漫
3. **四大奇書**：三國演義、水滸傳、西遊記、金瓶梅（長篇，流程成熟後再上）
4. **金庸**（構想）：版權仍在保護期，需另行處理授權，見下方版權備忘

## 專案結構

```text
scripts/      分鏡腳本（人讀的，Markdown）
storyboards/  分鏡資料（機器讀的，JSON：prompt + 對白）
tools/        產製 pipeline
cache/        單格生圖快取（自動生成，不進版控）
pages/        整頁成品 PNG（自動生成，不進版控）
```

## 產製流程

```text
分鏡 JSON → 生圖 API（三供應商擇一）→ Pillow 排版上對白 → 整頁 PNG → 人工校稿
```

生圖供應商用環境變數 `COMIC_PROVIDER` 切換：

| Provider | 費用 | 現況（2026-07 實測） |
| --- | --- | --- |
| `gemini` | 需開帳單，約 $0.039/張 | ⚠️ 免費層生圖額度已收掉：新專案打 `gemini-2.5-flash-image` / `gemini-3.1-flash-image` 一律 429 且 `limit: 0`。網路上「免費 500 張/天」是舊聞。key 本身有效，開帳單（Tier 1）即可用 |
| `pollinations`（預設） | 免費、零 key | ✅ 可用，畫質與角色一致性較差，適合校分鏡與排版 |
| `openai` | 付費，$0.04–0.06/張 | 可用，需 `OPENAI_API_KEY` |

**目前策略**：先用 `pollinations` 迭代分鏡與排版，定稿要出正式圖再幫 Google 專案開帳單走 `gemini`。

### 快速開始

```bash
pip install -r requirements.txt

# 免費路線（目前預設走法）
set COMIC_PROVIDER=pollinations     # mac/linux: export COMIC_PROVIDER=pollinations
python tools/generate_comic.py storyboards/macbeth_1_1.json

# Gemini 路線（需先在 Google 專案開帳單）
set GEMINI_API_KEY=xxx              # https://aistudio.google.com/apikey
python tools/generate_comic.py storyboards/macbeth_1_1.json
```

輸出在 `pages/`，直接校稿。

### 校稿迭代

改 `storyboards/*.json` 的 prompt 或 dialogue 後重跑——生圖以 prompt 雜湊快取，
**只有改過的格會重新生圖**；只改對白不改 prompt 則零生圖成本。

## 角色一致性約定

跨格辨識靠 prompt 內的固定特徵 token（定義在 JSON 的 `characters` 欄位）：

| 角色 | 特徵 |
| --- | --- |
| 女巫甲 | 獨眼 (single eye) |
| 女巫乙 | 裂嘴笑 (torn grinning mouth) |
| 女巫丙 | 白瞳 (pale white pupils) |

## 進度

- [x] 馬克白 1-1 荒野女巫：分鏡腳本 + JSON + pipeline
- [ ] 馬克白 1-1：首輪生圖與校稿
- [x] 馬克白 1-2 戰報：分鏡 JSON（待生圖）
- [ ] 馬克白 1-2：首輪生圖與校稿
- [x] 馬克白 1-3 女巫預言：分鏡 JSON（待生圖）
- [ ] 對白框氣泡樣式優化（尾巴指向說話者）

## 版權備忘

- **莎劇**：原文為公版；本專案對白為自行改寫之譯文。
  朱生豪譯本（1944 年逝世）已屬公版可參考；梁實秋譯本仍在版權期內，勿直接引用。
- **四大奇書、世說新語**：原文為公版，無版權疑慮；改寫白話對白時避免抄現代譯注本。
- **金庸**：作者 2018 年逝世，作品版權至 2068 年，**未經授權不可改編發布**；此線僅止於私人習作或先取得授權。
