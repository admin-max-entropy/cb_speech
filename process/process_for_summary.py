import src.data_utils
from pydantic import BaseModel
import openai
import config

from typing import Literal

summarization_prompt = '''
    You will be provided with a speech from Federal Reserve FOMC members.
    Your goal will be to summarize the article following the schema provided.
    Here is a description of the parameters:
    - restricted_keywords: a list of keywords in the pre-defined list
    - keywords: a list of keywords 
    - views: array of view on inflation, labor market, balance sheet, monetary policy, r star, banking regulation and economic growth
    Note: If there is no view for certain topic, just leave it empty. For the keywords, please extract the keywords of the speech, rather than the author.
    Also, please pay attention to Federal Reserve facilities, such as SRF. For inflation, please make it detailed for CPI, PPI, etc.
'''

class Views(BaseModel):
    inflation: str
    labor_market: str
    balance_sheet: str
    monetary_policy: str
    r_star: str
    policy_rate: str
    banking_regulation: str
    economic_growth: str

class FedSpeechSummary(BaseModel):
    restricted_keywords: list[Literal["inflation", "labor market", "economic growth", "policy rate", "monetary policy",
    "balance sheet", "r star", "treasury market", "regulation", "repo"]]
    views: Views
    keywords: list[str]

client = openai.OpenAI(api_key=config.OPEN_API_KEY)

def get_summary(full_text):
    completion = client.beta.chat.completions.parse(
        model=config.MODEL,
        messages=[
            {"role": "system", "content": summarization_prompt},
            {"role": "user", "content": full_text}
    ],
    response_format=FedSpeechSummary,
    )
    research_paper = completion.choices[0].message.parsed
    keywords = research_paper.keywords
    views = research_paper.views
    restricted_keyword = research_paper.restricted_keywords

    views_output = {}
    for field in views.model_fields:
        views_output[field] = getattr(views, field, None )

    return dict(keywords=keywords, #views=views_output,
                restricted_keywords=restricted_keyword, views=views_output)


container = src.data_utils.fed_speech_collection()
output_container = src.data_utils.fed_speech_structured_output()
#output_container.drop()

for document in container.find():
    full_text = document.get("full_text")
    url = document.get("url")
    if output_container.find_one(dict(url=url)) is not None:
        continue
    summary = get_summary(full_text)
    full_info = summary
    full_info["url"] = url
    print(summary["keywords"])
    print(summary["restricted_keywords"])
    print(summary["views"])
    output_container.insert_one(full_info)