import requests
from bs4 import BeautifulSoup

def search_articles(claim, max_results=20):
    url = "https://duckduckgo.com/html/"
    params = {"q": claim}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, params=params, timeout=15)

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    results = []
    for res in soup.select(".result__snippet")[:max_results]:
        title_tag = res.find_previous_sibling("a", class_="result__a")
        link = title_tag["href"] if title_tag else None

        results.append({
            "snippet": res.get_text(strip=True),
            "link": link
        })

    return results
