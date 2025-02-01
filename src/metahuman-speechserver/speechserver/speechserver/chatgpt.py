import json
from openai import OpenAI
from speechserver.config import config

client = OpenAI(api_key=config.openai_api_key)
model = 'gpt-4o'

def completion(messages):
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=256,
        temperature=0.9
    )

    message = {
        'role': completion.choices[0].message.role,
        'content': completion.choices[0].message.content
    }

    messages.append(message)
