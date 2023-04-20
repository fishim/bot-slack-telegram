import psycopg2



def Insert_messenge(text, id_user_message, name_user, id_channel_message, messenger):
   
    
    try:
        # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
        conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
        cur = conn.cursor()
        id_user = Check_user(id_user_message, name_user, messenger)
        id_channel = Check_channel(id_channel_message, messenger)

        # Виконання запиту для вставки повідомлення до таблиці бази даних
        cur.execute('''INSERT INTO message (Text, Id_channel, Id_user) VALUES (%s, %s, %s)''', ( text, id_channel, id_user))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")
      
    

def Check_user(id_user_message, name_user, messenger):
    # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
    conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute('''SELECT id_user FROM users WHERE id_user_message = %s''', (id_user_message,))
    result = cur.fetchall()
    if result:
        cur.close()
        conn.close()
        return result[0]
    else:
        cur.close()
        conn.close()
        return Insert_user(id_user_message,name_user, messenger)

def Insert_user(id_user_message, name_user, messenger):
    # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
    conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute('''INSERT INTO users (Id_user_message, Name_user, Id_messenger) VALUES (%s, %s, %s) RETURNING Id_user;''', (id_user_message, name_user, messenger))
    conn.commit()
    result = cur.fetchall()[0]
    cur.close()
    conn.close()
    return result

def Check_channel(id_channel_message, messenger):
    # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
    conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute('''SELECT id_channel FROM channels WHERE id_channel_message = %s''', ( id_channel_message,))
    result = cur.fetchall()
    if result:
        cur.close()
        conn.close()
        return result[0]
    else:
        cur.close()
        conn.close()
        return Insert_channel(id_channel_message, messenger)

def Insert_channel(id_channel_message, messenger):
    # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
    conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute('''INSERT INTO channels (Id_channel_message, Id_messenger) VALUES (%s, %s) RETURNING Id_channel;''', ( id_channel_message, messenger))
    conn.commit()
    result = cur.fetchall()[0]
    cur.close()
    conn.close()
    return result



def Delete_messenge(text, id_user_message, id_channel_message):
    conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
    cur = conn.cursor()
    
    try:
        cur.execute('''DELETE FROM message
                       USING users, channels
                       WHERE users.Id_user = message.Id_user
                       AND channels.Id_channel = message.Id_channel
                       AND text = %s
                       AND channels.Id_channel_message = %s
                       AND users.Id_user_message = %s;''', (text , id_channel_message, id_user_message))
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error: {e}")

    cur.close()
    conn.close()



def history(id_channel_message):
    conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
    cur = conn.cursor()
    
    try:
        
        cur.execute('''SELECT name_user, text 
                        FROM users
                        JOIN message ON users.Id_user = message.Id_user
                        JOIN channels ON message.Id_channel = channels.Id_channel
                        WHERE channels.Id_channel_message = %s;''', (id_channel_message,))
        rows = cur.fetchall()
        data = []
        for row in rows:
            data.append(f"{row[0]}: {row[1]}")
        
        result = "\n".join(data)

        cur.execute('''SELECT messenger.id_messenger 
                       FROM messenger INNER JOIN channels ON messenger.id_messenger = channels.id_messenger
                       WHERE channels.id_channel_message = %s''', (id_channel_message,))
        id_messenger = cur.fetchall()
        return result, id_messenger


    except psycopg2.Error as e:
        print(f"Error: {e}")

    cur.close()
    conn.close()



def Insert_messenge2(text, id_user_message, name_user, id_channel_message, messenger):

    # Підключення до бази даних (Назва, користувач, пароль, хост, порт)
    conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")
    cur = conn.cursor()

    try:
        # Виконання запиту для вставки повідомлення до таблиці бази даних
        cur.execute('''WITH 
                         new_channel AS (
                           INSERT INTO channels (Id_channel_message, Id_messenger)
                           SELECT %(id_channel_message)s, %(id_messenger)s
                           WHERE NOT EXISTS (
                             SELECT 1 FROM channels WHERE Id_channel_message = %(id_channel_message)s
                           )
                           RETURNING Id_channel
                         ),
                         new_user AS (
                           INSERT INTO users (Id_user_message, Name_user, Id_messenger)
                           SELECT %(id_user_message)s, %(name_user)s, %(id_messenger)s
                           WHERE NOT EXISTS (
                             SELECT 1 FROM users WHERE Id_user_message = %(id_user_message)s
                           )
                           RETURNING Id_user
                         )
                       INSERT INTO message (Text, Id_channel, Id_user)
                       SELECT 
                         %(text)s, 
                         COALESCE(
                           (SELECT Id_channel FROM channels WHERE Id_channel_message = %(id_channel_message)s),
                           (SELECT Id_channel FROM new_channel)
                         ),
                         COALESCE(
                           (SELECT Id_user FROM users WHERE Id_user_message = %(id_user_message)s),
                           (SELECT Id_user FROM new_user)
                         )''', {
                                   'text': text,
                                   'id_channel_message': id_channel_message,
                                   'id_user_message': id_user_message,
                                   'name_user': name_user,
                                   'id_messenger': messenger
                               })
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error: {e}")
      
    cur.close()
    conn.close()


    
