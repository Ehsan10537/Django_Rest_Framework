
import openai
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def welcome_user(name):
    messages = [
    {"role": "system", "content": "Be funny. Greet the new user by name. Max 20 words."},
    {"role": "user", "content": f"{name} joined."}
    ]

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        max_tokens = 30,
        temperature = 0.8
    )

    return response.choices[0].message.content

