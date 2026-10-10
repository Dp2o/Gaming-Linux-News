import json
import datetime
import urllib.request
import xml.etree.ElementTree as ET

# Free public Linux gaming news feed (No login or keys needed)
RSS_URL = "https://www.gamingonlinux.com/article_rss.php"

def fetch_news():
    try:
        req = urllib.request.Request(
            RSS_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        items = []
        
        for item in root.findall('.//item')[:15]:
            title = item.find('title').text if item.find('title') is not None else "Update"
            link = item.find('link').text if item.find('link') is not None else ""
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            description = item.find('description').text if item.find('description') is not None else ""
            
            items.append({
                "title": title.strip(),
                "link": link.strip(),
                "published": pub_date.strip(),
                "snippet": description.strip()[:300]
            })
        return items
    except Exception as e:
        print(f"Error fetching feed: {e}")
        return []

def main():
    posts = fetch_news()
    
    try:
        with open('data.json', 'r') as f:
            content = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        content = {"_meta": {"license": "CC-BY-4.0", "source": "Linux Gaming Feed"}, "data": []}

    content["_meta"]["updated_at"] = datetime.datetime.utcnow().isoformat()
    if posts:
        content["data"] = posts

    with open('data.json', 'w') as f:
        json.dump(content, f, indent=2)

    print(f"Successfully updated data.json with {len(posts)} items.")

if __name__ == "__main__":
    main()
