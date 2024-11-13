from airflow.www.views import restrict_to_dev

import src.data_utils
from pydantic import BaseModel
import openai
import config

from typing import Literal

container = src.data_utils.fed_speech_collection()
output_container = src.data_utils.fed_speech_structured_output()

keys = []
for document in output_container.find():
    keys += document["keywords"]

keys = list(set(keys))
print(len(keys))
for key in keys:
    print(key)