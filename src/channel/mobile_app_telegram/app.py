from flask import Flask, request
import telegram
import os
from dotenv import load_dotenv


from callback import ConversationManagement


bot_user_name = "BKBot"
URL = "https://telegram-hcmut.herokuapp.com/"


global bot
global TOKEN
TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)


@app.route("/{}".format(TOKEN), methods=["POST"])
def respond():

    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    global manager

    object_message = update.message
    object_callback = update.callback_query
    first_res = False
    if object_message:
        object_text = object_message.text
        if object_text:
            # global manager
            manager = ConversationManagement(update)
            manager.process_mess()

            if manager.list_mess_response:
                page = int(1)
                first_res = True
                if manager.total_page > 1:
                    edit_mess_id = None
                    manager.paginator(page, bot, edit_mess_id, first_res)
                else:
                    manager.single_mess(page, bot)

                return "success"
            else:
                return "fail"
        else:
            return "fail"
    else:
        if object_callback:
            object_page = int(object_callback.data.split("#")[1])

            edit_mess_id = object_callback.message.message_id

            if manager:
                manager.paginator(object_page, bot, edit_mess_id, first_res)
                return "success"
            else:
                return "fail"
        else:
            return "fail"


@app.route("/set_webhook", methods=["GET", "POST"])
def set_webhook():
    s = bot.setWebhook("{URL}{HOOK}".format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route("/")
def index():
    return "."


if __name__ == "__main__":
    app.run(threaded=True)
