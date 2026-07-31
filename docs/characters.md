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

## 李爾王 King Lear

人名採台灣慣用譯名（見 docs/text-sources.md 對照表）。李爾的袍服與王冠隨劇情剝落，
不進 token——token 只鎖臉部特徵，衣著逐場在 prompt 內指定。

| 角色 | 特徵 token（進 prompt 的原文） | 視覺錨點 | 首次登場 |
| --- | --- | --- | --- |
| 李爾 | `King Lear, a mighty old king with a wild mane of white hair, a long white beard, deep-lined imperious face, fierce hawk-like eyes` | 白髮鬃獅 | 1-1 |
| 高納里爾 | `Goneril, a tall haughty duchess with dark hair under a severe jeweled headdress, cold narrow eyes, a high-collared black and gold gown` | 高聳珠冠冷眼 | 1-1 |
| 里根 | `Regan, a sharp-faced smiling duchess with auburn hair in twin coiled braids, a fox-fur stole around her shoulders` | 狐裘雙辮假笑 | 1-1 |
| 寇蒂莉亞 | `Cordelia, a young princess with soft wavy fair hair loose over her shoulders, clear steady eyes, in a plain white gown with no jewels` | 素白無飾 | 1-1 |
| 肯特 | `Earl of Kent, a solid grey-bearded nobleman with a weathered honest face, plain sturdy clothes and a broad sword belt` | 灰鬚寬劍帶 | 1-1 |
| 葛羅斯特 | `Earl of Gloucester, a stout old courtier with a short white beard, a rich chain of office, leaning on a walking staff` | 官鏈手杖 | 1-1 |
| 愛德蒙 | `Edmund, a handsome young man with slicked black hair and a trim pointed beard, a half-smile that never reaches his eyes, a fine dark doublet` | 油亮黑髮半笑 | 1-1 |
| 愛德加 | `Edgar, an earnest young nobleman with curly brown hair and an open honest face, in plain riding clothes` | 棕捲髮憨直 | 1-2（瘋乞丐湯姆造型逐場另述） |
| 弄人 | `the Fool, a small wiry jester in a patched motley coat and a drooping three-pointed cap with tiny bells, sad knowing eyes` | 三角鈴帽悲眼 | 1-3 |

### 全劇風格（李爾王）

- `style_suffix`：`black and white ink comic style, high contrast, heavy shadows, bleak windswept atmosphere`
- **無特許色**：四大悲劇中唯一純黑白的一部——荒野、暴風雨、白髮，最亮的白留給閃電。
  刻意與馬克白（紅）、哈姆雷特（幽藍）、奧賽羅（綠）區隔。

## 奧賽羅 Othello

人名採台灣慣用譯名（見 docs/text-sources.md 對照表）。

| 角色 | 特徵 token（進 prompt 的原文） | 視覺錨點 | 首次登場 |
| --- | --- | --- | --- |
| 奧賽羅 | `Othello, a powerful Moorish general with deep brown skin, a shaved head, a short grizzled black beard, a single gold hoop earring, a curved scimitar at his hip` | 光頭金耳環彎刀 | 1-1 |
| 伊阿古 | `Iago, a lean soldier with cropped sandy hair, a neat short beard, hooded watchful eyes, in a plain buff military jerkin` | 低垂眼皮 | 1-1 |
| 黛絲德夢娜 | `Desdemona, a graceful young Venetian lady with long golden hair in a loose braid, gentle bright eyes, in a pale silk gown with a delicate lace collar` | 金髮鬆辮蕾絲領 | 1-2（元老院） |
| 卡西歐 | `Cassio, a handsome young Florentine officer, clean-shaven with wavy chestnut hair, an elegant half-cape and a rapier` | 俊秀半披風 | 1-2 |
| 羅德利哥 | `Roderigo, a foppish rich young Venetian with limp curled hair, a drooping feather in his cap, a perpetually anxious face` | 垂羽帽苦臉 | 1-1 |
| 勃拉班修 | `Brabantio, an old Venetian senator with thin white hair under a black cap, a dark damask robe with a heavy gold chain` | 黑帽金鏈 | 1-1 |
| 愛米莉霞 | `Emilia, a practical middle-aged woman with brown hair pinned under a linen coif, a ring of household keys at her waist` | 亞麻頭巾鑰匙串 | 3-x（手帕） |

### 全劇風格（奧賽羅）

- `style_suffix`：`black and white ink comic style, high contrast, heavy shadows, Venetian chiaroscuro atmosphere`
  （威尼斯／賽普勒斯的強烈明暗——運河夜色、火把、白牆烈日）
- **特許色綠**（`a sickly green tint`）：「綠眼的妖魔」＝嫉妒。只用在伊阿古毒語入耳、
  奧賽羅妒火發作的格；手帕等關鍵物件維持黑白強調。

## 使用方式

- 該場最常出鏡的角色（或「整組同場」如三女巫）放 JSON 頂層 `characters` 欄位，prompt 用 `{characters}` 引用。
- 其他角色誰出場誰的 token 就完整貼進該格 prompt（複製表格第二欄原文，不要改寫）。
- 一次性角色（如馬克白 1-2 的流血軍曹、哈姆雷特 1-1 的守夜士兵）在該場 JSON 內自行保持一致即可，不進 canon。
- 站上讀者也靠這些視覺錨點認人：劇目頁（`shakespeare/<play>/index.html`）的「登場人物 Dramatis Personae」與各場次頁的「本場人物」角註（`.cast-strip`）都引用本表的錨點。canon 改動（含帽子這類待決項定案）時同步更新；新場次刊出頁記得帶上該場的角註。
