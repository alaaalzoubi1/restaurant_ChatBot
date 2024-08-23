import pandas as pd
import random
import mysql.connector

def new_order(message,user_id):
    mySqlConnector = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='restaurant'
    )
    cursor = mySqlConnector.cursor()
    query = "SELECT cart_id FROM chat_bots WHERE user_id = %s ;"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    if len(result) != 0:
        df = pd.read_csv("neworder_responses.csv")
        random_row = df.sample(n=1)
        message = random_row.iloc[0, 0]
        return message
    query = "INSERT INTO visitors (user_id, table_id) VALUES (%s,1);"
    cursor.execute(query, (user_id,))
    mySqlConnector.commit()
    query = "SELECT id FROM visitors WHERE user_id = %s ;"
    cursor.execute(query, (user_id,))
    visitor_id = cursor.fetchall()
    query = "INSERT INTO carts (visitor_id) VALUES (%s);"
    cursor.execute(query, (visitor_id[len(visitor_id) - 1][0],))
    mySqlConnector.commit()
    query = "SELECT id FROM carts WHERE visitor_id = %s ;"
    cursor.execute(query, (visitor_id[len(visitor_id) - 1][0],))
    cart_id = cursor.fetchall()
    query = "INSERT INTO chat_bots (user_id,cart_id) VALUES (%s,%s);"
    cursor.execute(query, (user_id, cart_id[0][0]))
    mySqlConnector.commit()
    df = pd.read_csv("neworder_responses.csv")
    random_row = df.sample(n=1)
    message = random_row.iloc[0, 0]
    cursor.close()
    mySqlConnector.close()
    return message


# print(new_order("new order", 2))


