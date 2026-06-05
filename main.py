from fastapi import FastAPI
import requests
import os

app = FastAPI()

API_KEY = os.getenv("ODDS_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })


@app.get("/")
def home():

    send_telegram("🔥 BOT FUNCIONANDO CORRECTAMENTE")

    return {"status": "ok"}
