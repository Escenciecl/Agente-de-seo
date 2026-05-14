from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def save_pages(pages):
    db = get_client()
    db.table("pages").upsert(pages, on_conflict="url").execute()

def save_rankings(rankings):
    db = get_client()
    db.table("rankings").upsert(rankings, on_conflict="keyword,page_url,recorded_at").execute()

def save_alert(type, severity, message, url=None, data=None):
    db = get_client()
    db.table("alerts").insert({
        "type": type, "severity": severity,
        "message": message, "url": url, "data": data
    }).execute()

def save_recommendation(page_url, type, priority, description, suggestion=None):
    db = get_client()
    db.table("recommendations").insert({
        "page_url": page_url, "type": type, "priority": priority,
        "description": description, "suggestion": suggestion
    }).execute()

def get_previous_rankings(keyword, page_url):
    db = get_client()
    result = db.table("rankings")\
        .select("position")\
        .eq("keyword", keyword)\
        .eq("page_url", page_url)\
        .order("recorded_at", desc=True)\
        .limit(2)\
        .execute()
    rows = result.data
    if len(rows) >= 2:
        return rows[1]["position"]
    return None

