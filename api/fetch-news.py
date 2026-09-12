from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import feedparser

BOT_TOKEN = "8974305013:AAGvuDQDwqPnCBT8pK3Gad2xGnl5auKsMUg"
CHANNEL_ID = "-1004471080700"

# የዜና ምንጭ (BBC Football RSS Feed)
RSS_URL = "http://newsrss.bbc.co.uk/rss/sportrss/0/football/rss.xml"

def get_latest_news():
    feed = feedparser.parse(RSS_URL)
    if feed.entries:
        latest = feed.entries[0]
        title = latest.title
        link = latest.link
        summary = latest.get('summary', '')
        
        # የቴሌግራም መልእክት ቅርፅ
        message = f"🚨 **የእግር ኳስ ዜና**\n\n📌 **{title}**\n\n{summary}\n\n🔗 [ሙሉውን ለማንበብ]({link})"
        return message
    return "አዲስ ዜና አልተገኘም።"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            news_text = get_latest_news()
            
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = json.dumps({
                "chat_id": CHANNEL_ID,
                "text": news_text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": False
            }).encode('utf-8')

            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as response:
                status_code = response.getcode()

            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"News Sent Successfully! Status: {status_code}".encode('utf-8'))
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))
        return
