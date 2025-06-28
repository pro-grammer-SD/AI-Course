import os
import requests
from dotenv import load_dotenv

load_dotenv()

username = "pro-grammer-sd"
token = os.getenv("KEY")

if not token:
    print("❌ No token found in environment variable 'KEY'")
    exit(1)

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

repos = []
page = 1

# Fetch ALL pages of repos
while True:
    url = f"https://api.github.com/user/repos?per_page=100&page={page}&type=owner"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ GitHub API Error:", response.json())
        exit(1)

    data = response.json()
    if not data:
        break

    repos.extend(data)
    page += 1

# Delete repos that start with "Class"
for repo in repos:
    name = repo.get("name", "")
    if name.startswith("Class"):
        delete_url = f"https://api.github.com/repos/{username}/{name}"
        del_response = requests.delete(delete_url, headers=headers)
        if del_response.status_code == 204:
            print(f"🧨 Deleted repo: {name}")
        elif del_response.status_code == 403:
            print(f"🚫 Forbidden deleting {name} (check delete_repo scope or admin rights)")
        elif del_response.status_code == 404:
            print(f"❓ Not found or already deleted: {name}")
        else:
            print(f"❌ Failed to delete {name}: {del_response.status_code} – {del_response.json()}")

print("✅ All matching 'Class*' repos processed.")
