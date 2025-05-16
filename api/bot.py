import os
import json
from http.server import BaseHTTPRequestHandler
import requests

BOT_TOKEN = os.getenv('7782183273:AAF0ftxZJwyPrT3J-rr95JIZJ01nqzRVOVI')  # Must match Vercel's env var name
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. Log raw headers (check in Vercel logs)
            print("Headers:", dict(self.headers))
            
            # 2. Read request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print("Raw data:", post_data.decode('utf-8'))
            
            # 3. Parse and respond
            update = json.loads(post_data.decode('utf-8'))
            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')
            
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={'chat_id': chat_id, 'text': f"✅ Received: {text}"}
            )
            
            self.send_response(200)
            self.end_headers()
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            print(error_msg)  # Check in Vercel logs
            self.send_response(500)
            self.end_headers()