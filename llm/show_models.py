import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_models():
    api_key = os.getenv("KICONNECT_API_KEY")

    if not api_key:
        raise RuntimeError("KICONNECT_API_KEY wurde nicht gefunden.")

    url = "https://chat.kiconnect.nrw/api/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    models = [model["id"] for model in response.json()["data"]]

    # Embedding-Modelle funktionieren nicht mit /chat/completions.
    return [
        model for model in models
        if "embedding" not in model.lower()
        and not model.lower().startswith("e5-")
    ]


if __name__ == "__main__":
    print("\n".join(get_models()))
