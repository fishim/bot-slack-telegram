import mainbot

def echo(chat_id, text, messenger):
    mainbot.send_message(chat_id, text, messenger)
