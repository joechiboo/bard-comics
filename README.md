# Bard Comics 莎劇漫畫

把經典文學做成漫畫的 side project。第一部：《馬克白》。

> 起心動念：小說大家不愛看，但故事本身不該被埋沒。

## 專案結構

```
scripts/      分鏡腳本（人讀的，Markdown）
storyboards/  分鏡資料（機器讀的，JSON：prompt + 對白）
tools/        產製 pipeline
cache/        單格生圖快取（自動生成，不進版控）
pages/        整頁成品 PNG（自動生成，不進版控）
```

## 產製流程

```
分鏡 JSON → OpenAI 生圖 (gpt-image-1) → Pillow 排版上對白 → 整頁 PNG → 人工校稿
```

### 快速開始

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-xxx        # Windows: set OPENAI_API_KEY=sk-xxx
python tools/generate_comic.py storyboards/macbeth_1_1.json
```

輸出在 `pages/`，直接校稿。

### 校稿迭代

改 `storyboards/*.json` 的 prompt 或 dialogue 後重跑——生圖以 prompt 雜湊快取，
**只有改過的格會重新生圖**；只改對白不改 prompt 則零生圖成本。

## 角色一致性約定

跨格辨識靠 prompt 內的固定特徵 token（定義在 JSON 的 `characters` 欄位）：

| 角色 | 特徵 |
|---|---|
| 女巫甲 | 獨眼 (single eye) |
| 女巫乙 | 裂嘴笑 (torn grinning mouth) |
| 女巫丙 | 白瞳 (pale white pupils) |

## 進度

- [x] 馬克白 1-1 荒野女巫：分鏡腳本 + JSON + pipeline
- [ ] 馬克白 1-1：首輪生圖與校稿
- [ ] 馬克白 1-2 戰報
- [ ] 對白框氣泡樣式優化（尾巴指向說話者）

## 譯文版權備忘

莎劇原文為公版；本專案對白為自行改寫之譯文。
朱生豪譯本（1944 年逝世）已屬公版可參考；梁實秋譯本仍在版權期內，勿直接引用。
