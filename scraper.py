import re
import feedparser
from datetime import datetime, timezone, timedelta

def fetch_articles(rss_url: str, max_age_days: int = None) -> list[dict]:
    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        print(f"[scraper] Failed to fetch {rss_url}: {e}")
        return []

    articles = []
    cutoff = None
    if max_age_days is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)

    for entry in feed.entries:
        if cutoff and hasattr(entry, "published_parsed") and entry.published_parsed:
            pub = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            if pub < cutoff:
                continue

        body = getattr(entry, "summary", "") or ""
        body = re.sub(r"<[^>]+>", " ", body).strip()
        body = body[:2000]

        articles.append({
            "id": getattr(entry, "id", entry.link),
            "title": getattr(entry, "title", ""),
            "body": body,
            "url": getattr(entry, "link", ""),
        })

    return articles
