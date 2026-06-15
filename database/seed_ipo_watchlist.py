from sqlalchemy.orm import sessionmaker

from database.connection import engine
from database.models import IPOWatchlist


Session = sessionmaker(bind=engine)

session = Session()


companies = [
    "OpenAI",
    "Anthropic",
    "SpaceX"
]


for company in companies:

    existing = (
        session.query(IPOWatchlist)
        .filter_by(company_name=company)
        .first()
    )

    if not existing:

        session.add(
            IPOWatchlist(
                company_name=company
            )
        )

        print(f"Added: {company}")

    else:

        print(f"Already exists: {company}")


session.commit()

print("Watchlist seeded successfully")
