import feedparser
import os
import sys

from datetime import datetime, timezone

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from database.insert_articles import save_article

rss_url = (
    "https://news.google.com/rss/search?q=SpaceX&hl=en-US&gl=US&ceid=US:en"
)

feed = feedparser.parse(rss_url)

print("Articles found:", len(feed.entries))

for article in feed.entries:

    try:

        published = datetime(
            *article.published_parsed[:6],
            tzinfo=timezone.utc
        )

        age_hours = (
            datetime.now(timezone.utc) - published
        ).total_seconds() / 3600

        if age_hours > 24:
            continue

    except Exception:
        continue

    save_article(
        company_name="SpaceX",
        headline=article.title,
        source="Google News",
        url=article.link
    )
