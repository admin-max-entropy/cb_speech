import parsing_utils
import src.data_utils
import src.parsing_utils
import feedparser

container = src.data_utils.fed_speech_collection()
container.drop()

for author, link in src.parsing_utils.rss_links().items():
    feed = feedparser.parse(link)
    for entry in feed.entries:
        if container.find_one(dict(url=entry.link)) is not None:
            print(entry.link)
            continue

        date_eastern = src.data_utils.convert_fed_rss_time(entry.published)
        summary_, full_text_ = src.parsing_utils.speech_summary(entry.link)
        container.insert_one(dict(url=entry.link, summary=summary_, full_text=full_text_,
                                  author=author, date=date_eastern, description=entry.description,
                                  title=entry.title))
