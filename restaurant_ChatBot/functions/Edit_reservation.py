import spacy
import re
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

}

def edit_reservation(message, user_id):
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
        elif ent.label_ == "CARDINAL":
            numbers.append(ent.text)

    if not numbers and not time:
        return "Please provide the number of people or the new timing, for example: 'Reserving a table for six people, at ten AM.'"

    int_num = [number_mapping.get(item, item) for item in numbers] if numbers else None

    query = "SELECT id, table_id, start_time, end_time, date FROM appointments WHERE user_id = %s AND ended = 0;"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()

    if len(result) == 0:
        return "You don’t have any active reservations to edit."

    appointment_id, old_table_id, old_start_time, old_end_time, date = result[0]

    update_fields = []
    update_values = []

    if int_num:
        query = "SELECT id FROM tables WHERE num_of_chairs >= %s LIMIT 1;"
        cursor.execute(query, (int_num[0],))
        result = cursor.fetchall()
        if len(result) != 0:
            new_table_id = result[0][0]
            update_fields.append("table_id = %s")
            update_values.append(new_table_id)
        else:
            return "We currently do not have a table for the number of people specified."

    if time:
        if not ts.is_valid_time_format(time[0]):
            start_time_str = ts.convert_to_24_hour_manual(time[0])
        else:
            start_time_str = time[0]

        if not ts.is_valid_time_format(start_time_str):
            return "Please provide a valid time format, for example: 10:00:00 or 5 PM."

        start_time = datetime.strptime(start_time_str, "%H:%M:%S")
        end_time = start_time + timedelta(hours=2)
        end_time_str = end_time.strftime("%H:%M:%S")

        update_fields.append("start_time = %s")
        update_fields.append("end_time = %s")
        update_values.append(start_time_str)
        update_values.append(end_time_str)

    if not update_fields:
        return "No valid updates could be made based on the provided information."

    update_values.extend([appointment_id, user_id])
    update_query = f"""
            UPDATE appointments 
            SET {', '.join(update_fields)} 
            WHERE id = %s AND user_id = %s;
        """

    try:
        cursor.execute(update_query, tuple(update_values))
        mySqlConnector.commit()

        return f"Your reservation has been successfully updated to {start_time_str if time else old_start_time}, for {int_num[0] if int_num else 'the original number of'} people."
    except Exception as e:
        print(f"Failed to update reservation: {e}")
        return "An error occurred while updating your reservation. Please try again."

    finally:
        cursor.close()
        mySqlConnector.close()

print(edit_reservation("I want to edit my reservation to be for five people",55))