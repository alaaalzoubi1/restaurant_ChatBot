import mysql.connector
import pandas as pd
import random
import json

def load_phrases(file_path: str):
    df = pd.read_excel(file_path)
    phrases = df['Phrases'].tolist()
    return phrases

def select_phrase(phrases):
    selected_phrase = random.choice(phrases)
    return selected_phrase
file_path = "welcome_responses.xlsx"
def get_random_phrase(user_id):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="restaurant"
    )
    cursor = db.cursor()
    query = "SELECT name FROM users WHERE id = %s;"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    name = result[0][0]
    phrases = load_phrases(file_path)
    phrase = select_phrase(phrases)
    message2 = f"Dear {name},"
    return message2+phrase

# print(get_random_phrase())