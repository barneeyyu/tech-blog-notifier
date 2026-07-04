# Tech Blog Notifier

每日自動追蹤科技大廠工程部落格，將新文章翻譯成繁體中文並摘要，透過 LINE Bot 廣播給所有追蹤者。

## 追蹤的部落格

| 公司 | 主題 |
|------|------|
| 🎬 Netflix Tech Blog | 微服務、高併發、Java 生態 |
| 🚗 Uber Engineering | 高併發、故障隔離 |
| 💳 Stripe Engineering | 金融級資料一致性、關聯式資料庫 |
| ⬛ Square/Block Engineering | 金融系統、嚴謹的資料庫操作 |
| 💬 Discord Blog | C++/Go/Rust、底層效能優化 |
| 🎨 Figma Blog | 效能優化、前端技術 |
| ▲ Vercel Blog | Serverless、邊緣運算 |
| ☁️ AWS Blog | 雲端部署、自動化流程 |

## 運作方式

1. GitHub Actions 每天早上 9:00（台灣時間）自動執行
2. 抓取各部落格的 RSS feed，比對 `state.json` 找出新文章
3. 呼叫 Gemini API 翻譯標題、生成中文摘要
4. 透過 LINE Messaging API Broadcast 發送給所有 Bot 好友
5. 更新 `state.json` 並 commit 回 repo，避免重複發送

LINE 訊息格式：
```
🎬 Netflix Tech Blog

📌 [中文標題]
Original: [English Title]

📝 [2-3 句中文摘要]

🔗 https://...
```

## 設定方式

### 1. Fork 或 clone 這個 repo

### 2. 取得必要的 API 金鑰

**Gemini API Key**
- 前往 [Google AI Studio](https://aistudio.google.com/app/apikey)
- 建立 API key（免費）

**LINE Channel Access Token**
- 前往 [LINE Developers Console](https://developers.line.biz/)
- 建立 Messaging API channel
- 在 Messaging API 頁面點「Issue」產生 Channel access token

### 3. 設定 GitHub Secrets

在 repo 的 **Settings → Secrets and variables → Actions** 新增：

| Secret 名稱 | 說明 |
|------------|------|
| `GEMINI_API_KEY` | Google AI Studio 的 API key |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE Messaging API 的 access token |

### 4. 加入 LINE Bot 為好友

在 LINE Developers Console → Basic settings 找到 Bot 的 QR code 或 Basic ID，加入好友後即可接收廣播。

### 5. 手動觸發測試

在 GitHub repo 的 **Actions → Daily Tech Blog Digest → Run workflow** 手動觸發一次，確認 LINE 有收到訊息。

## 本機開發

```bash
# 安裝依賴
pip install -r requirements.txt

# 設定環境變數
export GEMINI_API_KEY=your_key
export LINE_CHANNEL_ACCESS_TOKEN=your_token

# 執行
python main.py
```

執行測試：
```bash
pytest tests/ -v
```

## 注意事項

- 每次執行最多發送 **10 篇**文章，避免洗版
- 第一次執行只抓 **7 天內**的文章
- 若某個 RSS 來源失敗，不影響其他來源繼續執行
- 若 LINE 發送失敗，該文章不會被記入 `state.json`，下次會重試
