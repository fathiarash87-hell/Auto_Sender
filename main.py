import pandas as pd
from compare import today_path, previous_path, build_changes
import argparse
from scraper import scrape_category
from mailer import send_report
from formatter import format_report
from telegram_sender import send_telegram


def main():
    parser = argparse.ArgumentParser(description="اسکرپ محصولات و ارسال گزارش اکسل با ایمیل")
    parser.add_argument("url", help="آدرس صفحه‌ی لیست محصولات")
    parser.add_argument("email", help="ایمیل گیرنده")
    parser.add_argument("--pages", type=int, default=9, help="حداکثر تعداد صفحه")
    args = parser.parse_args()

    try:
        df = scrape_category(args.url, args.pages)
    except ValueError as e:
        print(e)
        return
    if df.empty:
        print("هیچ محصولی پیدا نشد، ارسال انجام نشد")
        return

    filename = today_path()
    prev = previous_path(filename)

    changes = None
    if prev is not None:
        old_df = pd.read_excel(prev, sheet_name="Products")
        changes = build_changes(old_df, df)
        print(f"مقایسه با {prev.name}: {len(changes)} تغییر")
    else:
        print("فایل قبلی نبود، مقایسه انجام نشد")

    try:
        with pd.ExcelWriter(filename) as writer:
            df.to_excel(writer, sheet_name="Products", index=False)
            if changes is not None:
                changes.to_excel(writer, sheet_name="Changes", index=False)
    except PermissionError:
        print("فایل", filename.name, "باز است، ببندش و دوباره اجرا کن")
        return
    format_report(filename)
    body = f"سلام،\nگزارش {len(df)} محصول پیوست است."
    if changes is not None:
        body += f"\nتغییرات نسبت به قبل: {len(changes)} مورد."

    send_report(
        to=args.email,
        subject="گزارش قیمت محصولات",
        body=body,
        attachment_path=filename,
    )
    send_telegram(body, filename)

if __name__ == "__main__":
    main()