from fastapi import FastAPI
import requests
import os

app = FastAPI()

API_KEY = os.getenv("ODDS_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SPORTS = [
    "soccer_epl",
    "basketball_nba",
    "tennis_atp_french_open"
]

def calculate_arb(best_odds):
    return (1 - sum(1/x for x in best_odds.values())) * 100


def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })


@app.get("/")
def home():

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": "🔥 BOT FUNCIONANDO CORRECTAMENTE"
    })

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
                "markets": "h2h",
                "oddsFormat": "decimal"
            }
        )

        if response.status_code != 200:
            continue

        matches = response.json()

        for match in matches:

            best = {}

            for bookmaker in match.get("bookmakers", []):

                for market in bookmaker.get("markets", []):

                    for outcome in market.get("outcomes", []):

                        name = outcome["name"]
                        price = float(outcome["price"])

                        if name not in best or price > best[name]:
                            best[name] = price

            if len(best) < 2:
                continue

            profit = calculate_arb(best)

            if profit > 0:

                arb = {
                    "sport": sport,
                    "match": f"{match['home_team']} vs {match['away_team']}",
                    "profit": round(profit, 2),
                    "odds": best
                }

                opportunities.append(arb)

                message = (
                    f"🚨 ARBITRAJE DETECTADO 🚨\n\n"
                    f"🏆 {arb['sport']}\n"
                    f"⚽ {arb['match']}\n"
                    f"💰 Profit: {arb['profit']}%\n\n"
                    f"{arb['odds']}"
                )

                send_telegram(message)

    return {
        "count": len(opportunities),
        "opportunities": opportunities
    }
