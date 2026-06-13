def classify_event(headline):

    text = headline.lower()

    rules = {
        "IPO Signal": [
            "ipo",
            "public offering",
            "listing"
        ],

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
            "investigated",
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