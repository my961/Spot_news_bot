from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

BOT_TOKEN = "8974305013:AAGvuDQDwqPnCBT8pK3Gad2xGnl5auKsMUg"
CHANNEL_ID = "-1004471080700"
RSS_URL = "https://feeds.bbci.co.uk/sport/football/rss.xml"

def translate_to_amharic(text):
    """ጽሑፉን በነፃ Google Translate API ወደ አማርኛ ይመልሳል"""
    if not text:
        return ""
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=am&dt=t&q=" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            translated_text = "".join([item[0] for item in res[0] if item[0]])
            return translated_text
    except Exception:
        return text

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
        title_en = item.find('title').text if item.find('title') is not None else ''
        description_en = item.find('description').text if item.find('description') is not None else ''
        
        # ምስል ከ RSS Feed ውስጥ መፈለግ
        media = item.find('{http://search.yahoo.com/mrss/}thumbnail')
        image_url = media.attrib['url'] if media is not None and 'url' in media.attrib else None
        
        # ወደ አማርኛ መተርጎም
        title_am = translate_to_amharic(title_en)
        description_am = translate_to_amharic(description_en)
        
        caption = f"🚨 **የእግር ኳስ ዜና**\n\n📌 **{title_am}**\n\n{description_am}"
        
        return caption, image_url
    
    return None, None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            caption, image_url = fetch_rss_news()
            
            if caption:
                if image_url:
                    # ምስል ካለ በ sendPhoto መላክ
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
                    payload = json.dumps({
                        "chat_id": CHANNEL_ID,
                        "photo": image_url,
                        "caption": caption,
                        "parse_mode": "Markdown"
                    }).encode('utf-8')
                else:
                    # ምስል ከሌለ በ sendMessage መላክ
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                    payload = json.dumps({
                        "chat_id": CHANNEL_ID,
                        "text": caption,
                        "parse_mode": "Markdown"
                    }).encode('utf-8')

                req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req) as response:
                    status_code = response.getcode()

                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(f"Success! Status: {status_code}".encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("No news found.".encode('utf-8'))
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))
        return
