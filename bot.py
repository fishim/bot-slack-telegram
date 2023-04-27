import sys

from database import funct
from datetime import datetime


class Message:
    def __init__(self, text, user_id, user_name, chat_id, platform, is_it_group):
        self.user_id = user_id
        self.user_name = user_name
        self.chat_id = chat_id
        self.text = text
        self.platform = platform
        self.is_it_group = is_it_group


# def get_message(cls):
#     if not funct.Check_user(cls.user_id):
#         funct.Insert_user(cls.user_id, cls.platform, cls.chat_id)
#
#     funct.Insert_messenge(
#         cls.text, cls.user_id,
#         datetime.fromtimestamp(cls.date),
#         cls.user_name, cls.is_it_group
#     )
#     send_message(cls)

def get_message(chat_id, text, messenger):
    thirt.echo(chat_id, text, messenger)

def send_message(chat_id, text, messenger):
    BotCode.set_message(chat_id, text)


# def send_message(cls):
#     try:
#         if cls.platform == 'TG':
#             return cls.chat_id, cls.text
#         elif cls.platform == 'SL':
#             return 'slack'
#     except:
#         print('Could not send message.')
#         print("Unexpected error:", sys.exc_info()[0])
#
