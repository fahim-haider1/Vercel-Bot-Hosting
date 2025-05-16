import os
import json
from http.server import BaseHTTPRequestHandler
import requests

# WARNING: Never commit real tokens to GitHub. This is for testing only.
# Remove this line and use environment variables for production
BOT_TOKEN = "7782183273:AAF0ftxZJwyPrT3J-rr95JIZJ01nqzRVOVI"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is running. POST to /api/bot for Telegram updates.")

    def do_POST(self):
        try:
            # Debug: Show raw request
            print("\n=== New Telegram Update ===")
            
            # Read request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print("Raw JSON:", post_data.decode('utf-8'))
            
            # Parse update
            update = json.loads(post_data.decode('utf-8'))
            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')
            print(f"Processing: {text} from {chat_id}")
            
            # Prepare response
            response_text = f"✅ Received: {text}"
            print(f"Sending: {response_text}")
            
            # Send to Telegram
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={'chat_id': chat_id, 'text': response_text}
            )
            
            self.send_response(200)
            self.end_headers()
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            print(error_msg)
            self.send_response(500)
            self.end_headers()
            # Send error to yourself (optional)
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={'chat_id': YOUR_CHAT_ID, 'text': error_msg}
            )