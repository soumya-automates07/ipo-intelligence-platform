import feedparser
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from database.insert_articles import save_article

rss_url = (
    "https://news.google.com/rss/search?q=OpenAI&hl=en-US&gl=US&ceid=US:en"
)

print("Fetching news...")

feed = feedparser.parse(rss_url)

print("Articles found:", len(feed.entries))

for article in feed.entries:

    save_article(
        company_name="OpenAI",
        headline=article.title,
        source="Google News",
        url=article.link
    )

print("Articles saved successfully!")