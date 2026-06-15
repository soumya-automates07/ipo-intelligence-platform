from database.models import IPOOfficialEvent
from database.connection import SessionLocal
from fastapi import FastAPI
from database.connection import engine
from ipo_intelligence import EVENT_INTELLIGENCE
import subprocess
import sys

from ai_summary import (
    generate_summary,
    generate_risk_level
)

from sqlalchemy import text, func

app = FastAPI()


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/run-pipeline")
def run_pipeline():

    subprocess.Popen(
        [sys.executable, "run_pipeline.py"]
    )

    return {
        "success": True,
        "message": "Pipeline started in background"
    }


IPO_FILTERS = """
    event_type = 'IPO Signal'
    AND description NOT ILIKE '%probe%'
    AND description NOT ILIKE '%investigation%'
    AND description NOT ILIKE '%lawsuit%'
    AND description NOT ILIKE '%what does it mean%'
    AND description NOT ILIKE '%better buy%'
    AND description NOT ILIKE '%ipo race%'
    AND description NOT ILIKE '%ipo buzz%'
    AND description NOT ILIKE '%opinion%'
    AND description NOT ILIKE '%analysis%'
"""


IPO_RANKING = """
    CASE
        WHEN description ILIKE '%files for ipo%' THEN 100
        WHEN description ILIKE '%filed for ipo%' THEN 100
        WHEN description ILIKE '%confidentially files%' THEN 95
        WHEN description ILIKE '%confidentially filed%' THEN 95
        WHEN description ILIKE '%goes public%' THEN 90
        WHEN description ILIKE '%going public%' THEN 90
        WHEN description ILIKE '%nasdaq debut%' THEN 90
        WHEN description ILIKE '%public debut%' THEN 90
        WHEN description ILIKE '%prices shares%' THEN 85
        WHEN description ILIKE '%ipo priced%' THEN 85
        WHEN description ILIKE '%largest public offering%' THEN 80
        WHEN description ILIKE '%public offering%' THEN 80
        WHEN description ILIKE '%stock jumps%' THEN 50
        ELSE 1
    END
"""


def get_best_ipo_signal(company=None):

    with engine.connect() as conn:

        if company:

            query = text(f"""
                SELECT company_name,
                       description
                FROM events
                WHERE company_name = :company
                  AND {IPO_FILTERS}
                ORDER BY
                    {IPO_RANKING} DESC,
                    id DESC
                LIMIT 1
            """)

            result = conn.execute(
                query,
                {"company": company}
            )

        else:

            query = text(f"""
                SELECT company_name,
                       description
                FROM events
                WHERE {IPO_FILTERS}
                ORDER BY
                    {IPO_RANKING} DESC,
                    id DESC
                LIMIT 1
            """)

            result = conn.execute(query)

        return result.fetchone()


@app.get("/latest-ipo-signal")
def latest_ipo_signal():

    row = get_best_ipo_signal()

    if not row:
        return {
            "found": False
        }

    return {
        "found": True,
        "company": row[0],
        "description": row[1]
    }


@app.get("/latest-ipo-signal/{company}")
def latest_company_signal(company: str):

    row = get_best_ipo_signal(company)

    if not row:
        return {
            "found": False
        }

    return {
        "found": True,
        "company": row[0],
        "description": row[1]
    }
@app.get("/latest-ipo-summary/{company}")
def latest_company_summary(company: str):

    row = get_best_ipo_signal(company)

    if not row:
        return {
            "found": False
        }

    company_name = row[0]
    description = row[1]

    try:

        summary = generate_summary(
            company_name,
            description
        )

        risk_level = generate_risk_level(
            company_name,
            description
        )

    except Exception:

        summary = "AI summary temporarily unavailable"
        risk_level = "UNKNOWN"

    return {
        "found": True,
        "company": company_name,
        "description": description,
        "summary": summary,
        "risk_level": risk_level
    }

@app.get("/latest-ipo-summary")
def latest_ipo_summary():

    row = get_best_ipo_signal()

    if not row:
        return {
            "found": False
        }

    company = row[0]
    description = row[1]

    try:

        summary = generate_summary(
            company,
            description
        )

        risk_level = generate_risk_level(
            company,
            description
        )

    except Exception:

        summary = "AI summary temporarily unavailable"
        risk_level = "UNKNOWN"

    return {
        "found": True,
        "company": company,
        "description": description,
        "summary": summary,
        "risk_level": risk_level
    }


@app.get("/check-new-alert")
def check_new_alert():

    row = get_best_ipo_signal()

    if not row:
        return {
            "found": False
        }

    company = row[0]
    description = row[1]

    with engine.connect() as conn:

        check = conn.execute(text("""
            SELECT last_headline
            FROM alert_state
            ORDER BY id DESC
            LIMIT 1
        """))

        last = check.fetchone()

    is_new = True

    if last and last[0] == description:
        is_new = False

    return {
        "found": True,
        "is_new": is_new,
        "company": company,
        "description": description
    }


@app.post("/mark-alert-sent")
def mark_alert_sent():

    row = get_best_ipo_signal()

    if not row:
        return {
            "success": False
        }

    company = row[0]
    description = row[1]

    with engine.connect() as conn:

        conn.execute(text("""
            DELETE FROM alert_state
        """))

        conn.execute(
            text("""
                INSERT INTO alert_state(last_headline)
                VALUES(:headline)
            """),
            {
                "headline": description
            }
        )

        conn.execute(
            text("""
                INSERT INTO alert_history(
                    company_name,
                    headline
                )
                VALUES(
                    :company,
                    :headline
                )
            """),
            {
                "company": company,
                "headline": description
            }
        )

        conn.commit()

    return {
        "success": True,
        "headline": description
    }
@app.get("/check-new-alert/{company}")
def check_new_alert_company(company: str):

    row = get_best_ipo_signal(company)

    if not row:
        return {"found": False}

    description = row[1]

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT last_headline
                FROM alert_state
                WHERE company_name = :company
            """),
            {"company": company}
        )

        last = result.fetchone()

    is_new = True

    if last and last[0] == description:
        is_new = False

    return {
        "found": True,
        "company": company,
        "description": description,
        "is_new": is_new
    }
@app.post("/mark-alert-sent/{company}")
def mark_alert_sent_company(company: str):

    row = get_best_ipo_signal(company)

    if not row:
        return {"success": False}

    description = row[1]

    with engine.connect() as conn:

        conn.execute(
            text("""
                DELETE FROM alert_state
                WHERE company_name = :company
            """),
            {"company": company}
        )

        conn.execute(
            text("""
                INSERT INTO alert_state(
                    company_name,
                    last_headline
                )
                VALUES(
                    :company,
                    :headline
                )
            """),
            {
                "company": company,
                "headline": description
            }
        )

        conn.commit()

    return {
        "success": True,
        "company": company,
        "headline": description
    }
@app.get("/ipo/events")
def ipo_events():

    db = SessionLocal()

    try:

        events = (
            db.query(IPOOfficialEvent)
            .order_by(
                IPOOfficialEvent.filing_date.desc()
            )
            .all()
        )

        return [
            {
                "id": e.id,
                "company_name": e.company_name,
                "source": e.source,
                "event_type": e.event_type,
                "title": e.title,
                "filing_date": (
                    e.filing_date.isoformat()
                    if e.filing_date
                    else None
                )
            }
            for e in events
        ]

    finally:

        db.close()


@app.get("/ipo/events/{company}")
def ipo_company_events(company: str):

    db = SessionLocal()

    try:

        events = (
            db.query(IPOOfficialEvent)
            .filter(
                IPOOfficialEvent.company_name == company
            )
            .order_by(
                IPOOfficialEvent.filing_date.desc()
            )
            .all()
        )

        return [
            {
                "id": e.id,
                "company_name": e.company_name,
                "source": e.source,
                "event_type": e.event_type,
                "title": e.title,
                "filing_date": (
                    e.filing_date.isoformat()
                    if e.filing_date
                    else None
                )
            }
            for e in events
        ]

    finally:

        db.close()


@app.get("/ipo/latest")
def ipo_latest():

    db = SessionLocal()

    try:

        event = (
            db.query(IPOOfficialEvent)
            .order_by(
                IPOOfficialEvent.detected_at.desc()
            )
            .first()
        )

        if not event:

            return {
                "found": False
            }

        return {
            "found": True,
            "company_name":
                event.company_name,
            "source":
                event.source,
            "event_type":
                event.event_type,
            "title":
                event.title,
            "filing_date":
                event.filing_date,
            "detected_at":
                event.detected_at
        }

    finally:

        db.close()

@app.get("/ipo/check-new-alert")
def ipo_check_new_alert():

    db = SessionLocal()

    try:

        latest = db.execute(
            text("""
                SELECT ioe.*
                FROM ipo_official_events ioe
                INNER JOIN ipo_watchlist iw
                    ON lower(ioe.company_name) =
                       lower(iw.company_name)
                ORDER BY ioe.detected_at DESC
                LIMIT 1
            """)
        ).fetchone()

        if not latest:

            return {
                "found": False
            }

        latest_event = (
            db.query(IPOOfficialEvent)
            .filter(
                IPOOfficialEvent.id ==
                latest.id
            )
            .first()
        )

        intel = EVENT_INTELLIGENCE.get(
            latest_event.event_type,
            {
                "importance": "UNKNOWN",
                "summary": "No summary available.",
                "stage": "Unknown",
                "readiness_score": 0,
                "risk": "Unknown",
                "expected_next": "Unknown",
                "timeline": "Unknown",
                "intelligence": ""
            }
        )

        with engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT last_headline
                    FROM alert_state
                    WHERE company_name =
                          'OFFICIAL_IPO'
                    LIMIT 1
                """)
            )

            last = result.fetchone()

        current_key = (
            f"{latest_event.company_name}|"
            f"{latest_event.source}|"
            f"{latest_event.event_type}|"
            f"{latest_event.id}"
        )

        is_new = True

        if last and last[0] == current_key:

            is_new = False

        timeline_events = (
            db.query(IPOOfficialEvent)
            .filter(
                IPOOfficialEvent.company_name ==
                latest_event.company_name
            )
            .all()
        )

        IPO_ORDER = [
            "CONFIDENTIAL_FILING",
            "CONFIDENTIAL_FILING_AMENDMENT",
            "S1_FILED",
            "S1_AMENDED",
            "IPO_PRICING",
            "IPO_PRICED"
        ]

        existing_events = set(
            event.event_type
            for event in timeline_events
        )

        timeline = [
            event
            for event in IPO_ORDER
            if event in existing_events
        ]

        return {

            "found": True,

            "is_new":
                is_new,

            "event_id":
                latest_event.id,

            "company_name":
                latest_event.company_name,

            "source":
                latest_event.source,

            "event_type":
                latest_event.event_type,

            "title":
                latest_event.title,

            "source_url":
                latest_event.source_url,

            "filing_date":
                (
                    latest_event.filing_date.isoformat()
                    if latest_event.filing_date
                    else None
                ),

            "detected_at":
                (
                    latest_event.detected_at.isoformat()
                    if latest_event.detected_at
                    else None
                ),

            "importance":
                intel["importance"],

            "summary":
                intel["summary"],

            "intelligence":
                intel.get(
                    "intelligence",
                    ""
                ),

            "stage":
                intel.get(
                    "stage",
                    "Unknown"
                ),

            "readiness_score":
                intel.get(
                    "readiness_score",
                    0
                ),

            "risk":
                intel.get(
                    "risk",
                    "Unknown"
                ),

            "expected_next":
                intel.get(
                    "expected_next",
                    "Unknown"
                ),

            "timeline_estimate":
                intel.get(
                    "timeline",
                    "Unknown"
                ),

            "timeline":
                timeline,

            "event_count":
                len(timeline)
        }

    finally:

        db.close()

@app.post("/ipo/mark-alert-sent")
def ipo_mark_alert_sent():

    db = SessionLocal()

    try:

        latest = (
            db.query(IPOOfficialEvent)
            .order_by(
                IPOOfficialEvent.detected_at.desc()
            )
            .first()
        )

        if not latest:

            return {
                "success": False
            }

        current_key = (
            f"{latest.company_name}|"
            f"{latest.source}|"
            f"{latest.event_type}|"
            f"{latest.id}"
        )

        with engine.connect() as conn:

            conn.execute(
                text("""
                    DELETE FROM alert_state
                    WHERE company_name = 'OFFICIAL_IPO'
                """)
            )

            conn.execute(
                text("""
                    INSERT INTO alert_state(
                        company_name,
                        last_headline
                    )
                    VALUES(
                        'OFFICIAL_IPO',
                        :headline
                    )
                """),
                {
                    "headline":
                        current_key
                }
            )

            conn.commit()

        return {
            "success": True,
            "event_id": latest.id
        }

    finally:

        db.close()

@app.get("/ipo/timeline/{company}")
def ipo_timeline(company: str):

    db = SessionLocal()

    try:

        events = (
            db.query(IPOOfficialEvent)
            .filter(
                IPOOfficialEvent.company_name == company
            )
            .order_by(
                IPOOfficialEvent.filing_date.asc()
            )
            .all()
        )

        return [
            {
                "event_type": e.event_type
            }
            for e in events
        ]

    finally:

        db.close()

@app.get("/ipo/companies")
def ipo_companies():

    db = SessionLocal()

    try:

        companies = (
            db.query(
                IPOOfficialEvent.company_name
            )
            .distinct()
            .all()
        )

        return sorted(
            [
                company[0]
                for company in companies
            ]
        )

    finally:

        db.close()

@app.get("/ipo/stats")
def ipo_stats():

    db = SessionLocal()

    try:

        companies = db.execute(
            text("""
                SELECT COUNT(*)
                FROM ipo_watchlist
            """)
        ).scalar()

        total_events = (
            db.query(
                IPOOfficialEvent
            )
            .count()
        )

        sec_events = (
            db.query(
                IPOOfficialEvent
            )
            .filter(
                IPOOfficialEvent.source ==
                "SEC_EDGAR"
            )
            .count()
        )

        nasdaq_events = (
            db.query(
                IPOOfficialEvent
            )
            .filter(
                IPOOfficialEvent.source ==
                "NASDAQ"
            )
            .count()
        )

        nyse_events = (
            db.query(
                IPOOfficialEvent
            )
            .filter(
                IPOOfficialEvent.source ==
                "NYSE"
            )
            .count()
        )

        return {
            "companies":
                companies,

            "events":
                total_events,

            "sec_events":
                sec_events,

            "nasdaq_events":
                nasdaq_events,

            "nyse_events":
                nyse_events
        }

    finally:

        db.close()

@app.get("/ipo/readiness/{company}")
def ipo_readiness(company: str):

    db = SessionLocal()

    try:

        events = (
            db.query(
                IPOOfficialEvent
            )
            .filter(
                IPOOfficialEvent.company_name ==
                company
            )
            .all()
        )

        event_types = set(
            event.event_type
            for event in events
        )

        score = 0
        stage = "Unknown"

        if "CONFIDENTIAL_FILING" in event_types:
            score = 25
            stage = "🟡 Early Stage"

        if "S1_FILED" in event_types:
            score = 50
            stage = "🟠 Filing Stage"

        if "S1_AMENDED" in event_types:
            score = 75
            stage = "🟠 Filing Stage"

        if "IPO_PRICING" in event_types:
            score = 90
            stage = "🔴 Final Stage"

        if "IPO_PRICED" in event_types:
            score = 100
            stage = "🔴 Final Stage"

        return {
            "company": company,
            "score": score,
            "stage": stage
        }

    finally:

        db.close()

@app.get("/ipo/watchlist")
def get_watchlist():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT company_name
                FROM ipo_watchlist
                ORDER BY company_name
            """)
        )

        companies = [
            row[0]
            for row in result.fetchall()
        ]

    return companies

@app.get("/ipo/company/{company}")
def get_company(company: str):

    db = SessionLocal()

    try:

        watchlist_company = db.execute(
            text("""
                SELECT company_name
                FROM ipo_watchlist
                WHERE lower(company_name) =
                      lower(:company)
                LIMIT 1
            """),
            {
                "company": company
            }
        ).fetchone()

        if not watchlist_company:

            return {
                "found": False,
                "company": company
            }

        company_name = watchlist_company[0]

        events = (
            db.query(
                IPOOfficialEvent
            )
            .filter(
                IPOOfficialEvent.company_name.ilike(
                    company_name
                )
            )
            .order_by(
                IPOOfficialEvent.detected_at.desc()
            )
            .all()
        )

        if not events:

            return {

                "found": True,

                "company":
                    company_name,

                "latest_event":
                    None,

                "stage":
                    "NO_ACTIVITY",

                "readiness_score":
                    0,

                "source":
                    None,

                "filing_date":
                    None,

                "event_count":
                    0,

                "timeline":
                    [],

                "history":
                    [],

                "summary":
                    "No official IPO activity detected yet."
            }

        latest = events[0]

        score_map = {
            "CONFIDENTIAL_FILING": 20,
            "CONFIDENTIAL_FILING_AMENDMENT": 30,
            "S1_FILED": 50,
            "S1_AMENDED": 70,
            "IPO_PRICING": 90,
            "IPO_PRICED": 100
        }

        readiness_score = score_map.get(
            latest.event_type,
            0
        )

        timeline = []

        seen = set()

        for event in reversed(events):

            if event.event_type not in seen:

                timeline.append(
                    event.event_type
                )

                seen.add(
                    event.event_type
                )

        return {

            "found": True,

            "company":
                latest.company_name,

            "latest_event":
                latest.event_type,

            "stage":
                latest.event_type,

            "readiness_score":
                readiness_score,

            "source":
                latest.source,

            "filing_date":
                latest.filing_date,

            "event_count":
                len(events),

            "timeline":
                timeline,

            "history": [

                {
                    "event_type":
                        e.event_type,

                    "source":
                        e.source,

                    "filing_date":
                        str(e.filing_date)
                        if e.filing_date
                        else None
                }

                for e in events

            ],

            "summary":
                EVENT_INTELLIGENCE.get(
                    latest.event_type,
                    {}
                ).get(
                    "summary",
                    ""
                )
        }

    finally:

        db.close()

@app.get("/ipo/watchlist-status")
def watchlist_status():

    db = SessionLocal()

    try:

        watchlist = db.execute(
            text("""
                SELECT company_name
                FROM ipo_watchlist
                ORDER BY company_name
            """)
        ).fetchall()

        result = []

        score_map = {
            "CONFIDENTIAL_FILING": 20,
            "CONFIDENTIAL_FILING_AMENDMENT": 30,
            "S1_FILED": 50,
            "S1_AMENDED": 70,
            "IPO_PRICING": 90,
            "IPO_PRICED": 100
        }

        for company in watchlist:

            company_name = company[0]

            latest = (
                db.query(
                    IPOOfficialEvent
                )
                .filter(
                    IPOOfficialEvent.company_name.ilike(
                        company_name
                    )
                )
                .order_by(
                    IPOOfficialEvent.detected_at.desc()
                )
                .first()
            )

            if not latest:

                result.append({
                    "company_name":
                        company_name,

                    "stage":
                        "NO_ACTIVITY",

                    "readiness_score":
                        0
                })

                continue

            result.append({

                "company_name":
                    company_name,

                "stage":
                    latest.event_type,

                "readiness_score":
                    score_map.get(
                        latest.event_type,
                        0
                    )
            })

        return result

    finally:

        db.close()
