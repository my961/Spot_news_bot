import os
import requests
import feedparser
from http.server import BaseHTTPRequestHandler
import urllib.parse

# 1. ዜና ከ RSS Feed መሰብሰብ
def get_latest_news():
    feed_url = "https://skysports.com"
    feed = feedparser.parse(feed_url)
    
    if not feed.entries:
        return None
        
    latest_entry = feed.entries[0] # የመጨረሻዋን ትኩስ ዜና መውሰድ
    title = latest_entry.title
    link = latest_entry.link
    
    image_url = None
    if 'links' in latest_entry:
        for l in latest_entry.links:
            if 'image' in l.get('type', ''):
                image_url = l.get('href')
                break
                
    return title, image_url, link

# 2. የነፃ ጎግል ትርጉም ሲስተም
def translate_to_amharic(text):
    try:
        encoded_text = urllib.parse.quote(text)
        url = f"https://googleapis.com{encoded_text}"
        response = requests.get(url, timeout=10).json()
        amharic_text = ""
        for sentence in response[0]:
            if sentence[0]:
                amharic_text += sentence[0]
        return amharic_text
    except Exception:
        return text

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        BOT_TOKEN = os.environ.get("BOT_TOKEN")
        CHANNEL_ID = os.environ.get("CHANNEL_ID")
        
        if not BOT_TOKEN or not CHANNEL_ID:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Missing environment variables.")
            return

        news = get_latest_news()
        if news:
            title, image_url, link = news
            amharic_title = translate_to_amharic(title)
            
            # ሰው የጻፈው የሚመስል ማራኪ የቴሌግራም መልዕክት ቅርጽ
            message = f"🚨 #ትኩስ_መረጃ | \n\n{amharic_title}\n\nየትኛው ክለብ ደጋፊ ኖት? ሀሳብዎን በኮሜንት ያጋሩ 👇"
            
            if image_url:
                send_url = f"https://telegram.org{BOT_TOKEN}/sendPhoto"
                payload = {"chat_id": CHANNEL_ID, "photo": image_url, "caption": message}
            else:
                send_url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
                payload = {"chat_id": CHANNEL_ID, "text": message}
                
            requests.post(send_url, json=payload)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Success")
