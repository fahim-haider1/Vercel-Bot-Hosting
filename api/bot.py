import os
from http.server import BaseHTTPRequestHandler
import requests

# Replace with your actual token (this is a fake token from your example)
BOT_TOKEN = os.getenv('BOT_TOKEN', '7782183273:AAF0ftxZJwyPrT3J-rr95JIZJ01nqzRVOVI')
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse the update from Telegram
            update = json.loads(post_data.decode('utf-8'))
            chat_id = update['message']['chat']['id']
            text = update['message']['text']
            
            # Prepare echo response
            response_text = f"You said: {text}"
            
            # Send response back to Telegram
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={
                    'chat_id': chat_id,
                    'text': response_text
                }
            )
            
            self.send_response(200)
            self.end_headers()
            return
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            return