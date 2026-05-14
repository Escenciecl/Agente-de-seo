import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
load_dotenv()

WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_PASS = os.getenv("WP_APP_PASSWORD")

def get_auth():
    return HTTPBasicAuth(WP_USER, WP_PASS)

def fetch_content(post_type, per_page=100):
    items = []
    page = 1
    while True:
        url = f"{WP_URL}/wp-json/wp/v2/{post_type}"
        r = requests.get(url, params={
            "per_page": per_page,
            "page": page,
            "status": "publish"
        }, auth=get_auth(), timeout=30)
        if r.status_code == 400:
            break
        batch = r.json()
        if not batch:
            break
        items.extend(batch)
        total = int(r.headers.get("X-WP-TotalPages", 1))
        if page >= total:
            break
        page += 1
    return items

def parse_item(item, tipo):
    url = item.get("link", "")
    yoast = item.get("yoast_head_json") or {}
    try:
        r = requests.head(url, timeout=10, allow_redirects=True)
        status = r.status_code
    except:
        status = 0
    return {
        "url": url,
        "title": (item.get("title") or {}).get("rendered", ""),
        "meta_desc": yoast.get("description", ""),
        "h1": yoast.get("title", ""),
        "word_count": 0,
        "status_code": status,
    }

def crawl_wordpress():
    print("Crawleando WordPress...")
    all_items = []
    for tipo in ["pages", "product"]:
        raw = fetch_content(tipo)
        parsed = [parse_item(i, tipo) for i in raw]
        all_items.extend(parsed)
        print(f"  {tipo}: {len(parsed)} encontrados")
    print(f"Total: {len(all_items)} páginas")
    return all_items

