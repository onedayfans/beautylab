# BeautyLab 課程網站 交接文件

更新日期：2026-08-20（Claude 本次 session 修改後的交接，上一版交接內容保留在下方「歷史記錄」）

---

## 基本資訊

| 項目 | 內容 |
|---|---|
| 網址 | https://beautylab.onedayfans.fans |
| Cloudflare Worker 名稱 | `beautylab-onedayfans` |
| Worker Account ID | `YOUR_ACCOUNT_ID` |
| Zone ID | `YOUR_ZONE_ID` |
| 原始 HTML 檔 | `/Users/vkmacstudio/.codex/visualizations/2026/08/05/019fd12f-6fdb-7380-9a99-6771ed593b39/beautylab.html` |
| 部署腳本資料夾 | `/private/tmp/claude-501/-Users-vkmacstudio/20302ef5-7526-4f3a-87c6-74193f860c69/scratchpad/beautylab-deploy/` |

**注意**：部署腳本資料夾在 `/private/tmp/claude-501/...` 下，是 Claude 的 session scratchpad，**不保證長期存在**（曾經在同一天內就被清空重建過）。如果該資料夾不存在，用下面「部署方式」章節裡的完整內容直接重建 `build_worker.py` 和 `wrangler.jsonc` 即可，兩個檔案都不長。

---

## 部署方式

HTML 內嵌在 Cloudflare Worker 的 `index.js` 裡，需要兩步驟。

### Step 1：build_worker.py

```python
import re, pathlib

HTML = pathlib.Path('/Users/vkmacstudio/.codex/visualizations/2026/08/05/019fd12f-6fdb-7380-9a99-6771ed593b39/beautylab.html').read_text(encoding='utf-8')

# escape for JS template literal
HTML = HTML.replace('\\', '\\\\')
HTML = HTML.replace('`', '\\`')
HTML = HTML.replace('${', '\\${')

JS = f"""export default {{
  async fetch(request, env, ctx) {{
    const html = `{HTML}`;
    return new Response(html, {{
      headers: {{ 'content-type': 'text/html;charset=UTF-8' }}
    }});
  }}
}};
"""

pathlib.Path('index.js').write_text(JS, encoding='utf-8')
print(f'index.js written ({len(JS):,} chars)')
```

執行：
```bash
cd /path/to/beautylab-deploy
python3 build_worker.py
```

### Step 2：wrangler.jsonc（同一個資料夾）

```json
{
  "name": "beautylab-onedayfans",
  "main": "index.js",
  "compatibility_date": "2026-08-01",
  "account_id": "YOUR_ACCOUNT_ID",
  "routes": [
    {
      "pattern": "beautylab.onedayfans.fans/*",
      "zone_id": "YOUR_ZONE_ID"
    }
  ]
}
```

### Step 3：部署

```bash
cd /path/to/beautylab-deploy
npx wrangler deploy
```

**重要**：每次修改 `beautylab.html` 後，三個步驟都要跑，否則 Worker 不會更新。部署完成後瀏覽器可能會快取舊版，測試時建議開新分頁或加 `?v=數字` 之類的 query string 強制重新抓。

---

## 網站架構（單一 HTML 檔，約 2378 行，~1.45MB）

依原始碼中出現順序：

```
beautylab.html
├── <head>                    全域 CSS 變數（--green, --coral, --gold, --ink, --muted, --line 等）
├── course-hero               Hero（課程 Logo 圖 + ChatGPT/Gemini/Manus QR code 三格 + 手機掃碼開啟卡）
├── wrap（website-lab 等）    第一個作品 LOGO MAKER + 第二個作品 WEBSITE LAB（7 步驟網站精靈）
├── script-entry / scriptModal   【本次新增】美妝短影音分鏡腳本產生器
├── gpb-entry / gpbModal         【本次新增】遊戲指令填空產生器
├── hst-section                  【本次新增】你適合哪種髮型？（隨機髮型抽抽樂）
├── </main><footer>           Footer
├── helper-section             工作小幫手（5 工具 AI 指令生成器，上次 session 完整重寫）
├── picku-showcase             PICKU 交友平台展示區（上次 session 新增）
└── <script>                  各工具各自獨立 IIFE，互不干擾
```

**注意**：`helper-section` 和 `picku-showcase` 這兩個 `<section>` 的 HTML 實際上位在 `</footer>` **之後**（原始碼行號 1974、2094，footer 在 1860）。這是歷史遺留的插入順序問題——不是本次造成的，瀏覽器渲染不受影響（`<footer>` 只是語意標籤，不強制要求在最後），視覺上顯示順序仍然正常，只是原始碼裡看起來 footer 卡在中間，日後如果要在這附近插入新區塊要注意用字串比對找正確位置，不要單純假設「footer 前面」＝「所有內容前面」。

---

## 本次 session 修改摘要（2026-08-20）

### A. Step 2 服務項目價格加 ±100 按鈕

`updPrices()` 產生的每一列價格輸入框，兩側加上 `−` / `＋` 按鈕（`class="price-adj"`, `data-service`, `data-delta`），用事件委派掛在 `#wPriceRows` 上，點擊會把對應 input 的數字 ±100，最小 0。

### B. Manus 邀請連結更新

全站 3 處（QR code + 兩個下載連結）從舊碼 `LFAAAVNLK0OXCR` 換成新碼 `0UMSHSY8E47H`，完整連結：
`https://manus.im/invitation/0UMSHSY8E47H?utm_source=invitation&utm_medium=social&utm_campaign=copy_link`

### C. PICKU 交友網站展示區（`picku-showcase`）

介紹使用者自己做的交友 APP（`https://pickup.onedayfans.fans/`），左側文字介紹（React+Flask、Cloudflare Pages、Railway、4 輪配對機制、24 位 AI 測試會員），右側用 `api.qrserver.com` 產生的 QR code 圖，可掃碼進入。

### D. 美妝短影音分鏡腳本產生器（`script-entry` / `#scriptModal`）— 新增大功能

全螢幕 Modal，6 步驟精靈：
1. 選產品類別（7 類：髮油/洗髮精/護髮素/造型品/染燙護理/頭皮護理/美髮工具）→ 選產品項目，也可載入 6 個範例
2. 填產品資訊（名稱、品牌、價格、使用時間、髮質、功效特色、優缺點、心得、來源）
3. 影片設定（用途、時長 30–120 秒、平台 IG Reels/TikTok/YouTube Shorts、風格、出鏡模式）
4. 選開頭（18 種模板，一次顯示 6 種可換一批）
5. 選結尾（13 種模板，一次顯示 6 種可換一批）
6. 生成結果：3 種腳本版本（A 自然聊天版／B 快速吸睛版／C 專業介紹版），每個場景卡片含景別/畫面/動作/鏡頭運動/旁白/字幕/拍攝提示/秒數，可複製完整腳本、只複製旁白、只複製 hashtags

核心邏輯：`SCENE_LIBS`（各產品類別的分鏡場景庫）+ `OPENINGS`/`ENDINGS`（開頭結尾模板庫）+ `generate()` 依時長算場景數、組出三種語氣變體。全部是內建規則生成，不呼叫任何 AI API，也不需要後端。

### E. 遊戲指令填空產生器（`gpb-entry` / `#gpbModal`）— 新增大功能

單頁表單＋右側即時預覽（不是分步驟精靈），教學生怎麼寫「請 AI 幫我做小遊戲」的完整指令。用途：使用者原本丟了 3 份自己寫給 Manus 的完整遊戲指令（美業接接樂基本版、限時+獎品版、美業記憶翻牌王），要求做成讓學生練習填空產生同類指令的工具。

欄位（6 大類）：
1. 遊戲類型（掉接遊戲／翻牌配對／自訂）+ 名稱 + 副標題（右上角有「✨ AI 幫我想名稱」按鈕，10 組預設名稱+副標題隨機挑，不連續重複）+ 使用情境
2. 物品/角色（10 個預設物品 chip，可自訂新增）+ 角色補充說明
3. 操作方式（手機/電腦，多選 chip）
4. 得分與生命值（基礎分、Combo 開關、生命數、扣血條件）
5. 特殊道具（星星/愛心/加速/炸彈/鑽石）+ 限時模式開關 + 店家獎品門檻模式開關（分數,獎品 一行一組）+ 目標分數（用來自動算難度曲線三階段）
6. 視覺風格（配色多選、整體氛圍單選）

右側 `#gpbPreviewText` 即時組出完整 Manus 指令文字（含自動生成的測試檢查清單），複製按鈕一鍵複製。上方 3 個範例按鈕可以載入原始 3 份指令對應的欄位設定（教學示範用）。

預覽框下方加了一張提示卡（`.gpb-wait-tips`）：「複製後，等 AI 運算的這幾分鐘可以做什麼？」（互評指令／預測畫面／準備第二輪修改／聽老師講重點），給老師上課時安排空檔活動用。

**已知修過的 bug**：範例③（翻牌配對）原本因為操作方式／使用情境選項沒有對應到既有 chip 選項，生成的指令會有幾段空白。已修：`gpMobileControl`/`gpDesktopControl` 增加「手指/滑鼠直接點擊卡牌或物件」通用選項，`gpbLoadEx()` 對於不在預設清單裡的 industry 值會自動切到「自訂」chip 並填入自訂輸入框（見 `industryPresets` 陣列判斷邏輯）。

### F. 你適合哪種髮型？（`hst-section`）— 新增功能

左邊男生、右邊女生兩張卡片，各自獨立按鈕「🎲 隨機換髮型」。男生 20 種髮型（`HAIR_M`），女生分「長髮」10 種（`HAIR_F_LONG`）／「短髮」10 種（`HAIR_F_SHORT`），上方 chip 先選長短髮類別，按鈕只在該類別池子裡抽，抽的邏輯會避免連續抽到同一個（`pick()` 函式用 `lastM`/`lastF` 記上一次的 index）。

**目前是純 SVG 插畫**（男女各一個共用底圖 `MALE_SVG`/`FEMALE_SVG`，含身體/脖子/耳朵/五官，`<g id="mHairLayer">`/`<g id="fHairLayer">` 是空的容器，JS 動態塞入對應髮型的 SVG path/shape），**不是真人照片**。原因：這個 session 沒有圖片生成工具，也不能隨便抓網路上的真人照片（版權/肖像權風險）。使用者已經確認先用插畫版本上線。

**如果要升級成真實照片效果**：
- 使用者需提供一張男生正面照 + 一張女生正面照（或用 AI 生圖工具做出 20+20 張已經套用不同髮型的照片）
- 把 `MALE_SVG`/`FEMALE_SVG` 換成 `<img>` 或 `<canvas>`，`HAIR_M`/`HAIR_F_LONG`/`HAIR_F_SHORT` 陣列裡的 `svg` 欄位改成對應照片的圖片路徑/base64，`hstRandom()` 裡把 `innerHTML=style.svg` 改成換 `src`
- 40 張圖片全部 base64 內嵌會讓檔案暴增，比較適合的做法是另外放 R2 或圖床，再用 `<img src="https://...">`，不要直接塞進這個單一 HTML 檔（目前檔案已經 1.45MB 了）

---

## 關鍵 JS 架構說明（延續上次交接內容）

### 工作小幫手（`helper-section`）
```javascript
.helper-options:not(.helper-multi)  → 單選（click 後 toggle selected）
.helper-multi[data-max="N"]         → 多選（超過 max 不讓選）
[data-key="int-job"]                → 觸發 updateIntSkills(job)
[data-make="post|reply|interview|resume|job"] → 呼叫 GEN[tool]() 生成 prompt
[data-reset="xxx"]                  → 清空 inputs、移除 show class
```

### WEBSITE LAB 精靈（`website-wizard`）
```javascript
showStep(n)          → 切換 hidden、更新 progress bar、更新 step labels、save()
cur / TOTAL=7         → 當前步驟 / 總步驟
renderSvc(prof)       → 依職業重建 #wServiceChoices 按鈕
updPrices()           → 依已選服務更新價格輸入欄（本次加了 ±100 按鈕）
g('wGenerate').click  → 收集所有步驟資料 → 組出完整 prompt → 顯示 #wResult
```

### 本次新增三個工具都各自獨立 IIFE，互不共用變數/函式名稱
```javascript
(function(){ ... 分鏡腳本產生器 ... window.openScriptModal / closeScriptModal / scriptXxx ... })();
(function(){ ... 遊戲指令產生器 ... window.openGpbModal / closeGpbModal / gpbXxx ... })();
(function(){ ... 髮型抽抽樂 ... window.hstRandom / hstSetLength ... })();
```

---

## 已知情況

- **Step 6 wBookingEmail**：欄位 ID 仍存在（在 save/restore/clear 陣列裡），但 DOM 元素已被移除，`getElementById` 會回傳 null，不影響功能。
- **wCustomService Enter 新增**：使用者可在 Step 2 自行輸入服務名稱按 Enter 新增，新按鈕也會被 sbox listener 正確處理（事件委派）。
- **價格 ±100 事件監聽**：掛在 `#wPriceRows` 父元素上（事件委派），`updPrices()` 重新渲染時不會遺失監聽。
- **console 一直出現的兩個錯誤**（`Cannot read properties of null (reading 'closest')` / `Cannot set properties of null (setting 'innerHTML')`）：這是既有的、每次載入頁面就會出現的舊錯誤，跟本次新功能無關，尚未排查根因，不影響任何功能運作，Codex 有空可以抓一下是哪段程式碼在頁面還沒渲染完成前就想存取 `#wPriceRows` 之類的元素。

---

## Codex 可以繼續做的方向

- [ ] 髮型抽抽樂如果要換成真人照片，需要使用者提供素材（見上方 F 節說明）
- [ ] 檢查並修掉那兩個一直出現在 console 的既有錯誤（見上方「已知情況」）
- [ ] Step 3 自我介紹改成選擇題（類似面試自我介紹工具的設計）
- [ ] LOGO MAKER 的 AI 幫我想按鈕品牌名稱與 WEBSITE LAB 同步
- [ ] 工作小幫手：面試 / 履歷工具「AI 幫我想」某幾個欄位加更多選項（如地區、學校類型）
- [ ] 手機版 helper-cards 在 2 欄時文字截斷問題
- [ ] 整理原始碼順序，把 `helper-section` / `picku-showcase` 移到 `</footer>` 之前，讓原始碼順序跟視覺順序一致（非必要，純粹整潔）

---

## 修改規則

- **只改指定的地方**，沒說要改的一律不動（尤其 Hero 區、CSS 變數）
- **修改 beautylab.html 後一定要跑 build_worker.py + wrangler deploy**
- **用字串替換而非行號替換**（檔案行數因為 base64 logo 龐大，grep 行號不穩定）
- **Python 腳本中 JS 字串的換行**：`\\n`（Python 原始碼 `\\n` → 寫入檔案變成 `\n` → JS 解析成真正的換行字元）
- **JS 絕對不能用 template literal（反引號）**：Worker 會把整個 HTML 包在 `` `...` `` 裡，內容裡出現反引號會直接中斷字串
- **新增功能前先確認素材來源**：像髮型照片這種需要真人圖片的需求，沒有圖片生成工具或現成素材時要主動跟使用者確認，不要生成/抓取不明來源的人像照片
