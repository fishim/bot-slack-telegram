import psycopg2
# Підключення до бази даних (Назва, користувач, пароль, хост, порт)
conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")

cur = conn.cursor()

# Створення таблиці Text
cur.execute("""
    CREATE TABLE messenger (
        Id_messenger SERIAL PRIMARY KEY,
        Name_messenger VARCHAR(15)
    );
    
    CREATE TABLE users (
        Id_user SERIAL PRIMARY KEY,
        Id_user_message VARCHAR(15),
        Name_user VARCHAR(50),
        Id_messenger INT REFERENCES messenger(Id_messenger)
    );
    
    CREATE TABLE channels (
        Id_channel SERIAL PRIMARY KEY,
        Id_channel_message VARCHAR(15)
        Id_messenger INT REFERENCES messenger(Id_messenger)
    );
    
    CREATE TABLE message (
        Id_message SERIAL PRIMARY KEY,
        Text TEXT,
        Id_user INT REFERENCES users(Id_user),
        Id_channel INT REFERENCES channels(Id_channel)
    );

    INSERT INTO messenger (name_messenger) VALUES ('Telegram', 'Slack');
""")
conn.commit()

# Від'єднання від бази
cur.close()
conn.close()
