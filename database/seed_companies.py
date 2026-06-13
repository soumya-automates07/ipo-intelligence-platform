from database.connection import engine
from database.models import Company
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

companies_data = [
    ("OpenAI", "AI"),
    ("Anthropic", "AI"),
    ("SpaceX", "Space")
]

for name, sector in companies_data:
    existing = session.query(Company).filter_by(name=name).first()

    if not existing:
        company = Company(name=name, sector=sector)
        session.add(company)

session.commit()

print("Seeding completed successfully!")