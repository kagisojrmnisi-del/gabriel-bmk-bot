from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "gabriel123")

@app.route("/")
def home():
    return "Bot is running!", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        print(f"Verify attempt: mode={mode} token={token} challenge={challenge}")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("VERIFIED!")
            return challenge, 200
        else:
            print(f"FAILED: expected {VERIFY_TOKEN} got {token}")
            return "Verification failed", 403
    else:
        # POST - messages from WhatsApp will come here
        print(f"Message: {request.json}")
        return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
