# from fastapi import FastAPI, Request
# import pandas as pd
# import random
# import json
#
# app = FastAPI()
#
# def load_phrases(file_path: str):
#     df = pd.read_excel(file_path, engine='openpyxl')  # Specify the engine here
#     phrases = df['Phrases'].tolist()
#     return phrases
#
# file_path = 'MainFunctions/menu_response.xlsx'
# phrases = load_phrases(file_path)
#
# @app.get("/request_menu/", response_model=dict)
# async def send_menu(request: Request):
#     selected_phrase = random.choice(phrases)
#     response = {
#         "status": 200,
#         "message": selected_phrase
#     }
#     return response
#
import mysql.connector
import json


def get_menu_names():
    # Connect to the MySQL database
    mySqlConnector = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='restaurant'
    )

    cursor = mySqlConnector.cursor()

    # Query to fetch menu item names
    query = "SELECT name FROM menu_items;"
    cursor.execute(query)

    # Fetch all results
    menu_items = cursor.fetchall()

    # Process the results into a list of names
    menu_names = [item[0] for item in menu_items]

    # Convert the list to JSON format
    menu_json = json.dumps({"menu": menu_names}, indent=4)

    # Print the menu names in JSON format
    return f"{menu_names}"

    # Close the cursor and connection
    cursor.close()
    mySqlConnector.close()


# Call the function to display the menu names
get_menu_names()
