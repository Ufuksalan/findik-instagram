"""Her gün stories/ klasöründeki görselleri (en fazla 20) hikaye olarak paylaşır."""
import datetime
import glob
import json
import os
import time
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v21.0"
PER_DAY = 20


def call(url, data=None):
    body = urllib.parse.urlencode(data).encode() if data else None
    with urllib.request.urlopen(urllib.request.Request(url, data=body)) as r:
        return json.load(r)


def main():
    files = sorted(glob.glob("stories/*.jpg"))
    day = (datetime.date.today() - datetime.date(2026, 1, 1)).days
    n = min(PER_DAY, len(files))
    start = (day * n) % len(files)
    chosen = [files[(start + i) % len(files)] for i in range(n)]

    repo = os.environ["GITHUB_REPOSITORY"]
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    uid = os.environ["IG_USER_ID"]
    token = os.environ["IG_ACCESS_TOKEN"]

    for f in chosen:
        try:
            url = f"https://raw.githubusercontent.com/{repo}/{branch}/{f}"
            c = call(f"{API}/{uid}/media", {
                "image_url": url, "media_type": "STORIES", "access_token": token})
            for _ in range(10):
                st = call(f"{API}/{c['id']}?fields=status_code&access_token={token}")
                if st.get("status_code") in ("FINISHED", None):
                    break
                time.sleep(3)
            r = call(f"{API}/{uid}/media_publish", {
                "creation_id": c["id"], "access_token": token})
            print("Hikaye paylaşıldı:", f, r)
        except Exception as e:
            print("HATA:", f, e)
        time.sleep(5)


if __name__ == "__main__":
    main()
