import requests as r

def fetch():
    response = r.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    data = response.json()
    return data["text"]
