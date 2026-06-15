from analysis.event_classifier import classify_event

headlines = [
    "OpenAI raises $5 billion",
    "SpaceX IPO expected in 2028",
    "Anthropic launches Claude 5",
    "OpenAI investigated by regulators"
]

for h in headlines:
    print(h)
    print("=>", classify_event(h))
    print()