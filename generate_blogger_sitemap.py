import requests
from bs4 import BeautifulSoup
import datetime

SITEMAP_FILE = "sitemap_blogger.xml"
BLOG_URL = "https://4-hoteliers.blogspot.com"
ATOM_FEED = f"{BLOG_URL}/feeds/posts/default?alt=rss"

def fetch_blogger_posts():
    urls = []
    try:
        resp = requests.get(ATOM_FEED, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "xml")
        for entry in soup.find_all("link", rel="alternate"):
            href = entry.get("href")
            if href:
                urls.append(href + "?m=0")
    except Exception as e:
        print(f"Failed to fetch Atom feed: {e}")
    return urls

def generate_sitemap(urls):
    now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "+00:00"
    sitemap_entries = []
    for url in urls:
        priority = "1.00" if url.rstrip("?m=0") == BLOG_URL else "0.80"
        sitemap_entries.append(f'  <url><loc>{url}</loc><lastmod>{now}</lastmod><priority>{priority}</priority></url>')

    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap_content += "\n".join(sitemap_entries)
    sitemap_content += "\n</urlset>"

    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(sitemap_content)

if __name__ == "__main__":
    urls = fetch_blogger_posts()
    if BLOG_URL not in urls:
        urls.insert(0, BLOG_URL + "?m=0")
    generate_sitemap(urls)
    print(f"Sitemap updated with {len(urls)} URLs.")
