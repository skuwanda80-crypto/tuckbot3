from flask import Flask, request
import requests
import os

app = Flask(__name__)

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")


@app.route("/webhook", methods=["GET"])
def verify():
    # this connects whatsapp to tuckBot
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Failed", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received Data:",data)
    # when customer messages me
    if "message" in data["entry"][0]["changes"][0]["value"]:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        from_number = message["from"]
        msg_body = message["text"]["body"]

        print(f"message from {from_number}:{msg_body}")
    # reply automatically
        reply = f"Hi! Thanks for messaging TuckBot🙏🏻\n You said:{msg_body}"
        send_whatsapp_message(from_number, reply)


    return "ok",200


def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v26.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
