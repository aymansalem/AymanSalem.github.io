import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Your Blogger Atom feed URL
ATOM_FEED = "https://4-hoteliers.blogspot.com/feeds/posts/default"

# Output sitemap file
SITEMAP_FILE = "sitemap_blogger.xml"

# Fetch Atom feed
resp = requests.get(ATOM_FEED)
resp.raise_for_status()

soup = BeautifulSoup(resp.content, "xml")
entries = soup.find_all("entry")

# Start building sitemap
today = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

# Add homepage
sitemap.append(f'  <url><loc>https://4-hoteliers.blogspot.com/?m=0</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>')

# Add all posts
for entry in entries:
    link = entry.find("link")["href"]
    sitemap.append(f'  <url><loc>{link}?m=0</loc><lastmod>{today}</lastmod><priority>0.8</priority></url>')

sitemap.append('</urlset>')

# Write sitemap
with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap))

print(f"Sitemap generated: {SITEMAP_FILE}")
