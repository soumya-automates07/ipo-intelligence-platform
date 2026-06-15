from data_collectors.sec_edgar import (
    SECEdgarCollector
)

from data_collectors.nasdaq_ipo import (
    NasdaqIPOCollector
)

from data_collectors.nyse_ipo import (
    NYSEIPOCollector
)


def main():

    print("\n=== SEC EDGAR ===")
    SECEdgarCollector().run()

    print("\n=== NASDAQ ===")
    NasdaqIPOCollector().run()

    print("\n=== NYSE ===")
    NYSEIPOCollector().run()

    print(
        "\nOfficial IPO Pipeline Complete"
    )


if __name__ == "__main__":
    main()