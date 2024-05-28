from pathlib import Path

import json
import requests
import os

path_to_json = Path("./json_payloads/test_1.json")
input_payload = json.load(open(path_to_json))

api_token = os.environ['']
print(api_token[0:2])

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {api_token}"}


def query(payload: json) -> json:
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


data = query(input_payload)

print(data)
