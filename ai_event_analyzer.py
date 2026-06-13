import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def analyze_headline(headline):

    prompt = f"""
You are an IPO intelligence analyst.

Analyze this headline:

{headline}

Return ONLY valid JSON:

{{
    "event_type": "",
    "importance": "",
    "summary": ""
}}

Event types can be:

IPO Signal
Funding Round
Product Launch
Partnership
Acquisition
Regulatory Action
Legal Issue
General News

Importance can be:

Low
Medium
High
Critical
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    try:
        return json.loads(result)

    except Exception:

        return {
            "event_type": "General News",
            "importance": "Low",
            "summary": headline
        }