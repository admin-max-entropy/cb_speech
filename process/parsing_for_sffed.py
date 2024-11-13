import requests
import bs4
import src.parsing_utils
import config
import src.data_utils
from datetime import datetime

container = src.data_utils.fed_speech_collection()

r = requests.get("https://www.frbsf.org/news-and-media/speeches/mary-c-daly/")
doc = bs4.BeautifulSoup(r.text, 'html.parser')

items = doc.findAll(class_="wp-block-post")


for item in items:
    link_info = item.find("a", href=True)
    title = link_info.text
    link = link_info.attrs["href"]
    if container.find_one(dict(url=link)) is not None:
        continue
    date_str = item.find(class_="wp-block-post-date").text
    date = datetime.strptime(date_str, "%B %d, %Y")
    description = item.find(class_="wp-block-post-excerpt__excerpt")
    content = requests.get(link)
    content_soup = bs4.BeautifulSoup(content.text, 'html.parser')
    entry = content_soup.find(class_="entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow")
    full_text = ""

    for content in entry.contents:
        sub_soup = bs4.BeautifulSoup(content.text, 'html.parser')
        if sub_soup.text.lower() in ["footnotes", "references"]:
            break
        else:
            full_text += sub_soup.text + "\n"
    summary = src.parsing_utils.generate_summary(full_text)
    print(len(full_text), len(summary))

    container.insert_one(dict(url=link, summary=summary, full_text=full_text,
                                  date=date, author=config.MDALY,
                                  title=title, description=description.text))
