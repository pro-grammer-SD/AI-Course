import requests

files = {'file': open("aura.pdf", "rb")}
res = requests.post("http://127.0.0.1:8500/summarize/", files=files)
print(res.json()['summary'])
