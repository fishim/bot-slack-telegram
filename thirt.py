import bot

def echo(chat_id, text, messenger):
    bot.send_message(chat_id, text, messenger)
