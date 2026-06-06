from fastapi import FastAPI
import requests
import os

app = FastAPI()

API_KEY = "1b7210550cf787e13d245427301dd385"

BOT_TOKEN = "8744465782:AAGLbC8ETW_6LtW3Z4hCxKZTY8MD3yuwk9Y"

CHAT_ID = "7940837782"

SPORTS = [
    "soccer_epl",
    "soccer_spain_la_liga",
    "soccer_italy_serie_a",
    "soccer_germany_bundesliga",
    "soccer_france_ligue_one",
    "basketball_nba",
    "tennis_atp",
    "tennis_wta"
]

def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def calculate_arb(best_odds):

    return (1 - sum(1/x for x in best_odds.values())) * 100


@app.get("/")
def home():

    send_telegram("🔥 BOT DE ARBITRAJE ACTIVO")

    return {"status": "ok"}


@app.get("/run")
def run():

    opportunities = []

    for sport in SPORTS:

        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"

        response = requests.get(
            url,
            params={
                "apiKey": API_KEY,
                "regions": "eu",
                "markets": "h2h,spreads,totals",
                "oddsFormat": "decimal"
            }
        )

        if response.status_code != 200:
            continue

        matches = response.json()

        for match in matches:

            best = {}
            best_bookmakers = {}

            for bookmaker in match.get("bookmakers", []):

                for market in bookmaker.get("markets", []):

                    for outcome in market.get("outcomes", []):

                        name = outcome["name"]
                        price = float(outcome["price"])

                        if name not in best or price > best[name]:
                            best[name] = price
                            best_bookmakers[name] = bookmaker["title"]

            if len(best) < 2:
                continue

            profit = calculate_arb(best)

            if profit > 0:

                message = (
                    f"🚨 ARBITRAJE DETECTADO 🚨\n\n"
                    f"🏆 {sport}\n"
                    f"⚽ {match['home_team']} vs {match['away_team']}\n"
                    f"💰 Ganancia: {round(profit, 2)}%\n\n"
                    f"Cuotas:\n{best}\n\n"
                    f"Casas:\n{best_bookmakers}"
                )

                send_telegram(message)

                opportunities.append(message)

    return {
        "count": len(opportunities)
}
