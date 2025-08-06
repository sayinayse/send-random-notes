import os
import random
from telegram import Bot
from dotenv import load_dotenv

# .env dosyasından değerleri yükle
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

NOTES_FOLDER = "notes"  # GitHub'da bu klasör olacak
bot = Bot(token=BOT_TOKEN)

def send_random_note():
    try:
        md_files = []
        for root, dirs, files in os.walk(NOTES_FOLDER):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))

        if not md_files:
            print("No .md files in the given path.")
            return

        selected = random.choice(md_files)
        with open(selected, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")
        list_items = [line.strip() for line in lines if line.startswith("-")]

        if not list_items:
            print("No list elements. Sending full note instead.")
            selected_item = content
        else:
            selected_item = random.choice(list_items)

        title = os.path.basename(selected)
        message = f"{title}\n\n{selected_item}"

        if len(message) > 4096:
            message = message[:4090] + "..."

        print(f"Sending message: {message[:100]}...")
        bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"Sent from: {selected}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_random_note()
