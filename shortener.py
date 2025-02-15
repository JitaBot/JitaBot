import requests
import os

def shorten_url(long_url):
    api_token = os.environ.get("BITLY_API_TOKEN")
    url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = {
        "long_url": long_url,
        "domain": "bit.ly"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("link")
    else:
        return f"URL短縮失敗: {response.status_code}"