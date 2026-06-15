import requests
from datetime import datetime

from database.ipo_repository import IPORepository
from data_collectors.company_aliases import COMPANY_ALIASES


NASDAQ_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}


NASDAQ_IPO_URL = (
    "https://api.nasdaq.com/api/ipo/calendar"
)


NASDAQ_EVENT_MAPPING = {
    "filed": "IPO_FILED",
    "upcoming": "IPO_EXPECTED",
    "priced": "IPO_PRICED",
    "withdrawn": "IPO_WITHDRAWN"
}


class NasdaqIPOCollector:

    def __init__(self):

        self.watchlist = (
            IPORepository.get_watchlist()
        )

    def get_calendar_data(self):

        today = datetime.utcnow()

        date_value = (
            f"{today.year}-{today.month:02d}"
        )

        response = requests.get(
            NASDAQ_IPO_URL,
            params={
                "date": date_value
            },
            headers=NASDAQ_HEADERS,
            timeout=30
        )

        response.raise_for_status()

        payload = response.json()

        return payload.get(
            "data",
            {}
        )

    def company_matches(
        self,
        watchlist_company,
        nasdaq_company
    ):

        aliases = COMPANY_ALIASES.get(
            watchlist_company,
            [watchlist_company]
        )

        nasdaq_company = (
            nasdaq_company.lower()
        )

        for alias in aliases:

            if alias.lower() in nasdaq_company:
                return True

        return False

    def process_section(
        self,
        section_name,
        rows
    ):

        event_type = (
            NASDAQ_EVENT_MAPPING[
                section_name
            ]
        )

        for row in rows:

            company_name = (
                row.get(
                    "companyName",
                    ""
                )
            )

            for watchlist_company in self.watchlist:

                if not self.company_matches(
                    watchlist_company.company_name,
                    company_name
                ):
                    continue

                date_value = None

                for field in [
                    "pricedDate",
                    "expectedPriceDate",
                    "filedDate",
                    "withdrawDate"
                ]:

                    if row.get(field):

                        try:

                            date_value = (
                                datetime.strptime(
                                    row[field],
                                    "%m/%d/%Y"
                                )
                            )

                        except Exception:
                            pass

                        break

                source_url = (
                    "https://www.nasdaq.com/"
                    "market-activity/ipos"
                )

                saved = (
                    IPORepository.save_event(
                        company_name=
                        watchlist_company.company_name,

                        source="NASDAQ",

                        event_type=event_type,

                        title=(
                            f"{company_name}"
                            f" {event_type}"
                        ),

                        source_url=(
                            source_url
                            + "#"
                            + row.get(
                                "dealID",
                                ""
                            )
                        ),

                        filing_date=date_value,

                        event_metadata=row
                    )
                )

                if saved:

                    print(
                        f"Saved:"
                        f" {watchlist_company.company_name}"
                        f" -> {event_type}"
                    )

                else:

                    print(
                        f"Already exists:"
                        f" {watchlist_company.company_name}"
                        f" -> {event_type}"
                    )

    def run(self):

        data = (
            self.get_calendar_data()
        )

        priced = (
            data.get(
                "priced",
                {}
            ).get(
                "rows",
                []
            )
        )

        upcoming = (
            data.get(
                "upcoming",
                {}
            ).get(
                "upcomingTable",
                {}
            ).get(
                "rows",
                []
            )
        )

        filed = (
            data.get(
                "filed",
                {}
            ).get(
                "rows",
                []
            )
        )

        withdrawn = (
            data.get(
                "withdrawn",
                {}
            ).get(
                "rows",
                []
            )
        )

        self.process_section(
            "priced",
            priced
        )

        self.process_section(
            "upcoming",
            upcoming
        )

        self.process_section(
            "filed",
            filed
        )

        self.process_section(
            "withdrawn",
            withdrawn
        )


if __name__ == "__main__":

    collector = (
        NasdaqIPOCollector()
    )

    collector.run()
