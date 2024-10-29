import openai
import requests
import bs4
import config

openai.api_key = config.OPEN_API_KEY

def generate_summary(text):
    response = openai.chat.completions.create(
        model=config.MODEL,
        messages=[dict(content=f"Please summarize the following text:\n{text}\n\nSummary:", role="user")],
        temperature=0,
    )
    summary = response.choices[0]
    summary = summary.message.content
    return summary

def speech_summary(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    tags = soup.find_all("p", class_=None)
    full_text = ""

    for tag in tags:
        full_text += tag.text + "\n"
    print(len(full_text))
    summary = generate_summary(full_text)
    print(len(summary))
    return summary, full_text

def rss_links():
    names_map = {config.JPOW: "https://www.federalreserve.gov/feeds/s_t_powell.xml",
                 config.MBARR: "https://www.federalreserve.gov/feeds/s_t_barr.xml",
                 config.CWALLER: "https://www.federalreserve.gov/feeds/s_t_waller.xml",
                 config.PJEFF: "https://www.federalreserve.gov/feeds/s_t_jefferson.xml",
                 config.MBOW: "https://www.federalreserve.gov/feeds/m_w_Bowman.xml",
                 config.AKUGLER: "https://www.federalreserve.gov/feeds/s_t_kugler.xml",
                 config.LCOOK: "https://www.federalreserve.gov/feeds/s_t_cook.xml",
                 config.LOGAN: "https://www.dallasfed.org/rss/speeches.xml",
                 }
    return names_map
