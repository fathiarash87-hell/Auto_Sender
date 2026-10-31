from pathlib import Path
import requests
from dotenv import dotenv_values

values = dotenv_values(Path(__file__).parent / ".env")
token = values.get("TELEGRAM_TOKEN")
chat_id = values.get("TELEGRAM_CHAT_ID")


def send_telegram(text, file_path=None):
    if not token or not chat_id:
        print("TELEGRAM_TOKEN یا TELEGRAM_CHAT_ID از .env خوانده نشد")
        return False

    base = f"https://api.telegram.org/bot{token}"
    try:
        if file_path:
            path = Path(file_path)
            with open(path, "rb") as f:
                r = requests.post(
                    f"{base}/sendDocument",
                    data={"chat_id": chat_id, "caption": text},
                    files={"document": (path.name, f)},
                    timeout=60,
                )
        else:
            r = requests.post(
                f"{base}/sendMessage",
                data={"chat_id": chat_id, "text": text},
                timeout=30,
            )
        r.raise_for_status()
        print("پیام تلگرام ارسال شد")
        return True
    except (requests.exceptions.RequestException, OSError) as e:
        print("ارسال تلگرام ناموفق:", e)
        return False