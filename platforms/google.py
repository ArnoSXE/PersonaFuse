import requests
from bs4 import BeautifulSoup

def fetch(username):
    url = f"https://www.google.com/search?q={username}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    if r.status_code != 200:
        return {}

    soup = BeautifulSoup(r.text, "lxml")
    results = [h.text for h in soup.select("h3")][:10]

    return {"platform": "google", "mentions": results}
