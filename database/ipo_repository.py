from database.connection import SessionLocal
from database.models import (
    IPOWatchlist,
    IPOOfficialEvent
)


class IPORepository:

    @staticmethod
    def get_watchlist():

        db = SessionLocal()

        try:

            return (
                db.query(IPOWatchlist)
                .filter(
                    IPOWatchlist.active == "Y"
                )
                .all()
            )

        finally:

            db.close()

    @staticmethod
    def event_exists(
        company_name,
        source,
        event_type,
        source_url
    ):

        db = SessionLocal()

        try:

            event = (
                db.query(IPOOfficialEvent)
                .filter(
                    IPOOfficialEvent.company_name ==
                    company_name,

                    IPOOfficialEvent.source ==
                    source,

                    IPOOfficialEvent.event_type ==
                    event_type
                )
                .first()
            )

            return event is not None

        finally:

            db.close()

    @staticmethod
    def save_event(
        company_name,
        source,
        event_type,
        title,
        source_url,
        filing_date=None,
        event_metadata=None
    ):

        db = SessionLocal()

        try:

            existing = (
                db.query(IPOOfficialEvent)
                .filter(
                    IPOOfficialEvent.company_name ==
                    company_name,

                    IPOOfficialEvent.source ==
                    source,

                    IPOOfficialEvent.event_type ==
                    event_type
                )
                .first()
            )

            if existing:

                return False

            event = IPOOfficialEvent(

                company_name=
                    company_name,

                source=
                    source,

                event_type=
                    event_type,

                title=
                    title,

                source_url=
                    source_url,

                filing_date=
                    filing_date,

                event_metadata=
                    event_metadata
            )

            db.add(event)

            db.commit()

            return True

        finally:

            db.close()

    @staticmethod
    def get_company_events(company_name):

        db = SessionLocal()

        try:

            return (
                db.query(IPOOfficialEvent)
                .filter(
                    IPOOfficialEvent.company_name ==
                    company_name
                )
                .all()
            )

        finally:

            db.close()