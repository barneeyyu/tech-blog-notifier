import os
import sys
from feeds import FEEDS
from scraper import fetch_articles
from summarizer import summarize_article
from notifier import broadcast_article
from state import load_state, save_state

STATE_PATH = os.path.join(os.path.dirname(__file__), "state.json")
MAX_ARTICLES_PER_RUN = 10
MAX_ARTICLE_AGE_DAYS = 7

def init(state_path: str = STATE_PATH, feeds: list = None) -> None:
    """Scan all feeds and mark every article from the past 30 days as seen,
    without sending anything. Run once to bootstrap state."""
    if feeds is None:
        feeds = FEEDS

    state = load_state(state_path)
    total = 0

    for feed in feeds:
        key = feed["key"]
        seen = set(state.get(key, []))
        articles = fetch_articles(feed["rss"], max_age_days=MAX_ARTICLE_AGE_DAYS)
        before = len(seen)
        for article in articles:
            seen.add(article["id"])
        added = len(seen) - before
        total += added
        print(f"[init] {feed['name']}: marked {added} articles (total {len(seen)})")
        state[key] = list(seen)

    save_state(state, state_path)
    print(f"[init] Done. {total} new articles marked as seen.")

def run(state_path: str = STATE_PATH, feeds: list = None) -> None:
    if feeds is None:
        feeds = FEEDS

    gemini_key = os.environ["GEMINI_API_KEY"]
    line_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

    state = load_state(state_path)
    total_sent = 0

    for feed in feeds:
        key = feed["key"]
        old_seen = set(state.get(key, []))

        articles = fetch_articles(feed["rss"], max_age_days=MAX_ARTICLE_AGE_DAYS)

        new_articles = [a for a in articles if a["id"] not in old_seen]

        # Mark all fetched articles as seen upfront so nothing is retried next run
        new_seen = old_seen | {a["id"] for a in articles}

        for article in new_articles:
            if total_sent >= MAX_ARTICLES_PER_RUN:
                break
            result = summarize_article(article["title"], article["body"], gemini_key)
            try:
                broadcast_article(
                    token=line_token,
                    name=feed["name"],
                    emoji=feed["emoji"],
                    zh_title=result["zh_title"],
                    original_title=article["title"],
                    zh_summary=result["zh_summary"],
                    url=article["url"],
                )
                total_sent += 1
                print(f"[main] Sent: {article['title']}")
            except Exception as e:
                print(f"[main] LINE broadcast failed: {e}")

        state[key] = list(new_seen)

    save_state(state, state_path)
    print(f"[main] Done. {total_sent} articles sent.")

if __name__ == "__main__":
    if "--init" in sys.argv:
        init()
    else:
        run()
