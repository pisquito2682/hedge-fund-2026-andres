from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def home():

    requests.get("https://api.telegram.org/botTU_TOKEN/sendMessage?chat_id=TU_CHAT_ID&text=🔥FUNCIONA")

    return {"status":"ok"}
