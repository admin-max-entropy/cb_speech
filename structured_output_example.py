import openai
import config

from pydantic import BaseModel
import src.data_utils

def fetch_a_script():
    container = src.data_utils.fed_speech_collection()
    info = container.find_one()
    return info["full_text"]

fetch_a_script()

class Views(BaseModel):
    inflation: str
    labor_market: str
    balance_sheet: str
    monetary_policy: str
    r_star: str
    policy_rate: str

class FedSpeechSummary(BaseModel):
    author: str
    keywords: list[str]
    views: Views

client = openai.OpenAI(api_key=config.OPEN_API_KEY)

class ResearchPaperExtraction(BaseModel):
    title: str
    authors: list[str]
    abstract: str
    keywords: list[str]

completion = client.beta.chat.completions.parse(
    model=config.MODEL,
    messages=[
        {"role": "system", "content": "You are an expert at Federal Reserve. "
                                      "You will be given unstructured text from a central bank speech and should convert it into the given structure."},
        {"role": "user", "content": fetch_a_script()}
    ],
    response_format=FedSpeechSummary,
)

research_paper = completion.choices[0].message.parsed
keywords = research_paper.keywords
views = research_paper.views

views_output = {}
for field in views.model_fields:
    views_output[field] = getattr(views, field, None )

print(views_output)