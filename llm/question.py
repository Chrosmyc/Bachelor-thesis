import os
from pathlib import Path

import requests
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)


def ask_question(question, risks, mitigations, relationships):
    api_key = os.getenv("KICONNECT_API_KEY")

    if not api_key:
        raise RuntimeError("KICONNECT_API_KEY wurde nicht gefunden.")

    url = "https://chat.kiconnect.nrw/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Answer the question based exclusively on the following knowledge base.

If the answer cannot be found in the data, answer:
This is not in the knowledge base.

<RISKS>
{risks}
</RISKS>

<MITIGATIONS>
{mitigations}
</MITIGATIONS>

<RELATIONSHIPS>
{relationships}
</RELATIONSHIPS>

Question:
{question}
"""

    data = {
        "model": "gpt-5.5",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You answer questions about legacy system modernization. "
                    "Use only the provided knowledge base "
                    "and cite relevant risk, mitigation, and relationship IDs."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=120
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]