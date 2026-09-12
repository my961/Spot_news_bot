import os
import requests
import feedparser
import urllib.parse
from http.server import BaseHTTPRequestHandler

# Telegram Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8974305013:AAGvuDQDwqPnCBT8pK3Gad2xGnl5auKsMUg")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "-1004471080700")

# Multiple RSS Sources for Transfers, News, and Stories
FEEDS = [
    "https://www.skysports.com/rss/12040",   # Sky Sports Football
    "http://feeds.bbci.co.uk/sport/football/rss.xml", # BBC Sport Football
    "https://www.skysports.com/rss/11661"    # Transfer News
]

def get_latest_article():
    for feed_url in FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                entry = feed.entries[0]
                title = entry.title
                link = entry.link
                summary = getattr(entry, 'summary', '')
                
                # Image Extraction
                image_url = None
                if 'media_content' in entry and len(entry.media_content) > 0:
                    image_url = entry.media_content[0].get('url')
                elif 'media_thumbnail' in entry and len(entry.media_thumbnail) > 0:
                    image_url = entry.media_thumbnail[0].get('url')
                elif 'links' in entry:
                    for l in entry.links:
                        if 'image' in l.get('type', ''):
                            image_url = l.get('href')
                            break
                            
                return title, summary, image_url, link
        except Exception as e:
            print(f"Error fetching feed {feed_url}: {e}")
            continue
    return None

def translate_to_amharic(text):
    if not text:
        return ""
    try:
        # Translate up to 500 chars to avoid URL length issues
        clean_text = text[:500]
        encoded_text = urllib.parse.quote(clean_text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=am&dt=t&q={encoded_text}"
        res = requests.get(url, timeout=10).json()
        amharic_text = ""
        for sentence in res[0]:
            if sentence[0]:
                amharic_text += sentence[0]
        return amharic_text
    except Exception as e:
        print(f"Translation Error: {e}")
        return text

def format_caption(title, amharic_title):
    # Professional sportsperson formatting
    caption = f"⚽ **ስፖርት መረጃ | TRANSFERENCE & NEWS**\n\n"
    caption += f"📌 **{amharic_title}**\n\n"
    caption += f"───────────────\n"
    caption += f"🗣 ሀሳብዎን በኮሜንት ያጋሩ! | Share your thoughts below 👇\n"
    caption += f"🔗 @all_football_news_one"
    return caption

def post_to_telegram():
    data = get_latest_article()
    if not data:
        return "No news found"
        
    title, summary, image_url, link = data
    amharic_title = translate_to_amharic(title)
    caption = format_caption(title, amharic_title)

    if image_url:
        send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        payload = {
            "chat_id": CHANNEL_ID,
            "photo": image_url,
            "caption": caption,
            "parse_mode": "Markdown"
        }
    else:
        send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": caption,
            "parse_mode": "Markdown"
        }

    res = requests.post(send_url, json=payload)
    return res.json()

# Vercel Serverless Entrypoint
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            result = post_to_telegram()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(f'{{"status": "success", "telegram_response": {result}}}'.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))
        return
