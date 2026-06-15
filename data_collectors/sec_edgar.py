import requests
from datetime import datetime

from database.ipo_repository import IPORepository
from data_collectors.company_aliases import COMPANY_ALIASES


SEC_HEADERS = {
    "User-Agent": "soumyadutta_dash0712@hotmail.com"
}

SEC_COMPANY_TICKERS_URL = (
    "https://www.sec.gov/files/company_tickers.json"
)


IPO_FORMS = {
    "DRS": "CONFIDENTIAL_FILING",
    "DRS/A": "CONFIDENTIAL_FILING_AMENDMENT",

    "S-1": "S1_FILED",
    "S-1/A": "S1_AMENDED",

    "F-1": "F1_FILED",
    "F-1/A": "F1_AMENDED",

    "424B1": "IPO_PRICING",
    "424B4": "IPO_PRICING",
    "424B5": "IPO_PRICING"
}


class SECEdgarCollector:

    def __init__(self):

        self.watchlist = (
            IPORepository.get_watchlist()
        )

        self.company_mapping = (
            self.get_company_mapping()
        )

    def get_company_mapping(self):

        response = requests.get(
            SEC_COMPANY_TICKERS_URL,
            headers=SEC_HEADERS,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def find_company_cik(
        self,
        company_name
    ):

        aliases = COMPANY_ALIASES.get(
            company_name,
            [company_name]
        )

        for alias in aliases:

            for item in self.company_mapping.values():

                title = item.get(
                    "title",
                    ""
                )

                if alias.lower() == title.lower():

                    return (
                        str(
                            item["cik_str"]
                        ).zfill(10),
                        title
                    )

        return None, None

    def get_recent_filings(
        self,
        cik
    ):

        url = (
            f"https://data.sec.gov/submissions/"
            f"CIK{cik}.json"
        )

        response = requests.get(
            url,
            headers=SEC_HEADERS,
            timeout=30
        )

        if response.status_code != 200:
            return None

        return response.json()

    def process_company(
        self,
        company_name
    ):

        print(
            f"\nProcessing: {company_name}"
        )

        cik, matched_entity = (
            self.find_company_cik(
                company_name
            )
        )

        if not cik:

            print(
                f"No SEC entity found for {company_name}"
            )

            return

        print(
            f"Matched SEC entity: {matched_entity}"
        )

        print(
            f"CIK: {cik}"
        )

        data = self.get_recent_filings(
            cik
        )

        if not data:
            return

        recent = (
            data
            .get("filings", {})
            .get("recent", {})
        )

        forms = recent.get(
            "form",
            []
        )

        accession_numbers = recent.get(
            "accessionNumber",
            []
        )

        filing_dates = recent.get(
            "filingDate",
            []
        )

        for index, form in enumerate(forms):

            if form not in IPO_FORMS:
                continue

            accession = accession_numbers[index]

            filing_date = filing_dates[index]

            source_url = (
                "https://www.sec.gov/Archives/"
                f"edgar/data/{int(cik)}/"
                f"{accession.replace('-', '')}/"
            )

            event_type = IPO_FORMS[form]

            saved = (
                IPORepository.save_event(
                    company_name=company_name,
                    source="SEC_EDGAR",
                    event_type=event_type,
                    title=f"{form} Filing",
                    source_url=source_url,
                    filing_date=datetime.strptime(
                        filing_date,
                        "%Y-%m-%d"
                    ),
                    event_metadata={
                        "cik": cik,
                        "matched_entity": matched_entity,
                        "form": form,
                        "accession": accession
                    }
                )
            )

            if saved:

                print(
                    f"Saved: {event_type}"
                )

            else:

                print(
                    f"Already exists: {event_type}"
                )

    def run(self):

        for company in self.watchlist:

            self.process_company(
                company.company_name
            )


if __name__ == "__main__":

    collector = (
        SECEdgarCollector()
    )

    collector.run()