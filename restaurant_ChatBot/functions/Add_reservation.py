import spacy
import re
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import _convert as ts
number_mapping = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    # Add more mappings as needed
}
def add_reservation(message,user_id):
    nlp = spacy.load("en_core_web_sm")
    mySqlConnector = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='restaurant'
    )

    cursor = mySqlConnector.cursor()
    doc = nlp(message)
    numbers = []
    time = []
    for ent in doc.ents:
        if ent.label_ == "TIME":
            time.append(ent.text)
            continue
        for token in ent:
            if token.pos_ == "NUM":
                numbers.append(ent.text)
    if len(numbers) != 1 or len(time)!=1:
        return "please tell me the number of people and timing you want to book, for example (Reserving a table for six people, at ten AM.)"
    int_num = [number_mapping.get(item, item) for item in numbers]
    print(int_num)

    query = "SELECT id FROM tables WHERE num_of_chairs >= %s LIMIT 1;"
    cursor.execute(query, (numbers[0],))
    result = cursor.fetchall()
    if len(result) != 0:
        table_id = result[0][0]
    else:
        return "I would like to apologize to you, but we currently do not have reservations"
    if not ts.is_valid_time_format(time[0]):
        time_int = ts.convert_to_24_hour_manual(time[0])
        start_time_str = time_int
    else:
        start_time_str = time[0]
    if not ts.is_valid_time_format(str(start_time_str)):
        return "please give me a right time format you can say 10:00:00 or five PM"
    start_time = datetime.strptime(start_time_str, "%H:%M:%S")
    end_time = start_time + timedelta(hours=2)
    end_time_str = end_time.strftime("%H:%M:%S")
    query = """
            INSERT INTO appointments (user_id, table_id, start_time, end_time, date)
            VALUES (
                %s,
                %s,
                %s,
                %s,
                CURDATE()
            );
        """
    cursor.execute(query, (user_id, table_id, start_time_str, end_time_str))
    mySqlConnector.commit()
    last_inserted_id = cursor.lastrowid


    appointment_id = last_inserted_id
    query_check_user = "SELECT 1 FROM chat_bots WHERE user_id = %s"
    cursor.execute(query_check_user, (user_id,))
    user_exists = cursor.fetchone()

    if user_exists:
        query_update = "UPDATE chat_bots SET appointment_id = %s WHERE user_id = %s"
        cursor.execute(query_update, (appointment_id, user_id))
    else:
        query_insert = "INSERT INTO chat_bots (user_id, appointment_id) VALUES (%s, %s)"
        cursor.execute(query_insert, (user_id, appointment_id))


    mySqlConnector.commit()
    cursor.close()
    mySqlConnector.close()
    return f"A table has been reserved for you at {start_time_str}, with a number of people equal to {numbers[0]}"


# print(add_reservation("Need a  reservation for six, at 12:00:00 .", 2))
