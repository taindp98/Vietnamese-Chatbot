import requests

from telegram_bot_pagination import InlineKeyboardPaginator


class ConversationManagement:
    def __init__(self, update):
        self.chat_id = update.message.chat.id
        self.msg_id = update.message.message_id
        self.text = update.message.text.encode("utf-8").decode()

        self.converse_api_url = "localhost:8000/conversation"
        self.input_data = {}
        self.input_data["message"] = self.text
        self.input_data["state_tracker_id"] = self.chat_id
        self.list_mess_response = []

        self.total_page = 0

    def process_mess(self):
        response_object = requests.post(url=self.converse_api_url, json=self.input_data)
        response_object_json = response_object.json()

        if response_object_json["message"]:
            self.list_mess_response = [
                item.replace("\n", r"").replace(r'"', r"")
                for item in response_object_json["message"]
            ]

            self.total_page = len(self.list_mess_response)

    def render_mess(self, page):
        return self.list_mess_response[page - 1]

    def single_mess(self, page, bot):
        bot.sendMessage(
            chat_id=self.chat_id,
            text=self.render_mess(page),
            reply_to_message_id=self.msg_id,
        )

    def paginator(self, page, bot, edit_mess_id, first_res):
        paginator = InlineKeyboardPaginator(
            page_count=self.total_page, current_page=page, data_pattern="Trang#{page}"
        )

        if first_res:
            bot.sendMessage(
                chat_id=self.chat_id,
                text=self.render_mess(page),
                reply_to_message_id=self.msg_id,
                reply_markup=paginator.markup,
            )
        else:
            bot.editMessageText(
                chat_id=self.chat_id,
                text=self.render_mess(page),
                message_id=edit_mess_id,
                reply_markup=paginator.markup,
            )
