import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("KICONNECT_API_KEY")

url = "https://chat.kiconnect.nrw/api/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)