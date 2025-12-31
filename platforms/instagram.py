import requests
from bs4 import BeautifulSoup

def fetch(username):
    url = f"https://imginn.com/{username}/"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    if r.status_code != 200:
        return {}

    soup = BeautifulSoup(r.text, "lxml")
    bio = soup.find("div", class_="bio")
    captions = [c.text.strip() for c in soup.select(".item-caption")][:20]

    return {
        "platform": "instagram",
        "bio": bio.text.strip() if bio else "",
        "posts": captions
    }
