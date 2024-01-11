from feedgen.feed import FeedGenerator


def generate_feed(base_url: str, audio_path: str, description: str) -> str:
    fg = FeedGenerator()
    fg.title("My Podcast")
    fg.link(href=base_url, rel="alternate")
    fg.description(description)

    fe = fg.add_entry()
    fe.title("Episode 1")
    fe.link(href=f"{base_url}{audio_path}", rel="alternate")
    fe.description(description)

    rssfeed = fg.rss_str(pretty=True)

    return rssfeed
