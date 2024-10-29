import requests
import bs4
import parsing_utils
import config
import src.data_utils
import pytz
from datetime import datetime

container = src.data_utils.fed_speech_collection()

r = requests.get("https://www.atlantafed.org/rss/speechindex")
doc = bs4.BeautifulSoup(r.text, 'html.parser')

for item in doc.findAll('item'):
    links = item.find("guid").previous_siblings
    for link in links:
        link = link.strip()
        link = link.replace("\r\n", "")
        title = item.find('title').text
        date = item.find('pubdate').text
        date = datetime.strptime(date, f"%A, %d %b %Y %H:%M:%S EST")
        date = date.replace(tzinfo=pytz.timezone('US/Eastern'))
        description = item.find('description').text
        if container.find_one(dict(url=link)) is not None:
            continue
        content = requests.get(link)
        content_soup = bs4.BeautifulSoup(content.text, 'html.parser')
        next_info = content_soup.next
        full_content = content_soup.find("div", class_="main-content")
        content = full_content.find_all("p", class_=None)
        next_content = full_content.find("p", class_=None).next.get_text()
        assert "Raphael Bostic" in next_content
        full_text = ""
        for row in content:
            full_text += row.text + "\n"
        summary = parsing_utils.generate_summary(full_text)
        print(len(full_text), len(summary))

        container.insert_one(dict(url=link, summary=summary, full_text=full_text,
                                  date=date, author=config.RBOSTIC,
                                  title=title, description=description))

        break