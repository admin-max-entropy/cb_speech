import datetime
import bs4
import requests
import parsing_utils
import src.data_utils
import config

container = src.data_utils.fed_speech_collection()
headers = {
    "x-api-key": "408ab2cb55365557e2a47462e5d782b1",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}
r = requests.get("https://fedinprint.org/rss/newyork.rss", headers=headers)
doc = bs4.BeautifulSoup(r.text, 'xml')

for item in doc.findAll('item'):
    title = item.find('title').get_text()
    author = item.find('dc:creator').get_text()
    link = item.find('link').get_text()
    series = item.find('bibo:series').get_text()
    description = item.find('description').get_text()

    if author != "Williams, John C." or series != "Speech":
        continue

    if container.find_one(dict(url=link)) is not None:
        continue

    info = requests.get(link, headers=headers)
    info_soup = bs4.BeautifulSoup(info.text, 'html.parser')
    links = info_soup.findAll('a', href=True)

    for row in links:

        if "https://www.newyorkfed.org/newsevents/speeches" not in row.text:
            continue

        date_str =item.find('dc:date').get_text()
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        target_link = row.text
        content = requests.get(target_link)
        content_soup = bs4.BeautifulSoup(content.text, 'html.parser')
        tags = content_soup.find_all("div", class_="ts-article-text")[0]
        sub_tags = tags.find_all("p", class_=None)
        full_text = ""
        for tag in sub_tags:
            full_text += tag.text + "\n"
        print(len(full_text))
        summary = parsing_utils.generate_summary(full_text)
        print(len(summary))
        container.insert_one(dict(url=target_link, summary=summary, full_text=full_text,
                                  date=date, author=config.JWILLAIM, title=title, description=description))
