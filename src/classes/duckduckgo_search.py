#john
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def search_articles(claim, max_results=20):
    time.sleep(3) 
    url = "https://duckduckgo.com/html/"
    params = {"q": claim}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, params=params, timeout=15)


    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for res in soup.select(".result__snippet")[:max_results]:
        a = res.find_previous_sibling("a", class_="result__a")
        article_url = None
        if a:
            redirect_url = "https://duckduckgo.com" + a["href"]

            parsed = urllib.parse.urlparse(redirect_url)
            query_params = urllib.parse.parse_qs(parsed.query)
            if "uddg" in query_params:
                article_url = urllib.parse.unquote(query_params["uddg"][0])
        print(f"Article URL: {article_url}")
        results.append({
            "snippet": res.get_text(strip=True),
            "link": article_url
        })

    return results
