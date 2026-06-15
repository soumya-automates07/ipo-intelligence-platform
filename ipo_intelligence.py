EVENT_INTELLIGENCE = {

    "CONFIDENTIAL_FILING": {

        "importance":
            "MEDIUM",

        "stage":
            "🟡 Early Stage",

        "readiness_score":
            20,

        "risk":
            "HIGH",

        "expected_next":
            "Public S-1 Filing",

        "timeline":
            "6-12 Months",

        "summary":
            (
                "The company confidentially submitted IPO "
                "paperwork to regulators. This is typically "
                "the earliest official indication that IPO "
                "preparations are underway."
            ),

        "intelligence":
            (
                "Management has initiated the formal IPO "
                "process while keeping financial disclosures "
                "private. Regulatory review is likely in "
                "progress. Companies at this stage often "
                "remain months away from public trading."
            )
    },

    "CONFIDENTIAL_FILING_AMENDMENT": {

        "importance":
            "MEDIUM",

        "stage":
            "🟡 Early Stage",

        "readiness_score":
            30,

        "risk":
            "HIGH",

        "expected_next":
            "Public S-1 Filing",

        "timeline":
            "4-10 Months",

        "summary":
            (
                "The company updated its confidential IPO "
                "submission as discussions with regulators "
                "continue."
            ),

        "intelligence":
            (
                "Multiple confidential amendments usually "
                "indicate ongoing SEC review and preparation "
                "for eventual public disclosure. The IPO "
                "process remains active."
            )
    },

    "S1_FILED": {

        "importance":
            "HIGH",

        "stage":
            "🟠 Filing Stage",

        "readiness_score":
            50,

        "risk":
            "MEDIUM",

        "expected_next":
            "S-1 Amendment",

        "timeline":
            "2-6 Months",

        "summary":
            (
                "The company publicly filed its registration "
                "statement and formally entered the IPO "
                "process."
            ),

        "intelligence":
            (
                "Public filing provides investors visibility "
                "into the business, financials, risks, and "
                "offering structure. The IPO process has "
                "moved into a significantly more advanced "
                "stage."
            )
    },

    "S1_AMENDED": {

        "importance":
            "HIGH",

        "stage":
            "🟠 Filing Stage",

        "readiness_score":
            70,

        "risk":
            "MEDIUM",

        "expected_next":
            "IPO Pricing",

        "timeline":
            "1-4 Months",

        "summary":
            (
                "The company amended its registration "
                "statement with updated information."
            ),

        "intelligence":
            (
                "S-1 amendments often include updated "
                "financials, revised offering terms, or SEC "
                "feedback responses. Multiple amendments can "
                "occur before pricing."
            )
    },

    "IPO_PRICING": {

        "importance":
            "CRITICAL",

        "stage":
            "🔴 Final Stage",

        "readiness_score":
            90,

        "risk":
            "LOW",

        "expected_next":
            "IPO Priced",

        "timeline":
            "Days",

        "summary":
            (
                "IPO pricing details have been published and "
                "the offering is approaching public trading."
            ),

        "intelligence":
            (
                "Bookbuilding is largely complete and final "
                "investor allocations are being determined. "
                "Public market debut is typically imminent."
            )
    },

    "IPO_PRICED": {

        "importance":
            "CRITICAL",

        "stage":
            "🔴 Final Stage",

        "readiness_score":
            100,

        "risk":
            "LOW",

        "expected_next":
            "Public Trading",

        "timeline":
            "Immediate",

        "summary":
            (
                "The IPO has been priced and share allocation "
                "finalized."
            ),

        "intelligence":
            (
                "The offering process is effectively complete. "
                "The company is expected to begin trading or "
                "has already begun trading on a public market."
            )
    }
}