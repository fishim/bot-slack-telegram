from telebot import TeleBot, types
#import maksim
from maksim import get_message

# # створення бота
bot = TeleBot('5887488636:AAEtc9otfhVPvaOOOrazVPOJeUKyKCFFiPA')




@bot.message_handler(func=lambda message:True)
def exo(message):
    get_message(message.chat.id,message.text,2)
    
def send(chat_id,text):
    bot.send_message(chat_id,text)



bot.polling()




