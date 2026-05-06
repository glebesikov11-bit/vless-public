import json
import requests
import base64
from datetime import datetime
import os

PRIVATE_REPO = "glebesikov11-bit/vless-private"

def get_users():
    url = f"https://api.github.com/repos/{PRIVATE_REPO}/contents/users.json"
    # Токен GitHub Actions использует свой, встроенный!
    r = requests.get(url)
    if r.status_code == 200:
        content = base64.b64decode(r.json()["content"]).decode("utf-8")
        return json.loads(content)
    return []

def get_configs():
    url = "https://api.github.com/repos/glebesikov11-bit/vless-public/contents/configs"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    files = r.json()
    configs = []
    for file in files:
        if file["name"].endswith(".conf"):
            content = requests.get(file["download_url"]).text
            configs.append(content)
    return configs

def main():
    users = get_users()
    today = datetime.today().date()
    templates = get_configs()
    
    all_links = []
    for user in users:
        expire = user.get("expire_at") or user.get("premium_until")
        if expire and datetime.strptime(expire, "%Y-%m-%d").date() >= today:
            for template in templates:
                link = template.replace("USER_ID", user["id"])
                all_links.append(link)
    
    with open("sub.txt", "w") as f:
        f.write("\n".join(all_links))

if __name__ == "__main__":
    main()
