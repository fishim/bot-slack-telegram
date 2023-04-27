import funct
import datetime

# задамо параметри
text = 'Вітання'
messenger_user_id = 'іфолвптіл'
data_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
messenger_channel_id = 'лотчалм'
channel_type = 'Public'
messenger = 2
messenger_user_name = 'Юрій'

# перевірка та вставка юзера
Check1 = funct.Check_user(messenger_user_id)
if not Check1:
    funct.Insert_user(messenger_user_id, messenger_user_name, messenger)

# перевірка та вставка юзера з каналом
Check2 = funct.Check_user_channel(messenger_user_id, messenger_channel_id)
if not Check2:
    funct.Insert_user_channel(messenger_user_id, messenger_channel_id, channel_type)

# вивід для відображення результатів
print (Check1)
print (Check2)

# вставка повідомлення
funct.Insert_messenge(text, data_time, messenger_user_id, messenger_channel_id)

# історія
result = funct.history(messenger_channel_id)
# вивід для відображення результатів
received_text = result[0]
received_channel = result[1]
received_messenger = result[2]
print(received_text)
print(received_channel)
print(received_messenger)

# видалення всіх повідомлень
funct.Delete_all_messenges(messenger_channel_id)