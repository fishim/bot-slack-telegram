import os
import psycopg2
from datetime import datetime
from telebot import TeleBot, types


conn = psycopg2.connect(database="postgres",user="postgres",password="12345",host="localhost",port=5432)

# з'єднання з базою даних
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    message VARCHAR(1000),
    date TIMESTAMP
);
""")
conn.commit()

# створення бота
bot = TeleBot('5887488636:AAEtc9otfhVPvaOOOrazVPOJeUKyKCFFiPA')




#функція для повернення команди 
@bot.message_handler(commands=['start'])
def main(message):                                         
    bot.send_message(message.chat.id, message.text)




@bot.message_handler(commands=['history'])
def get_chat_history(message):
    # отримання історії чату з бази даних
    cursor.execute("SELECT * FROM chat_history")
    rows = cursor.fetchall()

    if len(rows) == 0:
        bot.reply_to(message, "Історія чату порожня.")
    else:
        for row in rows:
            username = row[1]
            message_text = row[2]
            date = row[3].strftime("%Y-%m-%d %H:%M:%S")
            response = f"{date} - {username}: {message_text}"
            bot.send_message(message.chat.id, response)


@bot.message_handler(func=lambda message: True)
def save_chat_history(message):
    username = message.from_user.username
    text = message.text
    date = datetime.fromtimestamp(message.date)

    # зберігання історії чату в базі даних
    cursor.execute("INSERT INTO chat_history (username, message, date) VALUES (%s, %s, %s)", (username, text, date))
    conn.commit()

def echo_all(message):                                     
	bot.send_message(message.chat.id, message.text)


bot.polling(skip_pending= True)
