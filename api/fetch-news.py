import json
import requests

BOT_TOKEN = "8974305013:AAGvuDQDwqPnCBT8pK3Gad2xGnl5auKsMUg"
CHANNEL_ID = "-1004471080700"

def app(environ, start_response):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": "⚽ አዲስ የእግር ኳስ ዜና!"
        }
        res = requests.post(url, json=payload)
        
        status = '200 OK'
        response_body = f"Success! Telegram status: {res.status_code}".encode('utf-8')
    except Exception as e:
        status = '500 Internal Server Error'
        response_body = f"Error: {str(e)}".encode('utf-8')

    response_headers = [
        ('Content-Type', 'text/plain; charset=utf-8'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    return [response_body]
