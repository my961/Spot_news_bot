from http.server import BaseHTTPRequestHandler
import requests

BOT_TOKEN = "8974305013:AAGvuDQDwqPnCBT8pK3Gad2xGnl5auKsMUg"
CHANNEL_ID = "-1004471080700"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": "⚽ አዲስ የእግር ኳስ ዜና!"
        }
        requests.post(url, json=payload)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('OK'.encode('utf-8'))
        return
