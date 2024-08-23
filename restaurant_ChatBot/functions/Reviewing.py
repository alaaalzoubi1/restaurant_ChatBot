import fasttext
import mysql.connector
from datetime import datetime
import pandas as pd
import spacy


def lemmatize_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    # Join the lemmas into a single string with spaces between each lemma
    lemmas_string = ' '.join(lemmas)
    print(lemmas_string)
    return lemmas_string
def review(message,user_id):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="restaurant"
    )
    cursor = db.cursor()
    insert_query = "INSERT INTO feed_backs(user_id, comment, date) VALUES (%s, %s, %s)"
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    values_to_insert = (user_id, message, current_time)
    cursor.execute(insert_query, values_to_insert)
    db.commit()
    print(f"{cursor.rowcount} record inserted.")
    query = "SELECT name FROM users WHERE id = %s;"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    name = result[0][0]
    db.close()
    model = fasttext.load_model('Reviews_classification_final1.bin')
    message = lemmatize_text(message)
    predict = model.predict(message)
    if predict[0][0] == "__label__not":
        df = pd.read_csv("neg.csv")
        random_row = df.sample(n=1)
        message1 = random_row.iloc[0, 0]
        message2 = f"Dear {name},"
        message = message2 + message1
        return message
    else:
        df = pd.read_csv("pos.csv")
        random_row = df.sample(n=1)
        message1 = random_row.iloc[0, 0]
        message2 = f"Dear {name},"
        message = message2+message1
        return message


# print(review("wow loved this place", 3))