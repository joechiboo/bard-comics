# -*- coding: utf-8 -*-
"""從分鏡 JSON 生成對照劇本頁（中文白話改寫 × 莎翁英文原文）
用法：python tools/generate_script_page.py storyboards/macbeth_1_1.json shakespeare/macbeth/1-1
輸出：<場次目錄>/script.html，閱讀頁旁的「對照劇本」入口自行加連結
台詞底本：朱生豪譯本（公版）改寫；英文為莎士比亞原文（公版）。
"""
import json, sys, html
from pathlib import Path

TPL_HEAD = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} 對照劇本 — Bard Comics</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Noto+Serif+TC:wght@400;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/style.css?v=2">
  <link rel="stylesheet" href="{prefix}assets/script.css">
</head>
<body>
  <main>
    <nav class="crumbs"><a href="{prefix}">BARD COMICS</a> ／ <a href="{prefix}shakespeare/">莎士比亞戲劇</a> ／ <a href="../">{play}</a> ／ <a href="./">{short}</a> ／ 劇本</nav>
    <header class="masthead">
      <p class="house">The Script</p>
      <h1>{short}<span class="latin">Bilingual Script</span></h1>
      <div class="ornament">❦</div>
      <p class="tagline">中文為朱生豪公版譯本之白話改寫；英文為莎士比亞公版原文。</p>
    </header>
    <p class="script-back"><a href="./">← 回漫畫閱讀</a></p>
"""

TPL_FOOT = """  </main>
  <footer>
    <a href="https://github.com/joechiboo/bard-comics">GitHub</a>
  </footer>
</body>
</html>
"""


def build(sb_path, out_dir):
    sb = json.loads(Path(sb_path).read_text(encoding="utf-8"))
    title = sb["title"]                      # 例：馬克白 1-1 荒野女巫
    play = title.split(" ", 1)[0]            # 例：馬克白／哈姆雷特（麵包屑用）
    short = title.split(" ", 1)[1] if " " in title else title   # 例：1-1 荒野女巫
    prefix = "../" * 3                        # shakespeare/<play>/<scene>/ 固定三層
    parts = [TPL_HEAD.format(title=html.escape(title), short=html.escape(short),
                             play=html.escape(play), prefix=prefix)]

    for page in sb["pages"]:
        parts.append(f'    <section class="script-page">\n')
        parts.append(f'      <h2 class="script-page-no">— 第 {page["page"]} 頁 —</h2>\n')
        for panel in page["panels"]:
            for d in panel.get("dialogue", []):
                sp = html.escape(d.get("speaker", ""))
                zh = html.escape(d["text"])
                en = html.escape(d.get("en", ""))
                parts.append('      <div class="line">\n')
                if sp:
                    parts.append(f'        <p class="speaker">{sp}</p>\n')
                parts.append(f'        <p class="zh">{zh}</p>\n')
                if en:
                    parts.append(f'        <p class="en">{en}</p>\n')
                parts.append('      </div>\n')
            q = panel.get("quote")
            if q:
                parts.append('      <blockquote class="script-quote">\n')
                parts.append(f'        <p class="zh">{html.escape(q["text"])}</p>\n')
                if q.get("en"):
                    parts.append(f'        <p class="en">{html.escape(q["en"])}</p>\n')
                parts.append('      </blockquote>\n')
        parts.append('    </section>\n')

    parts.append(TPL_FOOT)
    out = Path(out_dir) / "script.html"
    out.write_text("".join(parts), encoding="utf-8", newline="\n")
    print(f"-> {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("用法：python tools/generate_script_page.py <storyboard.json> <場次目錄>")
    build(sys.argv[1], sys.argv[2])
