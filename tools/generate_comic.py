# -*- coding: utf-8 -*-
"""
漫畫產製 pipeline：分鏡 JSON → 生圖 API → 自動排版上對白 → 整頁 PNG
支援三個生圖供應商（環境變數 COMIC_PROVIDER 切換，預設 pollinations）：
  pollinations Pollinations.ai，完全免費、零註冊零 key，適合迭代分鏡與排版
  gemini       Google Gemini (gemini-2.5-flash-image)，需 GEMINI_API_KEY＋開帳單
               （2026-07 起免費層生圖額度已收掉，見 README）
  openai       OpenAI gpt-image-1，付費，需 OPENAI_API_KEY
用法：
  1. pip install requests pillow
  2. python generate_comic.py storyboards/macbeth_1_1.json   ← 零設定直接跑
     定稿出正式圖：set COMIC_PROVIDER=gemini + GEMINI_API_KEY=xxx
輸出：
  pages/page_01.png ...   （整頁成品，直接校稿）
  cache/<hash>.png        （單格原圖快取；prompt 沒改就不會重生，省錢）
校稿迭代：改 JSON 裡的 prompt 或 dialogue → 重跑 → 只有改過的格會重新生圖
"""
import json, os, re, sys, hashlib, base64, math, time
from io import BytesIO
from pathlib import Path
from urllib.parse import quote as urlquote

import requests
from PIL import Image, ImageDraw, ImageFont

# ---------- 設定 ----------
PROVIDER = os.environ.get("COMIC_PROVIDER", "pollinations")  # pollinations / gemini / openai
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash-image"
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-image-1"
OPENAI_QUALITY = "medium"     # low / medium / high，先用 medium 試
PAGE_W, PAGE_H = 1240, 1754   # A4 直式 @150dpi
MARGIN, GUTTER = 48, 28
# 中文字型：Windows 預設微軟正黑；mac 可改 /System/Library/Fonts/PingFang.ttc
FONT_CANDIDATES = [
    os.environ.get("COMIC_FONT", ""),
    r"C:\Windows\Fonts\msjh.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]

CACHE = Path("cache"); CACHE.mkdir(exist_ok=True)
OUT = Path("pages"); OUT.mkdir(exist_ok=True)


def load_font(size):
    for p in FONT_CANDIDATES:
        if p and Path(p).exists():
            return ImageFont.truetype(p, size)
    print("!! 找不到中文字型，對白會變豆腐字。請設環境變數 COMIC_FONT 指向 .ttc/.ttf")
    return ImageFont.load_default()


# ---------- 生圖供應商 ----------
RETRYABLE = {429, 500, 502, 503, 504}


def http_retry(fn, tries=4):
    """免費額度常見 429/暫時性 5xx，退避重試；其他錯誤直接終止"""
    for i in range(tries):
        try:
            r = fn()
        except (requests.ConnectionError, requests.Timeout) as e:
            err = type(e).__name__
        else:
            if r.ok:
                return r
            if r.status_code not in RETRYABLE:
                sys.exit(f"API 錯誤 {r.status_code}：{r.text[:300]}")
            err = f"HTTP {r.status_code}"
        if i == tries - 1:
            sys.exit(f"重試 {tries} 次仍失敗：{err}")
        wait = 10 * (i + 1)
        print(f"    [retry] {err}，{wait}s 後重試...")
        time.sleep(wait)


# Gemini 用長寬比而非固定尺寸，挑最接近格子的，減少 cover_crop 裁切損失
GEMINI_RATIOS = {"21:9": 21 / 9, "16:9": 16 / 9, "3:2": 1.5, "4:3": 4 / 3,
                 "1:1": 1.0, "3:4": 0.75, "2:3": 2 / 3, "9:16": 9 / 16}


def pick_ratio(w, h):
    r = w / h
    return min(GEMINI_RATIOS, key=lambda k: abs(math.log(GEMINI_RATIOS[k] / r)))


def gen_gemini(prompt, ratio):
    r = http_retry(lambda: requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent",
        headers={"x-goog-api-key": GEMINI_KEY},
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "imageConfig": {"aspectRatio": ratio},
            },
        },
        timeout=300,
    ))
    for part in r.json()["candidates"][0]["content"]["parts"]:
        data = part.get("inlineData", {}).get("data")
        if data:
            return Image.open(BytesIO(base64.b64decode(data)))
    sys.exit("Gemini 沒有回傳圖片：" + json.dumps(r.json(), ensure_ascii=False)[:300])


def gen_pollinations(prompt, w, h):
    scale = min(1.0, 1280 / max(w, h))  # 免費服務別要太大張
    url = "https://image.pollinations.ai/prompt/" + urlquote(prompt[:1500], safe="")
    r = http_retry(lambda: requests.get(
        url,
        params={"width": int(w * scale), "height": int(h * scale),
                "nologo": "true", "model": "flux", "seed": 42},
        timeout=300,
    ))
    return Image.open(BytesIO(r.content))


def pick_size(panel_w, panel_h):
    """OpenAI 只支援三種固定尺寸，依格子長寬比選"""
    ratio = panel_w / panel_h
    if ratio > 1.25:
        return "1536x1024"
    if ratio < 0.8:
        return "1024x1536"
    return "1024x1024"


def gen_openai(prompt, api_size):
    r = http_retry(lambda: requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={"Authorization": f"Bearer {OPENAI_KEY}"},
        json={"model": OPENAI_MODEL, "prompt": prompt,
              "size": api_size, "quality": OPENAI_QUALITY},
        timeout=300,
    ))
    return Image.open(BytesIO(base64.b64decode(r.json()["data"][0]["b64_json"])))


def gen_panel(prompt, w, h):
    """依 PROVIDER 生圖，帶快取"""
    if PROVIDER == "gemini":
        variant = pick_ratio(w, h)
    elif PROVIDER == "openai":
        variant = f"{pick_size(w, h)}|{OPENAI_QUALITY}"
    else:
        variant = f"{w}x{h}"
    key = hashlib.sha1(f"{PROVIDER}|{variant}|{prompt}".encode()).hexdigest()
    cached = CACHE / f"{key}.png"
    if cached.exists():
        print(f"    [cache] {prompt[:50]}...")
        return Image.open(cached)
    print(f"    [ gen ] ({PROVIDER}) {prompt[:50]}...")
    if PROVIDER == "gemini":
        img = gen_gemini(prompt, variant)
    elif PROVIDER == "openai":
        img = gen_openai(prompt, pick_size(w, h))
    elif PROVIDER == "pollinations":
        img = gen_pollinations(prompt, w, h)
    else:
        sys.exit(f"不認識的 COMIC_PROVIDER：{PROVIDER}（gemini / pollinations / openai）")
    img.save(cached)
    return img


def cover_crop(img, w, h):
    """把生圖裁滿格子（等比放大後置中裁切）"""
    scale = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * scale) + 1, int(img.height * scale) + 1))
    x = (img.width - w) // 2
    y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def wrap_cjk(text, font, max_w, draw):
    """逐字換行（CJK 適用）"""
    lines, line = [], ""
    for ch in text:
        if draw.textlength(line + ch, font=font) <= max_w:
            line += ch
        else:
            lines.append(line); line = ch
    if line:
        lines.append(line)
    return lines


def draw_dialogue(page_img, box, dialogues):
    """在格子底部畫對白框"""
    if not dialogues:
        return
    d = ImageDraw.Draw(page_img)
    x0, y0, x1, y1 = box
    font = load_font(26)
    name_font = load_font(22)
    pad, inner_w = 14, (x1 - x0) - 2 * 24 - 2 * 14

    # 由下往上疊
    cursor = y1 - 16
    for item in reversed(dialogues):
        speaker, text = item.get("speaker", ""), item["text"]
        lines = wrap_cjk(text, font, inner_w, d)
        line_h = 34
        h = pad * 2 + len(lines) * line_h + (26 if speaker else 0)
        bx0, bx1 = x0 + 24, x1 - 24
        by1, by0 = cursor, cursor - h
        d.rounded_rectangle([bx0, by0, bx1, by1], radius=10,
                            fill="white", outline="black", width=3)
        ty = by0 + pad
        if speaker:
            d.text((bx0 + pad, ty), speaker + "：", font=name_font, fill="black")
            ty += 26
        for ln in lines:
            d.text((bx0 + pad, ty), ln, font=font, fill="black")
            ty += line_h
        cursor = by0 - 10


def draw_quote(page_img, box, quote):
    """經典台詞：中文直排置右（欄由右往左），英文原文轉 90° 沿中文欄左側並列"""
    if not quote:
        return
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(page_img)
    pad, char_size, char_h, col_gap = 28, 44, 54, 16
    font = load_font(char_size)
    max_chars = max(1, ((y1 - y0) - 2 * pad) // char_h)

    # 依標點斷欄（對聯式直排），過長的句子再截欄
    phrases = [s for s in re.split(r"[，。、；：—\s]+", quote.get("text", "")) if s]
    cols = []
    for ph in phrases:
        cols += [ph[i:i + max_chars] for i in range(0, len(ph), max_chars)]

    left = x1 - pad
    for col in cols:
        left -= char_size
        cy = y0 + pad
        for ch in col:
            d.text((left, cy), ch, font=font, fill="white",
                   stroke_width=3, stroke_fill="black")
            cy += char_h
        left -= col_gap

    en = quote.get("en", "")
    if en:
        en_font = load_font(24)
        tw = int(d.textlength(en, font=en_font))
        tmp = Image.new("RGBA", (tw + 12, 40), (0, 0, 0, 0))
        ImageDraw.Draw(tmp).text((6, 4), en, font=en_font, fill="white",
                                 stroke_width=2, stroke_fill="black")
        tmp = tmp.rotate(-90, expand=True)  # 順時針轉，由上往下讀（書背方向）
        page_img.paste(tmp, (left - tmp.width, y0 + pad), tmp)


def build_page(page_def, style_suffix, characters):
    page_img = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    d = ImageDraw.Draw(page_img)
    panels = page_def["panels"]
    total_w = sum(p.get("weight", 1) for p in panels)
    avail_h = PAGE_H - 2 * MARGIN - GUTTER * (len(panels) - 1)

    y = MARGIN
    for p in panels:
        h = int(avail_h * p.get("weight", 1) / total_w)
        w = PAGE_W - 2 * MARGIN
        prompt = p["prompt"].replace("{characters}", characters)
        prompt = f"comic panel, {prompt}, {style_suffix}"
        art = gen_panel(prompt, w, h)
        page_img.paste(cover_crop(art, w, h), (MARGIN, y))
        d.rectangle([MARGIN, y, MARGIN + w, y + h], outline="black", width=4)
        draw_dialogue(page_img, (MARGIN, y, MARGIN + w, y + h), p.get("dialogue", []))
        draw_quote(page_img, (MARGIN, y, MARGIN + w, y + h), p.get("quote"))
        y += h + GUTTER
    return page_img


def main():
    if PROVIDER == "gemini" and not GEMINI_KEY:
        sys.exit("請先設定 GEMINI_API_KEY（https://aistudio.google.com 免費申請），"
                 "或 set COMIC_PROVIDER=pollinations 走零 key 備案")
    if PROVIDER == "openai" and not OPENAI_KEY:
        sys.exit("請先設定環境變數 OPENAI_API_KEY")
    sb_path = sys.argv[1] if len(sys.argv) > 1 else "storyboards/macbeth_1_1.json"
    sb = json.loads(Path(sb_path).read_text(encoding="utf-8"))
    print(f"== {sb['title']} ({PROVIDER}) ==")
    scene = Path(sb_path).stem  # 檔名帶場次前綴，多場輸出才不互蓋
    for page_def in sb["pages"]:
        n = page_def["page"]
        print(f"[Page {n}]")
        img = build_page(page_def, sb.get("style_suffix", ""), sb.get("characters", ""))
        out = OUT / f"{scene}_page_{n:02d}.png"
        img.save(out)
        print(f"    -> {out}")
    print("完成，去 pages/ 資料夾校稿。")


if __name__ == "__main__":
    main()
