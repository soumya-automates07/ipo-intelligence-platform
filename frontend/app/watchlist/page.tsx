import { getWatchlistStatus } from "../../lib/api";

export const revalidate = 30;

export default async function WatchlistPage() {

  const companies =
    await getWatchlistStatus();

  const stageNames: Record<
    string,
    string
  > = {

    NO_ACTIVITY:
      "No Activity",

    CONFIDENTIAL_FILING:
      "Confidential Filing",

    CONFIDENTIAL_FILING_AMENDMENT:
      "Confidential Filing Amendment",

    S1_FILED:
      "S-1 Filed",

    S1_AMENDED:
      "S-1 Amended",

    IPO_PRICING:
      "IPO Pricing",

    IPO_PRICED:
      "IPO Priced"
  };

  function badgeColor(
    stage: string
  ) {

    switch (stage) {

      case "IPO_PRICED":
        return
        "bg-green-500";

      case "IPO_PRICING":
        return
        "bg-yellow-500";

      case "S1_FILED":

      case "S1_AMENDED":
        return
        "bg-orange-500";

      case "CONFIDENTIAL_FILING":

      case "CONFIDENTIAL_FILING_AMENDMENT":
        return
        "bg-blue-500";

      default:
        return
        "bg-slate-600";
    }
  }

  return (

    <main className="min-h-screen bg-slate-950 text-white p-8">

      <div className="max-w-7xl mx-auto">

        <a
          href="/"
          className="text-blue-400"
        >
          ← Dashboard
        </a>

        <h1 className="text-5xl font-bold mt-4 mb-2">
          IPO Radar
        </h1>

        <p className="text-slate-400 mb-8">
          Watchlist Monitoring
        </p>

        <div className="bg-slate-900 rounded-xl overflow-hidden">

          <table className="w-full">

            <thead>

              <tr className="border-b border-slate-800">

                <th className="p-4 text-left">
                  Company
                </th>

                <th className="p-4 text-left">
                  Status
                </th>

                <th className="p-4 text-left">
                  Readiness
                </th>

              </tr>

            </thead>

            <tbody>

              {companies.map(
                (company: any) => (

                  <tr
                    key={
                      company.company_name
                    }
                    className="
                      border-b
                      border-slate-800
                    "
                  >

                    <td className="p-4">

                      <a
                        href={`/company/${company.company_name}`}
                        className="
                          hover:text-blue-400
                        "
                      >
                        {
                          company.company_name
                        }
                      </a>

                    </td>

                    <td className="p-4">

                      <span
                        className={`
                          px-3
                          py-1
                          rounded-full
                          text-sm
                          ${badgeColor(
                            company.stage
                          )}
                        `}
                      >
                        {
                          stageNames[
                            company.stage
                          ]
                          ||
                          company.stage
                        }
                      </span>

                    </td>

                    <td className="p-4">

                      {
                        company.readiness_score
                      }%

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        </div>

      </div>

    </main>

  );
}
