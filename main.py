from fastapi import FastAPI
import requests
import os

app = FastAPI()

API_KEY = os.getenv("ODDS_API_KEY")

SPORTS = [
    "soccer_epl",
    "basketball_nba",
    "tennis_atp_french_open"
]

def calculate_arb(best_odds):
    return (1 - sum(1/x for x in best_odds.values())) * 100


@app.get("/")
def home():
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

                opportunities.append({
                    "sport": sport,
                    "match": f"{match['home_team']} vs {match['away_team']}",
                    "profit": round(profit, 2),
                    "odds": best
                })

    return {
        "count": len(opportunities),
        "opportunities": opportunities
                        }
