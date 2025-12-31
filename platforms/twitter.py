import requests
from bs4 import BeautifulSoup

def fetch(username):
    url = f"https://nitter.net/{username}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    if r.status_code != 200:
        return {}

    soup = BeautifulSoup(r.text, "lxml")
    posts = [p.text.strip() for p in soup.select(".tweet-content")][:20]

    return {"platform": "twitter", "posts": posts}
