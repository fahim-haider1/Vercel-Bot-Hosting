import os
import json
from http.server import BaseHTTPRequestHandler

BOT_TOKEN = os.getenv('7782183273:AAF0ftxZJwyPrT3J-rr95JIZJ01nqzRVOVI')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Telegram Bot is running! This endpoint expects POST requests from Telegram.")
        
    def do_POST(self):
        # Your existing POST handling code here
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
            chat_id = update['message']['chat']['id']
            text = update['message']['text']
            
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={'chat_id': chat_id, 'text': f"Echo: {text}"}
            )
            
            self.send_response(200)
            self.end_headers()
            
        except Exception as e:
            print("Error:", e)
            self.send_response(500)
            self.end_headers()