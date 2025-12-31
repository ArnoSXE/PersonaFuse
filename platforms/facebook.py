import requests
from bs4 import BeautifulSoup

def fetch(username):
    url = f"https://www.facebook.com/public/{username}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    if r.status_code != 200:
        return {}

    soup = BeautifulSoup(r.text, "lxml")
    snippets = [d.text.strip() for d in soup.find_all("div")][:10]

    return {"platform": "facebook", "snippets": snippets}
