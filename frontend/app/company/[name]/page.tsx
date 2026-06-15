type Props = {
  params: Promise<{
    name: string;
  }>;
};

async function getCompany(name: string) {

  const res = await fetch(
    `http://98.70.25.163:8000/ipo/company/${name}`,
    {
      cache: "no-store",
    }
  );

  return res.json();
}

export default async function CompanyPage(
  { params }: Props
) {

  const { name } = await params;

  const data = await getCompany(name);

  if (!data.found) {

    return (

      <main className="min-h-screen bg-slate-950 text-white p-8">

        <div className="max-w-5xl mx-auto">

          <a
            href="/"
            className="text-blue-400"
          >
            ← Dashboard
          </a>

          <h1 className="text-4xl font-bold mt-6">
            Company Not Found
          </h1>

        </div>

      </main>

    );
  }

  const timelineNames: Record<string, string> = {

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
      "IPO Priced",

    NO_ACTIVITY:
      "No Official IPO Activity"
  };

  const score = data.readiness_score || 0;

  return (

    <main className="min-h-screen bg-slate-950 text-white p-8">

      <div className="max-w-6xl mx-auto">

        <a
          href="/"
          className="text-blue-400"
        >
          ← Dashboard
        </a>

        <h1 className="text-5xl font-bold mt-4">
          {data.company}
        </h1>

        <p className="text-slate-400 mb-8">
          IPO Intelligence Profile
        </p>

        <div className="grid md:grid-cols-4 gap-4 mb-8">

          <div className="bg-slate-900 rounded-xl p-6">

            <p className="text-slate-400 text-sm">
              IPO Readiness
            </p>

            <p className="text-3xl font-bold mt-2">
              {score}%
            </p>

          </div>

          <div className="bg-slate-900 rounded-xl p-6">

            <p className="text-slate-400 text-sm">
              Current Stage
            </p>

            <p className="text-lg font-bold mt-2">
              {
                timelineNames[
                  data.stage
                ]
                || data.stage
              }
            </p>

          </div>

          <div className="bg-slate-900 rounded-xl p-6">

            <p className="text-slate-400 text-sm">
              Latest Source
            </p>

            <p className="text-lg font-bold mt-2">
              {data.source || "-"}
            </p>

          </div>

          <div className="bg-slate-900 rounded-xl p-6">

            <p className="text-slate-400 text-sm">
              Event Count
            </p>

            <p className="text-3xl font-bold mt-2">
              {data.event_count}
            </p>

          </div>

        </div>

        <div className="bg-slate-900 rounded-xl p-6 mb-8">

          <h2 className="text-2xl font-bold mb-4">
            IPO Readiness Progress
          </h2>

          <div className="w-full bg-slate-800 rounded-full h-6">

            <div
              className="bg-green-500 h-6 rounded-full"
              style={{
                width: `${score}%`
              }}
            />

          </div>

          <p className="mt-4 text-lg">
            {
              timelineNames[
                data.stage
              ]
              || data.stage
            }
          </p>

        </div>

        <div className="bg-slate-900 rounded-xl p-6 mb-8">

          <h2 className="text-2xl font-bold mb-4">
            Intelligence Summary
          </h2>

          <p className="text-slate-300">
            {
              data.summary ||
              "No official IPO activity detected yet."
            }
          </p>

        </div>

        <div className="grid lg:grid-cols-2 gap-6">

          <div className="bg-slate-900 rounded-xl p-6">

            <h2 className="text-2xl font-bold mb-4">
              IPO Timeline
            </h2>

            {
              data.timeline.length === 0 ? (

                <p className="text-slate-400">
                  No IPO activity detected yet.
                </p>

              ) : (

                <div className="space-y-3">

                  {data.timeline.map(
                    (
                      event: string
                    ) => (

                      <div
                        key={event}
                        className="
                          flex
                          items-center
                          gap-3
                        "
                      >

                        <span>
                          ✅
                        </span>

                        <span>
                          {
                            timelineNames[
                              event
                            ]
                            || event
                          }
                        </span>

                      </div>

                    )
                  )}

                </div>

              )
            }

          </div>

          <div className="bg-slate-900 rounded-xl p-6">

            <h2 className="text-2xl font-bold mb-4">
              Event History
            </h2>

            {
              data.history.length === 0 ? (

                <p className="text-slate-400">
                  No IPO events recorded.
                </p>

              ) : (

                <div className="space-y-4">

                  {data.history.map(
                    (
                      event: any,
                      index: number
                    ) => (

                      <div
                        key={index}
                        className="
                          border-b
                          border-slate-800
                          pb-3
                        "
                      >

                        <div
                          className="
                            font-semibold
                          "
                        >
                          {
                            timelineNames[
                              event.event_type
                            ]
                            || event.event_type
                          }
                        </div>

                        <div
                          className="
                            text-slate-400
                            text-sm
                          "
                        >
                          {event.source}
                        </div>

                        <div
                          className="
                            text-slate-500
                            text-xs
                          "
                        >
                          {event.filing_date}
                        </div>

                      </div>

                    )
                  )}

                </div>

              )
            }

          </div>

        </div>

      </div>

    </main>

  );
}