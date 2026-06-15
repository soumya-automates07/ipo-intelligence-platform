from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def generate_summary(company, description):

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are an IPO intelligence analyst.

    Company:
    {company}

    News:
    {description}

    Write a concise 2-sentence executive summary explaining
    why this development matters from an IPO or business
    intelligence perspective.
    """

    response = model.generate_content(prompt)

    return response.text


def generate_risk_level(company, description):

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are an IPO risk analyst.

    Company:
    {company}

    News:
    {description}

    Return ONLY ONE WORD:

    LOW
    MEDIUM
    HIGH

    No explanation.
    """

    response = model.generate_content(prompt)

    return response.text.strip().upper()
