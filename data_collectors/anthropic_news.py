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
    "https://news.google.com/rss/search?q=Anthropic&hl=en-US&gl=US&ceid=US:en"
)

feed = feedparser.parse(rss_url)

print("Articles found:", len(feed.entries))

for article in feed.entries:

    save_article(
        company_name="Anthropic",
        headline=article.title,
        source="Google News",
        url=article.link
    )

print("Anthropic articles saved successfully!")