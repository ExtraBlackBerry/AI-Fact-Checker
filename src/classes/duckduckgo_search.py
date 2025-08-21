#john
import requests, os
from bs4 import BeautifulSoup

API_KEY = os.getenv("API_KEY")
CX_ID   = os.getenv("CX_ID")

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

def google_search(claim, focus):
    test = claim
    url = "https://customsearch.googleapis.com/customsearch/v1"
    print(claim)
    params = {
        "key": API_KEY,
        "cx": CX_ID,
        "q": test,
        "exactTerms": focus
    }
    r = requests.get(url, params=params)
    print(r)
    results = r.json().get("items", [])
    if not results:
        print("No results found.")
    ans = [{"snippet": item["snippet"], "link": item["link"], "display": item["displayLink"], "title": item["title"]} for item in results]
    return ans