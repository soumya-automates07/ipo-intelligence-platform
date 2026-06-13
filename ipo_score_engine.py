from database.connection import engine
from database.models import Event
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

scores = {
    "IPO Signal": 10,
    "Funding Round": 8,
    "Partnership": 4,
    "Product Launch": 3,
    "Acquisition": 5,
    "Regulatory Action": -5,
    "Legal Issue": -8,
    "General News": 0
}

companies = ["OpenAI", "Anthropic", "SpaceX"]

for company in companies:

    events = session.query(Event).filter_by(
        company_name=company
    ).all()

    total_events = len(events)

    total_score = 0
    ipo_event_count = 0

    for event in events:

        total_score += scores.get(
            event.event_type,
            0
        )

        if event.event_type == "IPO Signal":
            ipo_event_count += 1

    # Score per event
    if total_events > 0:
        ipo_strength = round(
            (total_score / total_events) * 100,
            2
        )

        ipo_signal_percentage = round(
            (ipo_event_count / total_events) * 100,
            2
        )
    else:
        ipo_strength = 0
        ipo_signal_percentage = 0

    print("\n" + "=" * 50)
    print("Company:", company)
    print("Total Events:", total_events)
    print("IPO Score:", total_score)
    print("IPO Signal %:", ipo_signal_percentage)