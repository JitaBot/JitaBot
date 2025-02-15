import os
import requests
import json

def shorten_url(long_url):
    try:
        api_token = os.environ.get("BITLY_API_TOKEN")
        url = "https://api-ssl.bitly.com/v4/shorten"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        data = {"long_url": long_url, "domain": "bit.ly"}
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return response.json().get("link")
        else:
            print(f"URL短縮失敗: {response.status_code}, {response.text}")
            return "URL短縮に失敗したで…"

    except Exception as e:
        print(f"URL短縮エラー: {e}")
        return "URL短縮エラー発生"