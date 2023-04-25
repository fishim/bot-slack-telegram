import psycopg2
# Підключення до бази даних (Назва, користувач, пароль, хост, порт)
conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")

cur = conn.cursor()

# Створення таблиці Text
cur.execute("""    
    CREATE TABLE Person (
        person_id SERIAL PRIMARY KEY,
        First_name VARCHAR(20) NOT NULL,
        Last_name VARCHAR(20) NOT NULL,
        Email VARCHAR(50),
        Number_phone VARCHAR(15)
    );
    
    CREATE TABLE Users (
        user_id SERIAL PRIMARY KEY,
        person_id INTEGER REFERENCES person(person_id) ON UPDATE CASCADE ON DELETE CASCADE,
        messenger_user_id VARCHAR(15) NOT NULL,
        Name_messenger_user VARCHAR(50) NOT NULL
    );

    CREATE TABLE User_channel (
        user_channel_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
        messenger_channel_id VARCHAR(15) NOT NULL,
        channel_type VARCHAR(30) NOT NULL,
        messenger INTEGER NOT NULL
    );
    
    CREATE TABLE Messages (
        message_id SERIAL PRIMARY KEY,
        text TEXT NOT NULL,
        date_time TIMESTAMP NOT NULL,
        user_channel_id INTEGER NOT NULL REFERENCES User_channel(user_channel_id) ON UPDATE CASCADE ON DELETE CASCADE
    );
""")
conn.commit()

# Від'єднання від бази
cur.close()
conn.close()
