import requests

session = requests.get("https://opentdb.com/api_token.php?command=request").json()
token = session["token"]

def get_data():
    url = f"https://opentdb.com/api.php?amount=1&category=17&difficulty=easy&type=multiple&token={token}"
    res = requests.get(url).json()
    main_data = res.get("results", [])
    return main_data[0] if main_data else {}
