import feedparser
import json
import requests

# Step 1: Fetch the RSS feed
url = "https://podcast.frequenzalibera.it/feed.xml"
response = requests.get(url)
rss_feed = response.content

# Step 2: Parse the RSS feed
feed = feedparser.parse(rss_feed)

# Step 3: Convert the parsed data to JSON format
feed_json = {
    "title": feed.feed.title,
    "link": feed.feed.link,
    "language": feed.feed.language,
    "description": feed.feed.description,
    "items": [],
    "image": feed.feed.image,
}

for entry in feed.entries:
    item = {
        "title": entry.title,
        "link": entry.link,
        "description": entry.description,
        "published": entry.get("published", ""),
        "guid": entry.get("guid", ""),
        "image": entry.get("image", "").get("href", ""),
    }
    feed_json["items"].append(item)

# Step 4: Save the JSON data to a file
with open("feed.json", "w", encoding="utf-8") as json_file:
    json.dump(feed_json, json_file, ensure_ascii=False, indent=4)
