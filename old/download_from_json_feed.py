import feedparser
import json
import requests
import os
from datetime import datetime, timezone

# Define the folders
audio_folder = "audio"
cover_image_folder = "cover_image"

# Create the folders if they don't exist
os.makedirs(audio_folder, exist_ok=True)
os.makedirs(cover_image_folder, exist_ok=True)

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

# Define the cutoff date
cutoff_date = datetime(2023, 5, 12, tzinfo=timezone.utc)

for entry in feed.entries:
    published_date = entry.get("published", "")
    if published_date:
        # Replace GMT with +0000
        published_date = published_date.replace("GMT", "+0000")
        entry_date = datetime.strptime(published_date, "%a, %d %b %Y %H:%M:%S %z")
        if entry_date < cutoff_date:
            item = {
                "title": entry.title,
                "link": entry.link,
                "description": entry.description,
                "published": published_date,
                "guid": entry.get("guid", ""),
                "image": entry.get("image", "").get("href", ""),
            }
            feed_json["items"].append(item)

            # Download the audio file
            audio_url = item["guid"]
            audio_response = requests.get(audio_url)
            audio_filename = os.path.join(audio_folder, os.path.basename(audio_url))
            with open(audio_filename, "wb") as audio_file:
                audio_file.write(audio_response.content)

            # Download the cover image
            image_url = item["image"]
            image_response = requests.get(image_url)
            image_filename = os.path.join(
                cover_image_folder, os.path.basename(image_url)
            )
            with open(image_filename, "wb") as image_file:
                image_file.write(image_response.content)

            print(f"Downloaded {audio_filename} and {image_filename}")

# Step 4: Save the JSON data to a file
with open("feed.json", "w", encoding="utf-8") as json_file:
    json.dump(feed_json, json_file, ensure_ascii=False, indent=4)
