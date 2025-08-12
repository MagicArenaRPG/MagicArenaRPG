ls -la
python3 -m pip install -r requirements.txt
python3 -m pip list
import sys
import pkg_resources

print("Python version:", sys.version)
print("Installed packages:", [p.project_name for p in pkg_resources.working_set])

import requests
import logging
import os
import json
import random
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{TOKEN}"

logging.basicConfig(level=logging.INFO)

INVENTORY_FILE = "users.json"
CARD_POOL = [
    "🧙 Маг Вогню",
    "🧊 Льодовий Некромант",
    "🧬 Природній Друїд",
    "💀 Темний Жрець",
    "🦄 Ельф Чарівник",
    "🐉 Драконовий Колекціонер"
]

def load_users():
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users):
    with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def send_message(chat_id, text):
    requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

def process_update(update):
    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        user_id = str(chat_id)
        users = load_users()

        if text == "/start":
            send_message(chat_id, "✨ Вітаємо у Magic Arena RPG!\nНатисни /pack щоб відкрити пакет.")
        elif text == "/pack":
            inventory = users.get(user_id, [])
            card = random.choice(CARD_POOL)
            inventory.append(card)
            users[user_id] = inventory
            save_users(users)
            send_message(chat_id, f"🎁 Ви відкрили пак і отримали: {card}")
        elif text == "/inventory":
            inventory = users.get(user_id, [])
            if inventory:
                items = "\n".join(inventory)
                send_message(chat_id, f"📂 Ваш інвентар:\n{items}")
            else:
                send_message(chat_id, "📂 Ваш інвентар порожній. Відкрий пак за допомогою /pack")

def polling_loop():
    offset = None
    while True:
        try:
            response = requests.get(f"{API_URL}/getUpdates", params={"timeout": 30, "offset": offset})
            updates = response.json()["result"]
            for update in updates:
                process_update(update)
                offset = update["update_id"] + 1
        except Exception as e:
            logging.warning(f"Polling error: {e}")

if __name__ == '__main__':
    print("✅ Bot is running in polling mode...")
    polling_loop()
