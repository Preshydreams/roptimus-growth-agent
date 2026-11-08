import os
import json
import urllib.parse
import urllib.request
import subprocess
from pathlib import Path

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GROUP_LINK = "https://t.me/+3pRtVRtD4m5lMDdk"
OFFSET_FILE = Path("offset.txt")


def telegram(method, data):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    encoded = urllib.parse.urlencode(data).encode()

    request = urllib.request.Request(url, data=encoded)

    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.loads(response.read())

    if not result.get("ok"):
        raise RuntimeError("Telegram API request failed")

    return result["result"]


def reply(chat_id, text):
    telegram("sendMessage", {
        "chat_id": chat_id,
        "text": text
    })


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()

    command = text.split()[0].split("@")[0].lower() if text else ""

    if command == "/start":
        reply(chat_id,
              "Welcome to Roptimus AI Growth Agent!\n\n"
              "I can help you discover information about Roptimus "
              "and connect with our community.\n\n"
              "Use /about or /community.")

    elif command == "/about":
        reply(chat_id,
              "Welcome to Roptimus.\n\n"
              "Please review the platform's official information "
              "and understand all investment risks before making decisions.")

    elif command == "/community":
        reply(chat_id, f"Join our community:\n{GROUP_LINK}")

    else:
        reply(chat_id,
              "Thanks for contacting Roptimus AI Growth Agent.\n\n"
              "Use /about to learn more or /community to join our group.")


def save_offset(offset):
    OFFSET_FILE.write_text(str(offset))

    subprocess.run(
        ["git", "config", "user.name", "github-actions[bot]"],
        check=True
    )
    subprocess.run(
        ["git", "config", "user.email",
         "41898282+github-actions[bot]@users.noreply.github.com"],
        check=True
    )
    subprocess.run(["git", "add", "offset.txt"], check=True)

    changed = subprocess.run(
        ["git", "diff", "--cached", "--quiet"]
    ).returncode

    if changed != 0:
        subprocess.run(
            ["git", "commit", "-m", "Save Telegram update offset"],
            check=True
        )
        subprocess.run(["git", "push"], check=True)


def main():
    offset = int(OFFSET_FILE.read_text()) if OFFSET_FILE.exists() else 0

    print("Roptimus message handler started.")

    updates = telegram("getUpdates", {
        "offset": offset,
        "timeout": 45,
        "allowed_updates": json.dumps(["message"])
    })

    for update in updates:
        message = update.get("message")

        if message:
            handle_message(message)

        offset = update["update_id"] + 1
        save_offset(offset)

    print("Message check completed.")


if __name__ == "__main__":
    main()
