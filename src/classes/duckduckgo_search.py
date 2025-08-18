#john
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def search_articles(claim, max_results=20):
    url = "https://duckduckgo.com/html/"
    params = {"q": claim}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, params=params, timeout=15)


    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for res in soup.select(".result__snippet")[:max_results]:
        results.append({
            "snippet": res.get_text(strip=True)
        })

    return results
