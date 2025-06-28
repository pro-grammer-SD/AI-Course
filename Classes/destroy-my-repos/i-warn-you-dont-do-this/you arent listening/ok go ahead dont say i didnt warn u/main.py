import requests
from dotenv import load_dotenv
import os

load_dotenv()

username = "pro-grammer-sd"
token = os.environ["KEY"]

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

url = f"https://api.github.com/users/{username}/repos?per_page=100"

response = requests.get(url, headers=headers)
repos = response.json()

if not isinstance(repos, list):
    print("❌ GitHub API Error:")
    print(repos)
    exit(1)

changed_any = False

for repo in repos:
    name = repo["name"]
    if name.startswith("Class") and not repo["private"]:
        patch_url = f"https://api.github.com/repos/{username}/{name}"
        patch_data = {"private": True}
        patch_response = requests.patch(patch_url, headers=headers, json=patch_data)
        if patch_response.status_code == 200:
            print(f"✅ Made '{name}' private")
            changed_any = True
        else:
            print(f"❌ Failed on '{name}': {patch_response.status_code}")

if not changed_any:
    print("👌 Everything was already private. Nothing to do.")
else:
    print("🎉 All applicable repos have been cloaked!")
