import os
import requests
from dotenv import load_dotenv
from knowledge_base import knowledge_base

load_dotenv()

api_key = os.getenv("KICONNECT_API_KEY")

url = "https://chat.kiconnect.nrw/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

frage = "Was ist das Ziel der Bachelorarbeit?"

prompt = f"""
Nutze nur die folgende Knowledge Base als Kontext.

Wenn die Antwort nicht in der Knowledge Base steht,
sage: Das steht nicht in der Knowledge Base.

Knowledge Base:
{knowledge_base}

Frage:
{frage}
"""

data = {
    "model": "gpt-5.5",
    "messages": [
        {
            "role": "system",
            "content": "Du beantwortest Fragen auf Basis einer Knowledge Base."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
answer = response.json()["choices"][0]["message"]["content"]
print(answer)