import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Your Blogger Atom feed URL (max-results can be increased if you have >500 posts)
BLOGGER_FEED = "https://4-hoteliers.blogspot.com/feeds/posts/default?max-results=500"

# File to save sitemap
OUTPUT_FILE = "sitemap_blogger.xml"

def fetch_blogger_posts():
    """Fetch all post URLs and last updated dates from Blogger Atom feed"""
    print("Fetching Blogger feed...")
    response = requests.get(BLOGGER_FEED)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    posts = []
    for entry in root.findall("atom:entry", ns):
        link = entry.find("atom:link[@rel='alternate']", ns)
        updated = entry.find("atom:updated", ns)
        if link is not None and updated is not None:
            url = link.attrib["href"] + "?m=0"
            lastmod = updated.text
            posts.append((url, lastmod))
    print(f"Found {len(posts)} posts.")
    return posts

def generate_sitemap(posts):
    """Generate XML sitemap content"""
    urlset_open = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    urlset_close = "\n</urlset>"

    urls = []
    for url, lastmod in posts:
        urls.append(f"""
  <url>
    <loc>{url}</loc>
    <lastmod>{lastmod}</lastmod>
    <priority>0.80</priority>
  </url>""")

    # Add homepage with higher priority
    urls.insert(0, f"""
  <url>
    <loc>https://4-hoteliers.blogspot.com/?m=0</loc>
    <lastmod>{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")}</lastmod>
    <priority>1.00</priority>
  </url>""")

    return urlset_open + "".join(urls) + urlset_close

if __name__ == "__main__":
    posts = fetch_blogger_posts()
    sitemap_content = generate_sitemap(posts)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print(f"Sitemap saved to {OUTPUT_FILE}")
