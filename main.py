import os
from feeds import FEEDS
from scraper import fetch_articles
from summarizer import summarize_article
from notifier import broadcast_article
from state import load_state, save_state

STATE_PATH = os.path.join(os.path.dirname(__file__), "state.json")
MAX_ARTICLES_PER_RUN = 10
MAX_ARTICLE_AGE_DAYS = 30

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

        # Always limit to 30 days — prevents any old RSS articles from ever being sent
        articles = fetch_articles(feed["rss"], max_age_days=MAX_ARTICLE_AGE_DAYS)

        new_articles = [a for a in articles if a["id"] not in old_seen]

        # Mark ALL fetched articles as seen upfront, including ones we skip due to
        # MAX_ARTICLES_PER_RUN, so they are never retried in future runs
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
    run()
