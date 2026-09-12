import os
import time
import requests
import feedparser
import urllib.parse

# Environment Variables ከ Render ይወስዳል
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8974305013:AAGvuDQDwqPnCBT8pK3Gad2xGnl5auKsMUg")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "-1004471080700")

posted_guids = set()

def get_latest_news():
    # የ Sky Sports እግር ኳስ RSS Feed አድራሻ
    feed_url = "https://www.skysports.com/rss/12040"
    feed = feedparser.parse(feed_url)
    
    if not feed.entries:
        return None
        
    latest_entry = feed.entries[0]
    title = latest_entry.title
    link = latest_entry.link
    guid = latest_entry.get('id', link)
    
    image_url = None
    # ምስል መፈለጊያ
    if 'media_content' in latest_entry and len(latest_entry.media_content) > 0:
        image_url = latest_entry.media_content[0].get('url')
    elif 'links' in latest_entry:
        for l in latest_entry.links:
            if 'image' in l.get('type', ''):
                image_url = l.get('href')
                break
                
    return title, image_url, guid, link

def translate_to_amharic(text):
    try:
        encoded_text = urllib.parse.quote(text)
        # ትክክለኛው ነፃ የ Google Translate API Endpoint
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=am&dt=t&q={encoded_text}"
        response = requests.get(url, timeout=10).json()
        amharic_text = ""
        for sentence in response[0]:
            if sentence[0]:
                amharic_text += sentence[0]
        return amharic_text
    except Exception as e:
        print(f"የትርጉም ስህተት: {e}")
        return text

def start_bot():
    print("ቦቱ በ Render ላይ መስራት ጀምሯል...")
    while True:
        try:
            news = get_latest_news()
            if news:
                title, image_url, guid, link = news
                
                if guid not in posted_guids:
                    amharic_title = translate_to_amharic(title)
                    message = f"🚨 #ትኩስ_መረጃ | \n\n{amharic_title}\n\nየትኛው ክለብ ደጋፊ ኖት? ሀሳብዎን በኮሜንት ያጋሩ 👇"
                    
                    # ትክክለኛው የ Telegram API Base URL
                    if image_url:
                        send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
                        payload = {"chat_id": CHANNEL_ID, "photo": image_url, "caption": message}
                    else:
                        send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                        payload = {"chat_id": CHANNEL_ID, "text": message}
                        
                    res = requests.post(send_url, json=payload)
                    if res.status_code == 200:
                        posted_guids.add(guid)
                        print(f"አዲስ ዜና ተለቋል: {title}")
                    else:
                        print(f"Telegram Send Error: {res.text}")
        except Exception as e:
            print(f"ስህተት: {e}")
            
        time.sleep(900)  # በየ 15 ደቂቃው ይመረምራል

if __name__ == "__main__":
    start_bot()
