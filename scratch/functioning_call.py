import openai
import json
import config

# set openai api key
openai.api_key = config.OPEN_API_KEY

def get_completion(messages, model=config.MODEL,
                   temperature=0, max_tokens=300, tools=None, tool_choice=None):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        tools=tools,
        tool_choice=tool_choice
    )
    return response.choices[0].message

def get_current_weather(location, unit):
    """Get the current weather in a given location"""
    weather = {
        "location": location,
        "temperature": "50",
        "unit": unit,
    }

    return json.dumps(weather)

# define a function as tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location", "unit"],
            },
        },
    }
]

messages = [
    {
        "role": "user",
        "content": "What is the weather like in London in celsius?"
    }
]

response = get_completion(messages, tools=tools)
args = json.loads(response.tool_calls[0].function.arguments)
result = get_current_weather(**args)
print(result)
