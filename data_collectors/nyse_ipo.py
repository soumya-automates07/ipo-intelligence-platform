import requests
from datetime import datetime

from database.ipo_repository import IPORepository
from data_collectors.company_aliases import (
    COMPANY_ALIASES
)


NYSE_IPO_URL = (
    "https://www.nyse.com/api/ipo-center/calendar"
)


STATUS_MAPPING = {
    "F": "IPO_FILED",
    "E": "IPO_EXPECTED",
    "P": "IPO_PRICED",
    "W": "IPO_WITHDRAWN"
}


class NYSEIPOCollector:

    def __init__(self):

        self.watchlist = (
            IPORepository.get_watchlist()
        )

    def get_calendar(self):

        response = requests.get(
            NYSE_IPO_URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def matches_company(
        self,
        watchlist_name,
        issuer_name
    ):

        aliases = COMPANY_ALIASES.get(
            watchlist_name,
            []
        )

        issuer_lower = (
            issuer_name.lower()
        )

        if (
            watchlist_name.lower()
            in issuer_lower
        ):
            return True

        for alias in aliases:

            if alias.lower() in issuer_lower:
                return True

        return False

    def process_entry(
        self,
        watchlist_name,
        entry
    ):

        status = entry.get(
            "deal_status_flg"
        )

        if status not in STATUS_MAPPING:
            return

        event_type = (
            STATUS_MAPPING[status]
        )

        issuer = entry.get(
            "issuer_nm",
            ""
        )

        symbol = entry.get(
            "symbol",
            ""
        )

        expected_date = entry.get(
            "expected_dt_report"
        )

        filing_date = None

        try:

            if (
                expected_date
                and "/" in expected_date
            ):

                filing_date = (
                    datetime.strptime(
                        expected_date,
                        "%m/%d/%Y"
                    )
                )

        except Exception:

            pass

        source_url = (
            "https://www.nyse.com/ipo-center"
        )

        saved = (
            IPORepository.save_event(
                company_name=watchlist_name,
                source="NYSE",
                event_type=event_type,
                title=f"{issuer} {event_type}",
                source_url=source_url,
                filing_date=filing_date,
                event_metadata={
                    "symbol": symbol,
                    "issuer": issuer,
                    "exchange": entry.get(
                        "custom_group_exchange_nm"
                    ),
                    "industry": entry.get(
                        "custom_group_industry_nm"
                    )
                }
            )
        )

        if saved:

            print(
                f"Saved: "
                f"{watchlist_name} "
                f"{event_type}"
            )

    def run(self):

        data = self.get_calendar()

        entries = data.get(
            "calendarList",
            []
        )

        for company in self.watchlist:

            for entry in entries:

                issuer = entry.get(
                    "issuer_nm",
                    ""
                )

                if self.matches_company(
                    company.company_name,
                    issuer
                ):

                    self.process_entry(
                        company.company_name,
                        entry
                    )


if __name__ == "__main__":

    collector = (
        NYSEIPOCollector()
    )

    collector.run()