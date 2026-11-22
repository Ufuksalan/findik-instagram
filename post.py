"""Her gün images/ klasöründen sıradaki reklam görselini Instagram'a paylaşır.

Gerekli ortam değişkenleri:
  IG_USER_ID      Instagram Business hesabının ID'si
  IG_ACCESS_TOKEN Meta (Graph API) erişim anahtarı
  GITHUB_REPOSITORY (Actions'ta otomatik) örn. kullanici/findik-instagram
"""
import datetime
import json
import os
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v21.0"


def call(url, data):
    body = urllib.parse.urlencode(data).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=body)) as r:
        return json.load(r)


def main():
    posts = json.load(open("posts.json", encoding="utf-8"))
    # Her gün sıradaki gönderi; liste bitince başa döner
    day = (datetime.date.today() - datetime.date(2026, 1, 1)).days
    post = posts[day % len(posts)]

    repo = os.environ["GITHUB_REPOSITORY"]
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    image_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{post['image']}"

    uid = os.environ["IG_USER_ID"]
    token = os.environ["IG_ACCESS_TOKEN"]

    container = call(f"{API}/{uid}/media", {
        "image_url": image_url,
        "caption": post["caption"],
        "access_token": token,
    })
    result = call(f"{API}/{uid}/media_publish", {
        "creation_id": container["id"],
        "access_token": token,
    })
    print("Paylaşıldı:", post["image"], result)


if __name__ == "__main__":
    main()
