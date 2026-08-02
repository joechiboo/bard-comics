# -*- coding: utf-8 -*-
"""角色介紹肖像生成：canon token → 直式肖像卡（劇目頁 Dramatis Personae 用）
用法：python tools/generate_cast_portraits.py cast/<play>_cast.json shakespeare/<play>/cast
設定檔格式：[{"file": "hamlet", "prompt": "<token＋肖像措辭>"}, ...]
與正篇相反：這裡「就是要臉」——肖像模式是特性不是 bug。鬼魂等無臉角色照 canon 給無臉肖像。
seed 固定 42，同 prompt 必得同圖；改 prompt 才會重生。
"""
import json, sys, time
from io import BytesIO
from pathlib import Path
from urllib.parse import quote as urlquote

import requests
from PIL import Image

W, H = 720, 960  # 3:4 直式肖像

def gen(prompt):
    url = ("https://image.pollinations.ai/prompt/" + urlquote(prompt[:1500], safe="")
           + f"?width={W}&height={H}&seed=42&nologo=true")
    for i in range(4):
        try:
            r = requests.get(url, timeout=180)
            if r.ok:
                return Image.open(BytesIO(r.content)).convert("RGB")
        except (requests.ConnectionError, requests.Timeout):
            pass
        time.sleep(10 * (i + 1))
    sys.exit("生圖失敗：" + prompt[:80])

def main():
    cfg_path, out_dir = sys.argv[1], Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    for item in json.loads(Path(cfg_path).read_text(encoding="utf-8")):
        out = out_dir / f"{item['file']}.jpg"
        img = gen(item["prompt"])
        img.save(out, "JPEG", quality=88)
        print("->", out)

if __name__ == "__main__":
    main()
