# 角色特徵 token（跨場一致性canon）

生圖漫畫的角色一致性靠 prompt 裡的固定特徵 token。**同一角色在所有分鏡 JSON 裡必須逐字使用同一段英文描述**——改動會讓快取失效、跨場長相飄移。新增角色先在這裡定案再進分鏡。一劇一節，各劇風格與特許色也在該節定案。

## 馬克白 Macbeth

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

### 全劇風格（馬克白）

- `style_suffix`：`black and white ink comic style, high contrast, heavy shadows, dark fantasy atmosphere`（黑白水墨、全劇統一）
- 紅色是全劇唯一特許色，留給血／戰旗／王冠等關鍵物件的單點強調。

## 哈姆雷特 Hamlet

人名採台灣慣用譯名（見 docs/text-sources.md 對照表）。

| 角色 | 特徵 token（進 prompt 的原文） | 視覺錨點 | 首次登場 |
| --- | --- | --- | --- |
| 老王鬼魂 | `the Ghost of old King Hamlet, a towering spectral king in full plate armour with the visor raised, a long grey beard, hollow eyes, a faint cold blue glow around his translucent form` | 掀面甲全甲＋幽藍冷光 | 1-1 |
| 霍拉旭 | `Horatio, a sober young scholar in a plain dark scholar's gown with a high collar, short neatly combed brown hair, a small leather book at his belt` | 高領學袍＋腰間小書 | 1-1 |
| 哈姆雷特 | `Hamlet, a lean young prince dressed head to toe in black, a short dark cloak, tousled dark hair, pale clean-shaven face with shadowed sleepless eyes` | 全身黑衣＋失眠黑眼圈 | 1-2 |
| 克勞地 | `King Claudius, a broad heavyset king with a neatly trimmed dark pointed beard, a wide gold crown, fur-trimmed brocade robes, a jeweled goblet in hand` | 尖鬚金冠＋不離手的酒杯 | 1-2 |
| 葛簇特 | `Queen Gertrude, a stately middle-aged queen with coiled auburn braids under a golden circlet, in a layered brocade gown` | 赭紅盤辮 | 1-2 |
| 波隆尼 | `Polonius, a stooped elderly councillor with a long forked white beard, a heavy chain of office over dark robes, a rolled parchment in his sash` | 分叉白鬚＋官鏈 | 1-2（主戲在 1-3） |
| 雷歐提斯 | `Laertes, a hot-blooded young nobleman with short dark curls and a thin moustache, a slender rapier at his hip, a short travel cloak` | 短捲髮＋腰間細劍 | 1-3 |
| 奧菲莉亞 | `Ophelia, a slight young woman with very long loose fair hair, wide gentle eyes, in a simple pale flowing gown` | 及腰散髮淡色長裙 | 1-3 |

### 全劇風格（哈姆雷特）

- `style_suffix`：`black and white ink comic style, high contrast, heavy shadows, cold gothic atmosphere`
  （黑白水墨同 pipeline，氣氛從 dark fantasy 改 cold gothic——石牆、海霧、垂直線條）
- **特許色改幽藍**（`faint cold blue glow`）：留給鬼魂冷光與毒藥，與馬克白的紅明確區隔。
  紅色在本劇不使用，全劇黑白＋單點幽藍。
- 城牆戲（1-1、1-4to5）統一意象：海霧、垛口、遠處城堡燈火——與宮廷戲的燭光暖調對比。

## 使用方式

- 該場最常出鏡的角色（或「整組同場」如三女巫）放 JSON 頂層 `characters` 欄位，prompt 用 `{characters}` 引用。
- 其他角色誰出場誰的 token 就完整貼進該格 prompt（複製表格第二欄原文，不要改寫）。
- 一次性角色（如馬克白 1-2 的流血軍曹、哈姆雷特 1-1 的守夜士兵）在該場 JSON 內自行保持一致即可，不進 canon。
- 站上讀者也靠這些視覺錨點認人：劇目頁（`shakespeare/<play>/index.html`）的「登場人物 Dramatis Personae」與各場次頁的「本場人物」角註（`.cast-strip`）都引用本表的錨點。canon 改動（含帽子這類待決項定案）時同步更新；新場次刊出頁記得帶上該場的角註。
