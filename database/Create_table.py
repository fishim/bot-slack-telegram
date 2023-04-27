import psycopg2
# Підключення до бази даних (Назва, користувач, пароль, хост, порт)
conn = psycopg2.connect(database="filonchuk", user="postgres", password="Filon2003", host="localhost", port="5432")

cur = conn.cursor()

# Створення таблиці Text
cur.execute("""    
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    CREATE TABLE Persons (
        person_id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
        First_name VARCHAR(30) NOT NULL,
        Last_name VARCHAR(30) NOT NULL,
        Email VARCHAR(70),
        phone_number VARCHAR(15)
    );
    
    CREATE TABLE Users (
        user_id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
        person_id uuid REFERENCES persons(person_id) ON UPDATE CASCADE ON DELETE CASCADE,
        messenger_user_id VARCHAR(15) NOT NULL,
        messenger_user_name VARCHAR(50) NOT NULL,
        messenger INTEGER NOT NULL
    );

    CREATE TABLE Users_channels (
        user_channel_id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
        user_id uuid NOT NULL REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
        messenger_channel_id VARCHAR(15) NOT NULL,
        channel_type VARCHAR(30) NOT NULL
    );
    
    CREATE TABLE Messages (
        message_id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
        text TEXT NOT NULL,
        date_time TIMESTAMP NOT NULL,
        user_channel_id uuid NOT NULL REFERENCES Users_channels(user_channel_id) ON UPDATE CASCADE ON DELETE CASCADE
    );
""")
conn.commit()

# Від'єднання від бази
cur.close()
conn.close()
