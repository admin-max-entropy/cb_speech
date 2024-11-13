from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import pytz

def master_database():
    db_password = "DmUKR0yONjMExVNN"
    uri = f"mongodb+srv://admin:{db_password}@cluster0.vg3mk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client["max_entropy"]

def fed_speech_collection():
    return master_database()["fed_speech_summary"]

def fed_speech_structured_output():
    return master_database()["fed_speech_structured_output"]

def convert_fed_rss_time(input_time):

    if "GMT" in input_time:
        tz_name = 'GMT'
        tz = pytz.timezone(tz_name)
    elif "CST" in input_time:
        tz_name = "CST"
        tz = pytz.timezone("US/Central")
    else:
        raise RuntimeError("unsupported time format")

    eastern = pytz.timezone('US/Eastern')
    date = datetime.strptime(input_time, f"%a, %d %b %Y %H:%M:%S {tz_name}")
    date_tz = tz.localize(date)
    date_eastern = date_tz.astimezone(eastern)
    return date_eastern
