import os
import requests
from flask import Flask, request
app = Flask(__name__)
VERIFY_TOKEN = "BMK_GABRIEL_123"
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "")
@app.route('/')
def home():
    return "GABRIEL BMK BOT IS LIVE! God protects Gabriel!"
@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Verification failed", 403
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data:
        try:
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            if 'messages' in value:
                msg = value['messages'][0]
                from_number = msg['from']
                body = msg['text']['body'] if msg['type'] == 'text' else ""
                reply = f"BMK GABRIEL here 🔥 You said: {body}\n\nI am alive! How can I help you?"
                if "hello" in body.lower() or "hi" in body.lower():
                    reply = "Hello! I am GABRIEL BMK BOT 😎 Powered by BMK Designs. How can I help you?"
                send_message(from_number, reply)
        except Exception as e:
            print(e)
    return "OK", 200
def send_message(to, text):
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        return
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    requests.post(url, headers=headers, json=payload)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
