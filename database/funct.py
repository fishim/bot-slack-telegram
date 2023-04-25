import psycopg2

# Створює нове повідомлення
def Insert_messenge(text, data_time, messenger_user_id, messenger_channel_id):
    try:
        # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        # Виконання запиту для вставки повідомлення до таблиці бази даних
        cur.execute('''INSERT INTO Messages (text, date_time, user_channel_id)
                       SELECT %s, %s, user_channel_id FROM user_channel INNER JOIN users ON users.user_id = user_channel.user_id
                       WHERE messenger_user_id = %s AND messenger_channel_id = %s;''', ( text, data_time, messenger_user_id, messenger_channel_id))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")
   

# Перевіряє чи існує користувач
def Check_user(messenger_user_id):
    try:    
        # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute('''SELECT user_id FROM users WHERE messenger_user_id = %s;''', (messenger_user_id,))
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

# Перевіряє чи існує канал (Спочатку повинен існувати абу бути створений даний user)
def Check_user_channel(messenger_user_id, messenger_channel_id):
    try:   
        # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute('''SELECT user_channel_id FROM user_channel INNER JOIN users ON users.user_id = user_channel.user_id
                       WHERE messenger_user_id = %s AND messenger_channel_id = %s;''', ( messenger_user_id, messenger_channel_id))
        result = cur.fetchall()
        if result:
            check = True
        else:
            check = False
        cur.close()
        conn.close()
        return check #повертає булеву змінну. True якщо є, а False якщо немає такого користувача каналу
    except psycopg2.Error as e:
        print(f"Error: {e}")


# створення нового користувача 
def Insert_user(messenger_user_id, name_messenger_user):
    try:   
        # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute('''INSERT INTO users (messenger_user_id, name_messenger_user) VALUES (%s, %s);''', (messenger_user_id, name_messenger_user))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")

# створення нового каналу (Спочатку повинен існувати абу бути створений даний user)
def Insert_user_channel(messenger_user_id, messenger_channel_id, channel_type, messenger):
    try:    
        # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute('''INSERT INTO user_channel (messenger_channel_id, channel_type, messenger, user_id) 
                       SELECT %s, %s, %s, user_id FROM users
                       WHERE messenger_user_id = %s;''', ( messenger_channel_id, channel_type, messenger, messenger_user_id))
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
                       USING users, user_channel
                       WHERE users.user_id = user_channel.user_id
                       AND user_channel.user_channel_id = messages.user_channel_id
                       AND text = %s
                       AND messenger_channel_id = %s
                       AND messenger_user_id = %s;''', (text , messenger_channel_id, messenger_user_id))
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
                       USING users, user_channel
                       WHERE users.user_id = user_channel.user_id
                       AND user_channel.user_channel_id = messages.user_channel_id
                       AND messenger_channel_id = %s;''', (messenger_channel_id,))
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
        cur.execute('''SELECT Name_messenger_user , text, messenger
                       FROM messages INNER JOIN user_channel ON messages.user_channel_id = user_channel.user_channel_id
                       INNER JOIN users ON users.user_id = user_channel.user_id
                       WHERE messenger_channel_id = %s;''', (messenger_channel_id,))
        rows = cur.fetchall()
        if rows:
            text = ""
            for row in rows:
                text += f"{row[0]}: {row[1]}\n"
            messenger = rows[0][2]
        else:
            cur.execute('''SELECT messenger FROM user_channel WHERE messenger_channel_id = %s;''', (messenger_channel_id,))
            messenger = cur.fetchall()[0][0]
            text = "Channel history does not exist yet"
        cur.close()
        conn.close()
        return text, messenger # повертає текст історії та месенджер (для правильного відображення перетворити текст з масиву на змінну str)
    except psycopg2.Error as e:
        print(f"Error: {e}")
    





    
