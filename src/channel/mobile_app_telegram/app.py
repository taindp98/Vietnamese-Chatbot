import json
from flask import Flask, request
import telegram
import os
from dotenv import load_dotenv

from telegram_bot_pagination import InlineKeyboardPaginator


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

    global CVS_Mana

    object_message = update.message
    print("---", "object_message", object_message, "----")

    object_callback = update.callback_query
    print("---", "object_callback", object_callback, "----")
    first_res = False
    if object_message:
        object_text = object_message.text
        if object_text:
            # global CVS_Mana
            CVS_Mana = ConversationManagement(update)

            CVS_Mana.process_mess()

            if CVS_Mana.list_mess_response:
                page = int(1)

                first_res = True
                # text = CVS_Mana.render_mess(page)

                if CVS_Mana.total_page > 1:
                    edit_mess_id = None
                    CVS_Mana.paginator(page, bot, edit_mess_id, first_res)

                else:
                    CVS_Mana.single_mess(page, bot)

                return "success"
            else:
                return "fail"
        else:
            return "fail"
    else:
        if object_callback:
            # CVS_Mana = ConversationManagement(object_callback.message)
            object_page = int(object_callback.data.split("#")[1])

            edit_mess_id = object_callback.message.message_id

            print("--- edit_mess_id", edit_mess_id, "---")
            # print('object_page',object_page)
            if CVS_Mana:
                CVS_Mana.paginator(object_page, bot, edit_mess_id, first_res)
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
