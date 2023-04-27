import psycopg2
import datetime
# import bot
from flask import Flask, request, jsonify, make_response
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json


app = Flask(__name__)
token_client = WebClient(token='xoxp-5117735896177-5107587401396-5102906538901-59ffd614df0a146dd411dc1e460cf285')
token_bot = WebClient(token="xoxb-5117735896177-5090818001831-UzU3V0iDCGT92Sn6vbftmS8K")




# Создаем обработчик команды /menu
@app.route("/api/v1/help", methods=["POST"])
def menuSlackBot():
    '''command = request.form["command"]
    channel_id = request.form["channel_id"]
    user_id = request.form["user_id"]

    # Отправляем пользователю интерактивное меню
    try:
        # Создаем Slack Block Kit с меню
        menu = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Выберите пункт меню:"
                    },
                    "accessory": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Выберите"
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Пункт 1"
                                },
                                "value": "item_1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Пункт 2"
                                },
                                "value": "item_2"
                            }
                        ],
                        "action_id": "menu_selection"
                    }
                }
            ]
        }

        # Отправляем сообщение пользователю с интерактивным меню
        response = token_bot.chat_postMessage(
            channel=channel_id,
            blocks=menu["blocks"]
        )

        # Возвращаем успешный ответ
        return jsonify(
            response_type="in_channel",
            text="Interative menu has been sent to the user"
        )

    except SlackApiError as e:
        # Возвращаем ошибку
        return jsonify(
            response_type="in_channel",
            text="Error sending interative menu: {}".format(e)
        )
    try:
        channel_id = request.form['channel_id']
        channel_info = token_bot.conversations_info(channel="")
        channel_id = channel_info["channel"]["id"]
    except SlackApiError as e:
        print(f"Error: {e}")

    # Получаем список всех слэш-команд, доступных боту
    try:
        command_info = token_bot.api_call("conversations.commands", channel=channel_id)
        commands = command_info["commands"]
        for command in commands:
            print(f"{command['command']} - {command['description']}")
    except SlackApiError as e:
        print(f"Error: {e}")'''


#Команда після виклику /clear
@app.route('/api/v1/clear', methods=['POST'])
def clear_slack_channel():
    # Задаем токен доступа к API Slack
    bot_id = "D0533APGRS6"
    # ID канала, в котором нужно очистить историю сообщений
    channel_id = request.form['channel_id']
    try:
        result = token_bot.conversations_history(channel=channel_id)
    except SlackApiError as e:
        print("0)Error getting messages: {}".format(e))
    # Вызываем метод chat.delete для удаления каждого сообщения в канале
    for message in result["messages"]:
        if message.get("user") != bot_id:
            try:
                token_client.chat_delete(channel=channel_id, ts = message["ts"])
                print(f"Deleted message: {message['text']}")
            except SlackApiError as e:
                print("1)Error deleting message: {}".format(e))
        elif message.get("user") == bot_id:
            try:
                token_bot.chat_delete(channel=channel_id, ts = message["ts"])
                print(f"Deleted message: {message['text']}")
            except SlackApiError as e:
                print("1)Error deleting message: {}".format(e))



# Команда після виклику /history
@app.route('/api/v1/history', methods=['POST'])
def history_slack_channel():
    try:
        # Зчитати ID каналу з запиту
        channel_id = request.form['channel_id']

        try:
            # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
            conn = psycopg2.connect(database="Test_Python_Code", user="postgres", password="Grifenf2002", host="localhost", port="5432")
            cur = conn.cursor()
            
            # Виконання запиту для вставки повідомлення до таблиці бази даних
            cur.execute("SELECT client, text FROM text ORDER BY id DESC LIMIT 10;")
            rows = cur.fetchall()
            # Create a list of dictionaries from the rows
            data = []
            for row in rows:
                data.append(row[0] + ": " + row[1]) 
            
            # Convert the list of dictionaries to JSON
            json_data = json.dumps(data, ensure_ascii=False, indent=1)
            try:
                response = token_bot.chat_postMessage(channel=channel_id, text=json_data)
            except SlackApiError as e:
                print("Error sending message: {}".format(e))

            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as e:
            print(f"Error inserting driver: {e}")
    except SlackApiError as e:
        print("Error:", e)
    return make_response('', 200)

# def get_message():
#     data = request.get_json()
#     event = data['event']
#     if event['type'] == 'message' and 'text' in event:
#         text = event['text']
#         channel = event['channel']
#         user = event['user']
#         ts = float(event['ts'])
#         dt_obj = datetime.datetime.fromtimestamp(ts)
#         dt_str = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
#         try:
#                         # Call the users_info API method to get the name of the user
#             user_info = token_bot.users_info(user=user)
#             name_user = user_info["user"]["name"]

#             # Call the conversations_info API method to get the type of the channel
#             channel_info = token_bot.conversations_info(channel=channel)
#             is_group = channel_info["channel"]["is_channel"]

#             # Print the extracted fields
#             print("name_user:", name_user)
#             print("channel:", channel)
#             print("text:", text)
#             print("datetime:", dt_str)
#             print("is_group:", is_group)

#         except SlackApiError as e:
#             print("Error getting information from Slack: {}".format(e))
text = ""

# Команда після надходження повідомлення
@app.route('/api/v1/message', methods=['POST'])
def slack_event():
    '''data = request.get_json()
    if request.json['type'] == 'url_verification':
        challenge = request.json['challenge']
        return jsonify({'challenge': challenge})
    elif data['type'] == 'event_callback':
        event = data['event']
        if event['type'] == 'message' and 'text' in event:
            text = event['text']
            channel = event['channel']
            user = event['user']
            try:
                # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
                conn = psycopg2.connect(database="Test_Python_Code", user="postgres", password="Grifenf2002", host="localhost", port="5432")
                cur = conn.cursor()

                # Виконання запиту для вставки повідомлення до таблиці бази даних
                cur.execute("INSERT INTO Text (Text, Channel, Client) VALUES (%s, %s, %s)", (text, channel, user))
                print("Був запис")
                conn.commit()
                cur.close()
                conn.close()
            except psycopg2.Error as e:
                print(f"Error inserting driver: {e}") '''
    data = request.get_json()
    if request.json['type'] == 'url_verification':
        challenge = request.json['challenge']
        return jsonify({'challenge': challenge})
    elif data['type'] == 'event_callback':
        event = data['event']
        if event['type'] == 'message' and 'text' in event:
            _text_ = event['text']
            channel = event['channel']
            # user = event['user']
            ts = float(event['ts'])
            # bot.get_message(channel, text, "1")
            # dt_obj = datetime.datetime.fromtimestamp(ts)
            # dt_str = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
            try:
            #     # Call the users_info API method to get the name of the user
            #     # user_info = token_bot.users_info(user=user)
            #     # name_user = user_info["user"]["name"]

            #     # Call the conversations_info API method to get the type of the channel
            #     channel_info = token_bot.conversations_info(channel=channel)
            #     is_group = channel_info["channel"]["is_channel"]

            #     # Print the extracted fields
            #     # print("name_user:", name_user)
                print("channel:", channel)
            #     print("text:", text)
            #     # print("datetime:", dt_str)
            #     # print("is_group:", is_group)

            except SlackApiError as e:
                print("Error getting information from Slack: {}".format(e))

    return make_response('', 200) 

def send_message(channel, _text_):
    response = token_bot.chat_postMessage(channel=channel, text=_text_)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)

# Вставте текст повідомлення, яке ви хочете відправити
# Вставте ID каналу, в який ви хочете відправити повідомлення
#Method.send_message ("Добрий день!", "C052GHNA0UE")
#Method.last_message ("C052GHNA0UE")







