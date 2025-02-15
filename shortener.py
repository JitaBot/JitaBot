import os
import requests
import json

def shorten_url(long_url):
    token = os.environ.get("BITLY_API_TOKEN")  # Bitly APIトークン環境変数から取得
    url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "long_url": long_url,
        "domain": "bit.ly"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json().get("link")
    else:
        return f"URL短縮失敗: {response.status_code}"