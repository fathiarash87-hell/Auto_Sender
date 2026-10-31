import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from sites import SITES

headers = {"User-Agent": "Mozilla/5.0"}


def parse_price(tag):
    if tag is None:
        return None
    digits = re.sub(r"[^\d]", "", tag.get_text())
    return int(digits) if digits else None


def fetch(url, tries=3):
    for attempt in range(1, tries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"تلاش {attempt} ناموفق:", e)
            time.sleep(3)
    raise requests.exceptions.RequestException(f"بعد از {tries} تلاش جواب نیامد: {url}")


def get_config(url):
    domain = urlparse(url).netloc.removeprefix("www.")
    config = SITES.get(domain)
    if config is None:
        known = ", ".join(SITES)
        raise ValueError(f"سایت «{domain}» در sites.py تعریف نشده. سایت‌های موجود: {known}")
    return config


def scrape_page(url, config):
    soup = BeautifulSoup(fetch(url).text, "html.parser")
    rows = []
    for p in soup.select(config["item"]):
        a = p.select_one(config["name"])
        if not a:
            continue

        price_tag = None
        for selector in config["price"]:
            price_tag = p.select_one(selector)
            if price_tag:
                break

        rows.append({
            "Name": a.get_text(strip=True),
            "Price": parse_price(price_tag),
            "Link": a.get(config["link_attr"]),
        })
    return rows


def scrape_category(base_url, max_pages=9):
    config = get_config(base_url)
    base_url = base_url.rstrip("/") + "/"
    all_rows = []
    for page in range(1, max_pages + 1):
        url = base_url if page == 1 else config["page_url"].format(base=base_url, page=page)
        try:
            rows = scrape_page(url, config)
        except requests.exceptions.RequestException as e:
            print(f"صفحه {page} خطا:", e)
            break
        if not rows:
            print("صفحه خالی بود، تموم شد")
            break
        all_rows.extend(rows)
        print(f"صفحه {page}: {len(rows)} محصول")
        time.sleep(1)
    return pd.DataFrame(all_rows)