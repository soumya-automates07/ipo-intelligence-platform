from database.connection import engine
from database.models import Article, Event
from sqlalchemy.orm import sessionmaker

from analysis.event_classifier import classify_event

Session = sessionmaker(bind=engine)
session = Session()

articles = session.query(Article).all()

count = 0

for article in articles:

    event_type = classify_event(article.headline)

    existing = session.query(Event).filter_by(
        company_name=article.company_name,
        description=article.headline
    ).first()

    if existing:
        continue

    event = Event(
        company_name=article.company_name,
        event_type=event_type,
        description=article.headline
    )

    session.add(event)

    count += 1

    if count % 100 == 0:
        print(f"Processed {count} events...")

session.commit()

print(f"\nFinished! Created {count} events.")