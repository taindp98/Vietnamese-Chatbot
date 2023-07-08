import json

# import telebot
import timeit
import requests
import re
from flask import Flask, request
import telegram
import os
from dotenv import load_dotenv

from telegram_bot_pagination import InlineKeyboardPaginator

# from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from callback import ConversationManagement

# from telebot.credentials import bot_token, bot_user_name,URL


bot_user_name = "BKBot"
URL = "https://telegram-hcmut.herokuapp.com/"


global bot
global TOKEN
TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)


# global page
# global list_mess_response


@app.route("/{}".format(TOKEN), methods=["POST"])
def respond():
    # global chat_id
    # global msg_id

    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # CVS_Mana = ConversationManagement(update)

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

    # var_callback = update.callback_query

    # if update.message:
    # chat_id = update.message.chat.id
    # msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    # if update.message.text:
    # text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    # print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message

    # chatbot_sys_api_url = 'https://chatbot-hcmut.herokuapp.com/api/convers-manager'
    # input_data = {}
    # input_data['message'] = str(text)
    # input_data['state_tracker_id'] = chat_id
    # r = requests.post(url=chatbot_sys_api_url, json=input_data)
    # mess_response = r.json()

    # list_mess_response = [item.replace('\n', r'').replace(r'"',r'') for item in mess_response['message']]

    # if len(list_mess_response) > 1:
    # # mess_response = chatbot_respose['message'].replace('\n', r'').replace(r'"',r'')

    # 	# page = int(call.data.split('#')[1])
    # 	# bot.delete_message(
    # 	# 	call.message.chat.id,
    # 	# 	call.message.message_id
    # 	# )
    # 	# page = 1

    # 	var_callback = update.callback_query
    # 	## default page 1
    # 	# if not page:

    # 	page = 1

    # 	# if var_callback:
    # 		# page = int(var_callback.data.split('#')[1])

    # 	# print('page',page)

    # 	paginator = InlineKeyboardPaginator(
    # 	page_count = len(list_mess_response),
    # 	current_page=page,
    # 	data_pattern='Trang#{page}'
    # 	)

    # 	# bot.sendMessage(chat_id=chat_id, text=mess_response, reply_to_message_id=msg_id)
    # 	bot.sendMessage(
    # 		chat_id=chat_id,
    # 		text=list_mess_response[page-1],
    # 		reply_to_message_id=msg_id,
    # 		reply_markup=paginator.markup)
    # else:

    # bot.sendMessage(chat_id=chat_id, text=list_mess_response[0], reply_to_message_id=msg_id)

    # return 'ok'

    # else:
    # 	return 'fail'

    # elif var_callback:
    # 	page = int(var_callback.data.split('#')[1])

    # 	print('page',page)

    # 	paginator = InlineKeyboardPaginator(
    # 		page_count = len(list_mess_response),
    # 		current_page=page,
    # 		data_pattern='Trang#{page}'
    # 		)

    # 		# bot.sendMessage(chat_id=chat_id, text=mess_response, reply_to_message_id=msg_id)
    # 	# bot.editMessageText(
    # 	bot.sendMessage(
    # 		chat_id=chat_id,
    # 		text=list_mess_response[page-1],
    # 		reply_to_message_id=msg_id,
    # 		# reply_markup=reply_markup
    # 		reply_markup=paginator.markup
    # 		)
    # return 'ok'

    # else:
    # 	return 'fail'


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
# get_bot_response()
#
# if __name__ == '__main__':
#     app.run(threaded=True)
