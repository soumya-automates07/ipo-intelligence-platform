def classify_event(headline):

    text = headline.lower()

    # Ignore junk/opinion
    ignore_phrases = [
        "better buy",
        "what does it mean",
        "ipo race",
        "ipo buzz",
        "opinion",
        "analysis",
        "valuation",
        "ponzi scheme",
        "parallels to",
        "what happens now"
    ]

    for phrase in ignore_phrases:
        if phrase in text:
            return "General News"

    # Tier 1 - Highest priority IPO milestones
    high_priority = [
        "files for ipo",
        "filed for ipo",
        "confidentially files",
        "confidentially filed",
        "ipo filing",
        "goes public",
        "going public",
        "nasdaq debut",
        "public debut",
        "ipo priced",
        "prices shares",
        "largest ipo",
        "public offering"
    ]

    for keyword in high_priority:
        if keyword in text:
            return "IPO Signal"

    rules = {
        "Funding Round": [
            "funding",
            "raises",
            "raised",
            "investment"
        ],

        "Acquisition": [
            "acquire",
            "acquisition",
            "buyout"
        ],

        "Product Launch": [
            "launch",
            "introduces",
            "unveils"
        ],

        "Regulatory Action": [
            "investigation",
            "probe",
            "regulator"
        ],

        "Legal Issue": [
            "lawsuit",
            "court",
            "legal"
        ],

        "Partnership": [
            "partnership",
            "collaboration"
        ]
    }

    for event_type, keywords in rules.items():

        for keyword in keywords:

            if keyword in text:
                return event_type

    return "General News"
