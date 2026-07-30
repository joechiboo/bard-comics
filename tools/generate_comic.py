# -*- coding: utf-8 -*-
"""
漫畫產製 pipeline：分鏡 JSON → OpenAI 生圖 → 自動排版上對白 → 整頁 PNG
用法：
  1. pip install requests pillow
  2. set OPENAI_API_KEY=sk-xxx   (Windows) / export OPENAI_API_KEY=sk-xxx (mac/linux)
  3. python generate_comic.py storyboard_act1_scene1.json
輸出：
  pages/page_01.png ...   （整頁成品，直接校稿）
  cache/<hash>.png        （單格原圖快取；prompt 沒改就不會重生，省錢）
校稿迭代：改 JSON 裡的 prompt 或 dialogue → 重跑 → 只有改過的格會重新生圖
"""
import json, os, sys, hashlib, base64
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

# ---------- 設定 ----------
API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-image-1"
QUALITY = "medium"            # low / medium / high，先用 medium 試
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


def pick_size(panel_w, panel_h):
    """依格子長寬比選 API 支援的尺寸"""
    ratio = panel_w / panel_h
    if ratio > 1.25:
        return "1536x1024"
    if ratio < 0.8:
        return "1024x1536"
    return "1024x1024"


def gen_panel(prompt, api_size):
    """呼叫 OpenAI 生圖，帶快取"""
    key = hashlib.sha1(f"{MODEL}|{QUALITY}|{api_size}|{prompt}".encode()).hexdigest()
    cached = CACHE / f"{key}.png"
    if cached.exists():
        print(f"    [cache] {prompt[:50]}...")
        return Image.open(cached)
    print(f"    [ gen ] {prompt[:50]}...")
    r = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "prompt": prompt, "size": api_size, "quality": QUALITY},
        timeout=300,
    )
    r.raise_for_status()
    img = Image.open(BytesIO(base64.b64decode(r.json()["data"][0]["b64_json"])))
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
        art = gen_panel(prompt, pick_size(w, h))
        page_img.paste(cover_crop(art, w, h), (MARGIN, y))
        d.rectangle([MARGIN, y, MARGIN + w, y + h], outline="black", width=4)
        draw_dialogue(page_img, (MARGIN, y, MARGIN + w, y + h), p.get("dialogue", []))
        y += h + GUTTER
    return page_img


def main():
    if not API_KEY:
        sys.exit("請先設定環境變數 OPENAI_API_KEY")
    sb_path = sys.argv[1] if len(sys.argv) > 1 else "storyboard_act1_scene1.json"
    sb = json.loads(Path(sb_path).read_text(encoding="utf-8"))
    print(f"== {sb['title']} ==")
    for page_def in sb["pages"]:
        n = page_def["page"]
        print(f"[Page {n}]")
        img = build_page(page_def, sb.get("style_suffix", ""), sb.get("characters", ""))
        out = OUT / f"page_{n:02d}.png"
        img.save(out)
        print(f"    -> {out}")
    print("完成，去 pages/ 資料夾校稿。")


if __name__ == "__main__":
    main()
