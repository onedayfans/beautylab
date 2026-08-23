# Beauty Lab · 美業 AI 網頁實作課

線上網址：https://beautylab.onedayfans.fans

單一 HTML 檔的課程網站，教美容美髮學生用 AI（ChatGPT / Manus / Codex）做出自己的 Logo、品牌網站、AI 小工具，以及互動小遊戲。部署在 Cloudflare Workers。

## 部署

```bash
cd deploy
python3 build_worker.py   # 讀 ../beautylab.html，escape 後輸出 index.js
npx wrangler deploy       # 需要先 npx wrangler login
```

每次修改 `beautylab.html` 後都要重新跑這兩步，Worker 才會更新。

## 檔案結構

- `beautylab.html` — 網站主檔（Hero、LOGO MAKER、WEBSITE LAB 精靈、工作小幫手、分鏡腳本產生器、遊戲指令產生器、髮型抽抽樂、PICKU 展示區等）
- `deploy/` — Cloudflare Worker 部署腳本（`build_worker.py`、`wrangler.jsonc`）
- `assets/hairstyles/` — 髮型參考圖片素材（male / female）
- `index.html`, `w3.html`, `course-dog.png`, `dog-logo.png` — 早期版本 / Logo 素材備份
- `HANDOFF_CLAUDE.md` — 給 Codex／未來接手者的完整交接文件（架構說明、修改紀錄、已知問題、待辦事項）

## 說明

這個 repo 是獨立備份，跟其他專案（yt-uploader、biteballapp、picku 等）分開管理，不共用程式碼或部署設定。
