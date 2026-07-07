import os
from feeds import FEEDS
from scraper import fetch_articles
from summarizer import summarize_article
from notifier import broadcast_article
from state import load_state, save_state

STATE_PATH = os.path.join(os.path.dirname(__file__), "state.json")
MAX_ARTICLES_PER_RUN = 10

def run(state_path: str = STATE_PATH, feeds: list = None) -> None:
    if feeds is None:
        feeds = FEEDS

    gemini_key = os.environ["GEMINI_API_KEY"]
    line_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

    state = load_state(state_path)
    total_sent = 0

    for feed in feeds:
        key = feed["key"]
        seen = set(state.get(key, []))
        is_first_run = len(seen) == 0

        max_age = 7 if is_first_run else None
        articles = fetch_articles(feed["rss"], max_age_days=max_age)

        new_articles = [a for a in articles if a["id"] not in seen]

        # On first run, mark all fetched articles as seen (even ones we won't send)
        # so future runs only pick up genuinely new articles
        if is_first_run:
            for article in articles:
                seen.add(article["id"])

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
                seen.add(article["id"])
                total_sent += 1
                print(f"[main] Sent: {article['title']}")
            except Exception as e:
                print(f"[main] LINE broadcast failed: {e}")

        state[key] = list(seen)

    save_state(state, state_path)
    print(f"[main] Done. {total_sent} articles sent.")

if __name__ == "__main__":
    run()
