import config
from openai import OpenAI

client = OpenAI(api_key=config.OPEN_API_KEY)

stream = client.chat.completions.create(
    model=config.MODEL,
    messages=[
        {"role": "user", "content": "what is an apple?"}
    ],
    stream=False,
)

print(stream.choices[0].message)