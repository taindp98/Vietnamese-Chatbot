# from chatbot import chatbot
from flask import Flask, render_template, redirect, url_for, request
import json
import random
import requests

app = Flask(__name__)
app.static_folder = "static"
app.template_folder = "templates"


@app.route("/")
def home():
    return render_template("bot.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get("msg")
    userId = request.args.get("_id")
    # api_url = 'http://0.0.0.0:6969/api/convers-manager'
    api_url = "https://api-bkbot.herokuapp.com/api/convers-manager"
    input_data = {}
    input_data["message"] = str(userText)
    input_data["state_tracker_id"] = userId

    r = requests.post(url=api_url, json=input_data)
    chatbot_respose = r.json()
    mess_response = [
        item.replace("\n", r"").replace(r'"', r"")
        for item in chatbot_respose["message"]
    ]

    return {"message_list": mess_response}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
