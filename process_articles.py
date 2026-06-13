from database.connection import engine
from database.models import Article
from sqlalchemy.orm import sessionmaker

from analysis.event_classifier import classify_event

Session = sessionmaker(bind=engine)
session = Session()

articles = session.query(Article).limit(20).all()

for article in articles:

    event_type = classify_event(article.headline)

    print()
    print("Company :", article.company_name)
    print("Headline:", article.headline)
    print("Event   :", event_type)