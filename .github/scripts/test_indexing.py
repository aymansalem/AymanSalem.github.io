import os
import json
import requests
import xml.etree.ElementTree as ET
from google.oauth2 import service_account
from googleapiclient.discovery import build
from urllib.parse import urlparse

# === CONFIG ===
GITHUB_SITEMAP_URL = "https://aymansalem.github.io/sitemap.xml"
BLOGGER_FEED_URL = "https://hotelierhub.blogspot.com/feeds/posts/default?alt=rss"

# === LOAD GOOGLE CREDENTIALS ===
google_json = os.environ.get("GOOGLE_JSON")
if not google_json:
    raise ValueError("❌ GOOGLE_JSON secret is missing!")

try:
    service_account_info = json.loads(google_json)
except json.JSONDecodeError as e:
    raise ValueError(f"❌ GOOGLE_JSON is not valid JSON: {e}")

creds = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/indexing"]
)
print("✅ Google credentials loaded successfully")

# === BUILD INDEXING API CLIENT ===
service = build("indexing", "v3", credentials=creds)

def fetch_github_pages():
    """Fetch URLs from GitHub sitemap and normalize pretty URLs."""
    urls = []
    resp = requests.get(GITHUB_SITEMAP_URL)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)

    for loc in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        url = loc.text.strip()
        # Optional: normalize .html -> no extension for pretty URLs
        if url.endswith(".html") and not url.endswith("index.html"):
            url = url[:-5]  # remove ".html"
        urls.append(url)
    print(f"🔍 Found {len(urls)} GitHub URLs")
    return urls

def fetch_blogger_posts():
    """Fetch URLs from Blogger RSS feed."""
    urls = []
    resp = requests.get(BLOGGER_FEED_URL)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)

    for link in root.findall(".//{http://www.w3.org/2005/Atom}link"):
        href = link.attrib.get("href", "")
        rel = link.attrib.get("rel", "")
        if rel == "alternate" and href.startswith("http"):
            urls.append(href)
    print(f"🔍 Found {len(urls)} Blogger URLs")
    return urls

def send_to_indexing_api(url):
    """Send a single URL to Google's Indexing API."""
    try:
        resp = service.urlNotifications().publish(
            body={"url": url, "type": "URL_UPDATED"}
        ).execute()
        print(f"✅ Indexed: {url}")
        return True
    except Exception as e:
        if "Permission denied" in str(e):
            print(f"❌ 403 Permission Denied: {url}")
        else:
            print(f"❌ Failed to index {url}: {e}")
        return False

# === MAIN PROCESS ===
if __name__ == "__main__":
    github_urls = fetch_github_pages()
    blogger_urls = fetch_blogger_posts()

    all_urls = list(set(github_urls + blogger_urls))
    print(f"📢 Sending {len(all_urls)} total URLs to Indexing API...\n")

    success_count = 0
    fail_count = 0

    for url in all_urls:
        if send_to_indexing_api(url):
            success_count += 1
        else:
            fail_count += 1

    print("\n📊 SUMMARY")
    print(f"   ✅ Success: {success_count}")
    print(f"   ❌ Failed: {fail_count}")
