from database.connection import engine
from database.models import Article
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def save_article(company_name, headline, source, url):

    existing = session.query(Article).filter_by(
        url=url
    ).first()

    if existing:
        return

    article = Article(
        company_name=company_name,
        headline=headline,
        source=source,
        url=url
    )

    session.add(article)
    session.commit()