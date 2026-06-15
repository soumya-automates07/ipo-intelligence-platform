from database.connection import SessionLocal
from database.models import IPOOfficialEvent


db = SessionLocal()

events = (
    db.query(IPOOfficialEvent)
    .order_by(
        IPOOfficialEvent.filing_date.desc()
    )
    .all()
)

print("\nIPO EVENTS\n")

for event in events:

    print(
        f"{event.company_name}"
        f" | {event.event_type}"
        f" | {event.filing_date.date()}"
    )

db.close()
