import smtplib
from pathlib import Path
from email.message import EmailMessage
from dotenv import dotenv_values

values = dotenv_values(Path(__file__).parent / ".env")
sender = values.get("EMAIL_ADDRESS")
password = values.get("EMAIL_PASSWORD")


def send_report(to, subject, body, attachment_path):
    if not sender or not password:
        print("اطلاعات ایمیل از .env خوانده نشد")
        return False

    attachment = Path(attachment_path)
    if not attachment.exists():
        print("فایل پیوست پیدا نشد:", attachment)
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to
    msg.set_content(body)
    msg.add_attachment(
        attachment.read_bytes(),
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=attachment.name,
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        print("ایمیل ارسال شد به", to)
        return True
    except (smtplib.SMTPException, OSError) as e:
        print("ارسال نشد:", e)
        return False