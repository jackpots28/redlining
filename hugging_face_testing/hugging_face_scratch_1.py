import json
import os
import sys
from pathlib import Path

import requests

project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), './'))
sys.path.insert(0, os.path.abspath(project_root))

path_to_json = Path(f"{project_root}/json_payloads/test_1.json")
input_payload = json.load(open(path_to_json))

api_token = os.environ['api_token']
print(api_token[0:2])

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {api_token}"}


def query(payload: json) -> json:
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


data = query(input_payload)

print(data)
