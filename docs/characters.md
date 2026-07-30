# 角色特徵 token（跨場一致性canon）

生圖漫畫的角色一致性靠 prompt 裡的固定特徵 token。**同一角色在所有分鏡 JSON 裡必須逐字使用同一段英文描述**——改動會讓快取失效、跨場長相飄移。新增角色先在這裡定案再進分鏡。

| 角色 | 特徵 token（進 prompt 的原文） | 視覺錨點 | 首次登場 |
| --- | --- | --- | --- |
| 女巫甲 | `witch one has a single eye` | 獨眼 | 1-1 |
| 女巫乙 | `witch two has a torn grinning mouth` | 裂嘴笑 | 1-1 |
| 女巫丙 | `witch three has pale white pupils` | 白瞳 | 1-1 |
| 馬克白 | `Macbeth, a broad-shouldered warrior in dark plate armor, shoulder-length black hair, short black beard, a pale diagonal scar across his left cheek` | 左頰斜疤 | 1-2（戰場回憶） |
| 鄧肯王 | `elderly King Duncan with a long white beard, gold crown, fur-trimmed deep blue robe` | 白鬚金冠藍袍 | 1-2 |
| 馬爾康 | `young prince Malcolm, clean-shaven, short fair hair, thin gold circlet` | 無鬚金髮細冠 | 1-2 |
| 班柯 | `Banquo, a sturdy warrior with a thick braided beard, a raven feather pinned at his shoulder` | 辮鬚＋肩上鴉羽 | 1-2（戰場回憶） |
| 洛斯 | `thane Ross, a gaunt middle-aged nobleman in a long travel-stained grey cloak` | 風塵灰斗篷 | 1-2 |
| 馬克白夫人 | `Lady Macbeth, a pale stately noblewoman with long straight black hair, piercing dark eyes, in a deep crimson gown with a high collar` | 深紅長袍（全劇唯一常駐紅色＝血的化身） | 1-5 |
| 麥克德夫 | `Macduff, a burly thane with a thick unkempt red-brown beard, a jagged boar-tusk pendant at his neck, in a weathered grey-green tartan cloak` | 紅褐亂鬚・野豬牙墜 | 2-3（MVP 線於 5-2~9 首登場） |

## 使用方式

- 三女巫這種「整組同場」的角色放 JSON 頂層 `characters` 欄位，prompt 用 `{characters}` 引用。
- 其他角色誰出場誰的 token 就完整貼進該格 prompt（複製表格第二欄原文，不要改寫）。
- 一次性角色（如 1-2 的流血軍曹）在該場 JSON 內自行保持一致即可，不進 canon。
- 站上讀者也靠這些視覺錨點認人：劇目頁（`shakespeare/macbeth/index.html`）的「登場人物 Dramatis Personae」與各場次頁的「本場人物」角註（`.cast-strip`）都引用本表的錨點。canon 改動（含帽子這類待決項定案）時同步更新；新場次刊出頁記得帶上該場的角註。

## 全劇風格

- `style_suffix`：`black and white ink comic style, high contrast, heavy shadows, dark fantasy atmosphere`（黑白水墨、全劇統一）
- 紅色是全劇唯一特許色，留給血／戰旗／王冠等關鍵物件的單點強調。
