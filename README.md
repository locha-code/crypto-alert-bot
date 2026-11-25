# 24/7 Automated Crypto Alert & SQL Logging Bot

A lightweight, cloud-hosted Python trading alert system deployed on a **Google Cloud Platform (GCP) Linux VM** that monitors real-time cryptocurrency price levels, logs triggered alerts into a local **SQLite database**, and delivers instant notifications via the **Telegram Bot API**.

## Key Features
- **24/7 Cloud Execution:** Continuously runs on a Debian Linux GCP VM instance with automated background process management.
- **Automated Support & Resistance Monitoring:** Tracks live `BTC-USD` market prices and detects breakouts/breakdowns against predefined technical levels.
- **Persistent SQL Audit Trail:** Stores every triggered alert (`alert_type`, `trigger_price`, `timestamp`) in an `SQLite3` database (`btc_alerts.db`) for historical verification and quantitative analysis.
- **Instant Telegram Notifications:** Dispatches formatted Markdown alerts directly to Telegram via REST API.
- **Secure Credential Management:** Separates API tokens and chat IDs from source code using environment variables (`python-dotenv`).

## Tech Stack
- **Language:** Python 3
- **Database:** SQLite3 (`sqlite3`)
- **APIs & Libraries:** Telegram Bot API, `requests`, `python-dotenv`
- **Infrastructure:** Google Cloud Platform (Compute Engine VM - Debian Linux)

## Setup & Deployment
1. Clone the repository: `git clone [https://github.com/lochanahimsara378-art/crypto-alert-bot.git](https://github.com/lochanahimsara378-art/crypto-alert-bot.git)`
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your `BOT_TOKEN` and `CHAT_ID`.
4. Run the bot: `python3 bot.py`
