import {
  getStats,
  getLatestEvent,
  getCompanies,
} from "../lib/api";

export const revalidate = 30;

export default async function Home() {

  const stats = await getStats();
  const latest = await getLatestEvent();
  const companies = await getCompanies();

  const prettyEvent = latest?.event_type
    ?.replaceAll("_", " ")
    ?.toLowerCase()
    ?.replace(/\b\w/g, (c: string) => c.toUpperCase())
    ?.replace("Ipo", "IPO");

  const timelineNames: Record<string, string> = {
    CONFIDENTIAL_FILING: "Confidential Filing",
    CONFIDENTIAL_FILING_AMENDMENT:
      "Confidential Filing Amendment",
    S1_FILED: "S-1 Filed",
    S1_AMENDED: "S-1 Amended",
    IPO_PRICING: "IPO Pricing",
    IPO_PRICED: "IPO Priced",
  };

  const scoreMap: Record<string, number> = {
    CONFIDENTIAL_FILING: 20,
    CONFIDENTIAL_FILING_AMENDMENT: 30,
    S1_FILED: 50,
    S1_AMENDED: 70,
    IPO_PRICING: 90,
    IPO_PRICED: 100,
  };

  const score = scoreMap[
    latest?.event_type
  ] || 0;

  return (

    <main className="min-h-screen bg-slate-950 text-white p-8">

      <div className="max-w-7xl mx-auto">

        <h1 className="text-4xl font-bold mb-2">
          IPO Intelligence Platform
        </h1>

        <p className="text-slate-400 mb-8">
          Official IPO Monitoring & Alerting System
        </p>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">

          <div className="bg-slate-900 p-6 rounded-xl">

            <p className="text-slate-400 text-sm">
              Companies
            </p>

            <p className="text-3xl font-bold">
              {stats.companies}
            </p>

          </div>

          <div className="bg-slate-900 p-6 rounded-xl">

            <p className="text-slate-400 text-sm">
              Events
            </p>

            <p className="text-3xl font-bold">
              {stats.events}
            </p>

          </div>

          <div className="bg-slate-900 p-6 rounded-xl">

            <p className="text-slate-400 text-sm">
              SEC Events
            </p>

            <p className="text-3xl font-bold">
              {stats.sec_events}
            </p>

          </div>

          <div className="bg-slate-900 p-6 rounded-xl">

            <p className="text-slate-400 text-sm">
              Latest Event
            </p>

            <p className="text-xl font-bold">
              {prettyEvent}
            </p>

          </div>

        </div>

        <div className="grid lg:grid-cols-2 gap-6 mb-6">

          <div className="bg-slate-900 rounded-xl p-6">

            <h2 className="text-xl font-bold mb-4">
              Latest Official Event
            </h2>

            <p className="text-3xl font-bold mb-2">
              {latest.company_name}
            </p>

            <p className="text-blue-400 mb-1">
              {prettyEvent}
            </p>

            <p className="text-slate-400 mb-4">
              {latest.source}
            </p>

            <p>
              {latest.summary}
            </p>

          </div>

          <div className="bg-slate-900 rounded-xl p-6">

            <div className="flex items-center justify-between mb-4">

              <h2 className="text-xl font-bold">
                Tracked Companies
              </h2>

              <a
                href="/watchlist"
                className="text-blue-400 text-sm"
              >
                Open IPO Radar →
              </a>

            </div>

            <ul className="space-y-3 max-h-[350px] overflow-y-auto">

              {companies.map(
                (company: string) => (

                  <li
                    key={company}
                    className="border-b border-slate-800 pb-2"
                  >

                    <a
                      href={`/company/${company}`}
                      className="hover:text-blue-400"
                    >
                      {company}
                    </a>

                  </li>

                )
              )}

            </ul>

          </div>

        </div>

        <div className="grid lg:grid-cols-2 gap-6">

          <div className="bg-slate-900 rounded-xl p-6">

            <h2 className="text-xl font-bold mb-4">
              IPO Readiness
            </h2>

            <p className="mb-3 text-lg">
              {prettyEvent}
            </p>

            <div className="w-full bg-slate-800 rounded-full h-5">

              <div
                className="bg-green-500 h-5 rounded-full"
                style={{
                  width: `${score}%`
                }}
              />

            </div>

            <p className="mt-3 text-2xl font-bold">
              {score}%
            </p>

          </div>

          <div className="bg-slate-900 rounded-xl p-6">

            <h2 className="text-xl font-bold mb-4">
              IPO Timeline
            </h2>

            <div className="space-y-3">

              {latest.timeline?.map(
                (event: string) => (

                  <div
                    key={event}
                    className="flex items-center gap-3"
                  >

                    <span>
                      ✅
                    </span>

                    <span>
                      {
                        timelineNames[event]
                        || event
                      }
                    </span>

                  </div>

                )
              )}

            </div>

          </div>

        </div>

        <div className="grid lg:grid-cols-2 gap-6 mt-6">

          <div className="bg-slate-900 rounded-xl p-6">

            <h2 className="text-xl font-bold mb-4">
              Analytics
            </h2>

            <div className="text-slate-400">
              Charts coming soon
            </div>

          </div>

          <div className="bg-slate-900 rounded-xl p-6">

            <h2 className="text-xl font-bold mb-4">
              Platform Health
            </h2>

            <div className="space-y-6">

              <div>

                <p className="text-slate-400">
                  Official Events
                </p>

                <p className="text-3xl font-bold">
                  {stats.events}
                </p>

              </div>

              <div>

                <p className="text-slate-400">
                  Latest Source
                </p>

                <p className="text-xl">
                  {latest.source}
                </p>

              </div>

              <div>

                <p className="text-slate-400">
                  System Status
                </p>

                <p className="text-green-400 font-semibold">
                  Operational
                </p>

              </div>

            </div>

          </div>

        </div>

      </div>

    </main>

  );
}