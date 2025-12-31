import json

def save(data, filename="personafuse_output.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
