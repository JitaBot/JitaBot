import requests
import os
import json

def check_bitly_api():
    api_token = os.environ.get("BITLY_API_TOKEN")
    url = "https://api-ssl.bitly.com/v4/user"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"Bitly API使用状況: {data}")
    else:
        print(f"Bitly APIエラー: {response.status_code}, {response.text}")

check_bitly_api()