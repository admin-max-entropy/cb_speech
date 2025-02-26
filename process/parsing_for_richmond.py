import requests
import bs4
import src.data_utils
from datetime import datetime
import src.parsing_utils
import config

container = src.data_utils.fed_speech_collection()

r = requests.get("https://www.richmondfed.org/press_room/speeches")
doc = bs4.BeautifulSoup(r.text, 'html.parser')

children = doc.find(class_='component comp-archive')
for item in children.find_all(class_="data__row"):
    title = item.find(class_="data__title").text
    link = item.find("a", href=True).attrs["href"]

    if container.find_one(dict(url=link)) is not None:
        continue

    try:
        pub_date = datetime.strptime(item.find(class_="data__date").text, "%b. %d, %Y")
    except:
        pub_date = datetime.strptime(item.find(class_="data__date").text, "%B %d, %Y")

    description = item.find(class_="data__summary").text
    author = item.find(class_="data__authors").text
    assert "tom barkin" in author.lower()

    content = bs4.BeautifulSoup(requests.get(f"https://www.richmondfed.org{link}").text, "html.parser")
    main = content.find("main")
    speech = main.find(class_="tmplt speech")
    title = speech.find(class_="tmplt__title")
    if title is None:
        title = ""
    else:
        title = title.text

    main_content = speech.find(class_="tmplt__content").find_all("p", class_=None)

    full_text = ""
    for row in main_content:
        full_text += row.text + "\n"

    summary = src.parsing_utils.generate_summary(full_text)
    print(len(summary), len(full_text))
    container.insert_one(dict(url=link, summary=summary, full_text=full_text,
                              date=pub_date, author=config.TBARKIN,
                              title=title, description=description))
