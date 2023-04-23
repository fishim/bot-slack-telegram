import psycopg2

# Створює нове повідомлення
def Insert_messenge(text, messenger_user_id, data_time, messenger_channel_id, check_group):
    try:
        # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()

        # Виконання запиту для вставки повідомлення до таблиці бази даних
        cur.execute('''INSERT INTO Messages (text, date_time, user_id)
                       SELECT %s, %s, user_id FROM Users
                       WHERE messenger_user_id = %s RETURNING message_id;''', ( text, data_time, messenger_user_id))
        conn.commit()
        if check_group:
            message_id = cur.fetchone()[0]
            cur.execute('''INSERT INTO Group_messages (message_id, channel_id)
                           SELECT %s, channel_id FROM channels
                           WHERE messenger_channel_id = %s;''', ( message_id, messenger_channel_id))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")
   
        
# Перевіряє чи існує канал 
def Check_channel(messenger_channel_id):
    try:   
        # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute('''SELECT * FROM channels WHERE messenger_channel_id = %s''', ( messenger_channel_id,))
        result = cur.fetchall()
        if result:
            check = True
        else:
            check = False
        cur.close()
        conn.close()
        return check #повертає булеву змінну. True якщо є, а False якщо немає такого каналу
    except psycopg2.Error as e:
        print(f"Error: {e}")

# Перевіряє чи існує користувач
def Check_user(messenger_user_id):
    try:    
        # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute('''SELECT * FROM users WHERE messenger_user_id = %s''', (messenger_user_id,))
        result = cur.fetchall()
        if result:
            check = True
        else:
            check = False
        cur.close()
        conn.close()
        return check #повертає булеву змінну. True якщо є, а False якщо немає такого користувача
    except psycopg2.Error as e:
        print(f"Error: {e}")

# створення нового каналу
def Insert_channel(messenger_channel_id, messenger, messenger_user_id, check_group):
    try:    
        # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        if check_group:
            cur.execute('''INSERT INTO channels (messenger_channel_id, messenger) VALUES (%s, %s);''', ( messenger_channel_id, messenger))
        else:
            cur.execute('''INSERT INTO channels (messenger_channel_id, messenger) VALUES (%s, %s) RETURNING channel_id;''', ( messenger_channel_id, messenger))
            conn.commit()
            channel_id = cur.fetchone()[0]
            check = Check_user(messenger_user_id)
            if check:
                cur.execute('''UPDATE Users SET channel_id = %s WHERE messenger_user_id = %s;''', ( channel_id, messenger_user_id))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")

# створення нового користувача (Якщо це особисті, то спочатку потрібно створити новий канал для цього користувача) 
def Insert_user(messenger_user_id, name_messenger_user, messenger_channel_id, check_group):
    try:   
        # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        if check_group:
            cur.execute('''INSERT INTO users (messenger_user_id, name_messenger_user) VALUES (%s, %s);''', (messenger_user_id, name_messenger_user))
        else:
            cur.execute('''INSERT INTO users (messenger_user_id, name_messenger_user, channel_id) 
                           SELECT %s, %s,  channel_id FROM channels
                           WHERE messenger_channel_id = %s;''', (messenger_user_id, name_messenger_user, messenger_channel_id))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")


# видаляє повідомлення за текстом, id користувача та id каналу
def Delete_messenge(text, messenger_user_id, messenger_channel_id):
    try:
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute('''DELETE FROM messages
                       USING users, channels, group_messages
                       WHERE (users.user_id = messages.user_id
                       AND channels.channel_id = users.channel_id
                       AND text = %s
                       AND channels.messenger_channel_id = %s
                       AND users.messenger_user_id = %s)
                       OR (users.user_id = messages.user_id
                       AND channels.channel_id = group_messages.channel_id
                       AND group_messages.message_id = messages.message_id
                       AND text = %s
                       AND channels.messenger_channel_id = %s
                       AND users.messenger_user_id = %s);''', (text , messenger_channel_id, messenger_user_id, text , messenger_channel_id, messenger_user_id))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")

    

# видаляє всі повідомлення з каналу
def Delete_all_messenges(messenger_channel_id):
    try:
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute('''DELETE FROM messages
                       USING users, channels, group_messages
                       WHERE (users.user_id = messages.user_id
                       AND channels.channel_id = users.channel_id
                       AND channels.messenger_channel_id = %s)
                       OR (users.user_id = messages.user_id
                       AND channels.channel_id = group_messages.channel_id
                       AND group_messages.message_id = messages.message_id
                       AND channels.messenger_channel_id = %s);''', (messenger_channel_id, messenger_channel_id))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")

    

# виводить історію каналу
def history(messenger_channel_id):
    try:
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute('''SELECT u.Name_messenger_user , m.text
                       FROM Messages m
                       INNER JOIN Users u ON m.user_id = u.user_id
                       INNER JOIN Channels c ON u.channel_id = c.channel_id
                       WHERE c.messenger_channel_id = %s
                       UNION
                       SELECT u.Name_messenger_user , m.text
                       FROM Messages m
                       INNER JOIN Group_messages gm ON m.message_id = gm.message_id
                       INNER JOIN Channels c ON gm.channel_id = c.channel_id
                       INNER JOIN Users u ON m.user_id = u.user_id
                       WHERE c.messenger_channel_id = %s;''', (messenger_channel_id, messenger_channel_id))
        rows = cur.fetchall()
        text = []
        for row in rows:
            text.append(f"{row[0]}: {row[1]}")

        cur.execute('''SELECT messenger 
                       FROM channels
                       WHERE messenger_channel_id = %s''', (messenger_channel_id,))
        messenger = cur.fetchall()[0]
        cur.close()
        conn.close()
        return text, messenger # повертає оброблений текст історії та назву месенджеру
    except psycopg2.Error as e:
        print(f"Error: {e}")
    





    
