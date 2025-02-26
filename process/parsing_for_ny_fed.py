import datetime
import bs4
import requests
from numpy.ma.extras import row_stack
from urllib3.util.response import assert_header_parsing

from src import parsing_utils
import src.data_utils
import config

container = src.data_utils.fed_speech_collection()
# container.drop()

def __find_info(target_link):

    if "speeches" not in target_link:
        return None

    content = requests.get(target_link)
    content_soup = bs4.BeautifulSoup(content.text, 'html.parser')
    contact_infos = content_soup.findAll("div", class_="ts-contact-info")

    for row in contact_infos:
        href_info = row.find(href=True)
        if href_info is not None:
            author = href_info.text
            if author in ["John C. Williams", "Roberto Perli"]:
                date = bs4.BeautifulSoup(contact_infos[0].text).text.replace("\r\n", "")
                date = date.split("Posted")[0]
                date = date.strip()
                print(date)
                date = datetime.datetime.strptime(date, "%B %d, %Y")

                if date <= datetime.datetime(2016, 1, 1):
                    return None

                if author == "John C. Williams":
                    author = config.JWILLAIM
                else:
                    author = config.PERLI
                return author, date

    return None

speeches = requests.get("https://www.newyorkfed.org/press/#speeches")
doc = bs4.BeautifulSoup(speeches.text, 'xml')
sub_title = doc.findAll(class_="tablTitle")

for item in sub_title:
    link_info = item.find("a", href=True)
    if link_info is None:
        continue
    title = link_info.text
    target_link = link_info.attrs["href"]
    if "speeches" not in target_link:
        continue

    target_link = "https://www.newyorkfed.org/" + target_link
    if container.find_one(dict(url=target_link)) is not None:
        continue

    author_info = __find_info(target_link)
    if author_info is None:
        continue

    author, date = author_info
    content = requests.get(target_link)
    content_soup = bs4.BeautifulSoup(content.text, 'html.parser')
    tags = content_soup.find_all("div", class_="ts-article-text")[0]
    sub_tags = tags.find_all("p", class_=None)
    full_text = ""
    for tag in sub_tags:
        full_text += tag.text + "\n"

    summary = parsing_utils.generate_summary(full_text)
    print(author, date, len(full_text), len(summary))

    container.insert_one(dict(url=target_link, summary=summary, full_text=full_text,
                              date=date, author=author, title=title, description=""))
