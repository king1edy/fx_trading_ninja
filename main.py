from fastapi import FastAPI, Request, HTTPException
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from .env file

app = FastAPI()

# Replace with your broker's API endpoint and headers
BROKER_API = os.environ.get("BROKER_API")
BROKER_API_KEY = os.environ.get("BROKER_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HEADERS = {"Authorization": f"Bearer {BROKER_API_KEY}"}

# Replace with your Telegram bot API token and chat ID
TELEGRAM_API_URL = f"https://api.telegram.org/botT_BOT_TOKEN/sendMessage".replace("T_BOT_TOKEN", TELEGRAM_BOT_TOKEN)
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

@app.get("/")
async def root():
    return {"message": f"Hello Traders..\n Welcome to FXNinja"}


# Webhook route
@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        # Parse incoming JSON payload
        payload = await request.json()
        symbol = payload['symbol']
        action = payload['action']

        print("Received Webhook:", json.dumps(payload, indent=4))

        # Implement logic based on the received webhook data
        # For example, log the signal, trigger a trading bot, or send a response
        # Here, we just print and return the payload for simplicity
        if "action" in payload:
            if payload["action"] == "buy":
                print("Buy Signal Received")
                # Trigger Buy logic
                order = {"symbol": symbol, "side": "buy", "quantity": 1}
                response = requests.post(BROKER_API, json=order, headers=HEADERS)

                # Log to telegram
                send_telegram_message(f"Bought {symbol}")
            elif payload["action"] == "sell":
                # Trigger Sell logic

                # Log to telegram
                order = {"symbol": symbol, "side": "sell", "quantity": 1}
                response = requests.post(BROKER_API, json=order, headers=HEADERS)
                send_telegram_message(f"Sold {symbol}")

                print("Sell Signal Received")
            else:
                print("Unknown action:", payload["action"])
        else:
            raise HTTPException(status_code=400, detail="Invalid payload")

        return {"status": "success", "data": payload}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

def send_telegram_message(message):
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(TELEGRAM_API_URL, json=payload)
