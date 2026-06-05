from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def home():

    requests.get("https://api.telegram.org/bot8744465782:AAGLbC8ETW_6LtW3Z4hCxKZTY8MD3yuwk9Y/sendMessage?chat_id=7940837782&text=🔥FUNCIONA")

    return {"status":"ok"}
