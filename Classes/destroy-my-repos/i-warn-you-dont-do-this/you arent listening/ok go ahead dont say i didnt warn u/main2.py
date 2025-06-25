import os
import subprocess
import requests
from pathlib import Path

username = "pro-grammer-sd"
token = os.environ["KEY"]

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

base_dir = Path("Python-Foolproof-Course")
base_dir.mkdir(exist_ok=True)

repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
repos = requests.get(repos_url, headers=headers).json()

for repo in repos:
    name = repo["name"]
    if name.startswith("Class"):
        clone_url = repo["clone_url"].replace("https://", f"https://{username}:{token}@")
        target_dir = base_dir / name
        print(f"📥 Cloning {name}...")
        subprocess.run(["git", "clone", clone_url, str(target_dir)])

# Init new repo
os.chdir(base_dir)
subprocess.run(["git", "init"])
subprocess.run(["git", "remote", "add", "origin", f"https://github.com/{username}/Python-Foolproof-Course.git"])
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Combined all Class repos"])
subprocess.run(["git", "branch", "-M", "main"])
subprocess.run(["git", "push", "-u", "origin", "main"])
