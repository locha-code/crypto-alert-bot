import requests
import sqlite3
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

RESISTANCE_LEVEL = 59400.0
SUPPORT_LEVEL = 55680.0
SYMBOL = "BTC-USD"

conn = sqlite3.connect("btc_alerts.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS alert_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_type TEXT,
        trigger_price REAL,
        timestamp TEXT
    )
""")
conn.commit()

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram Error: {e}")
        return False

def get_btc_price():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    try:
        r = requests.get(url, timeout=10)
        return float(r.json()["data"]["amount"])
    except Exception as e:
        print(f"API Error: {e}")
        return None

send_telegram_msg(
    f"☁️ *Google Cloud 24/7 BTC Bot Active!*\n"
    f"📈 Resistance: `${RESISTANCE_LEVEL:,.2f}`\n"
    f"📉 Support: `${SUPPORT_LEVEL:,.2f}`"
)

resistance_triggered = False
support_triggered = False

while True:
    price = get_btc_price()
    if price is not None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] {SYMBOL}: ${price:,.2f}")

        if price >= RESISTANCE_LEVEL and not resistance_triggered:
            msg = f"🚨 *RESISTANCE ALERT ({SYMBOL})* 🚨\nPrice hit `${price:,.2f}` (Target: `${RESISTANCE_LEVEL:,.2f}`)\n⏰ `{now}`"
            if send_telegram_msg(msg):
                cursor.execute("INSERT INTO alert_history (alert_type, trigger_price, timestamp) VALUES (?, ?, ?)", ("RESISTANCE", price, now))
                conn.commit()
                resistance_triggered = True

        elif price <= SUPPORT_LEVEL and not support_triggered:
            msg = f"⚠️ *SUPPORT ALERT ({SYMBOL})* ⚠️\nPrice dropped to `${price:,.2f}` (Target: `${SUPPORT_LEVEL:,.2f}`)\n⏰ `{now}`"
            if send_telegram_msg(msg):
                cursor.execute("INSERT INTO alert_history (alert_type, trigger_price, timestamp) VALUES (?, ?, ?)", ("SUPPORT", price, now))
                conn.commit()
                support_triggered = True

        if price < (RESISTANCE_LEVEL - 150):
            resistance_triggered = False
        if price > (SUPPORT_LEVEL + 150):
            support_triggered = False

    time.sleep(10)
