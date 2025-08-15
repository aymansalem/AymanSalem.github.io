import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

# Blogger Atom feed
ATOM_FEED = "https://4-hoteliers.blogspot.com/feeds/posts/default"

# Output sitemap file
SITEMAP_FILE = "sitemap_blogger.xml"

# Fetch Atom feed
try:
    resp = requests.get(ATOM_FEED)
    resp.raise_for_status()
except Exception as e:
    print(f"Failed to fetch Atom feed: {e}")
    exit(1)

# Use lxml parser explicitly
soup = BeautifulSoup(resp.content, "lxml-xml")
entries = soup.find_all("entry")

# Build sitemap
now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

# Homepage
sitemap.append(f'  <url><loc>https://4-hoteliers.blogspot.com/?m=0</loc><lastmod>{now}</lastmod><priority>1.0</priority></url>')

# All posts
for entry in entries:
    link = entry.find("link")["href"]
    sitemap.append(f'  <url><loc>{link}?m=0</loc><lastmod>{now}</lastmod><priority>0.8</priority></url>')

sitemap.append('</urlset>')

# Write to file
with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap))

print(f"Sitemap generated: {SITEMAP_FILE} ({len(entries)+1} URLs)")
