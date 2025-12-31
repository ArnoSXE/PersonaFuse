import requests

HEADERS = {"User-Agent": "PersonaFuse-OSINT"}

def fetch(username):
    url = f"https://www.reddit.com/user/{username}/about.json"
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code != 200:
        return {}

    d = r.json().get("data", {})
    return {
        "platform": "reddit",
        "bio": d.get("subreddit", {}).get("public_description", ""),
        "created": d.get("created_utc", 0)
    }
