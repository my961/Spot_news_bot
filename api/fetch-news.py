from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import xml.etree.ElementTree as ET

BOT_TOKEN = "8974305013:AAGvuDQDwqPnCBT8pK3Gad2xGnl5auKsMUg"
CHANNEL_ID = "-1004471080700"
RSS_URL = "https://feeds.bbci.co.uk/sport/football/rss.xml"

def fetch_rss_news():
    req = urllib.request.Request(
        RSS_URL, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    item = root.find('.//channel/item')
    
    if item is not None:
        title = item.find('title').text if item.find('title') is not None else ''
        link = item.find('link').text if item.find('link') is not None else ''
        description = item.find('description').text if item.find('description') is not None else ''
        
        return f"🚨 **የእግር ኳስ ዜና**\n\n📌 **{title}**\n\n{description}\n\n🔗 [ሙሉውን ለማንበብ]({link})"
    
    return "አዲስ ዜና አልተገኘም።"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            message_text = fetch_rss_news()
            
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = json.dumps({
                "chat_id": CHANNEL_ID,
                "text": message_text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": False
            }).encode('utf-8')

            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as response:
                status_code = response.getcode()

            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Success! Status: {status_code}".encode('utf-8'))
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))
        return
