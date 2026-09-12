from http.server import BaseHTTPRequestHandler
import json
import urllib.request

BOT_TOKEN = "8974305013:AAGvuDQDwqPnCBT8pK3Gad2xGnl5auKsMUg"
CHANNEL_ID = "-1004471080700"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = json.dumps({
                "chat_id": CHANNEL_ID,
                "text": "⚽ አዲስ የእግር ኳስ ዜና!"
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
