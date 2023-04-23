import funct
import datetime

text = 'Я тут'
messenger_user_id = 'hjgvhgf'
data_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
messenger_channel_id = '4636263'
check_group = True
messenger = 'slack'
name_messenger_user = 'Григорій'

Check1 = funct.Check_channel(messenger_channel_id)
if not Check1:
    funct.Insert_channel(messenger_channel_id, messenger, messenger_user_id, check_group)
Check2 = funct.Check_user(messenger_user_id)
if not Check2:
    funct.Insert_user(messenger_user_id, name_messenger_user, messenger_channel_id, check_group)
print (Check1)
print (Check2)

print(funct.history(messenger_channel_id))

# funct.Delete_all_messenges(messenger_channel_id)