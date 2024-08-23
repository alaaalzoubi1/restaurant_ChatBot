import spacy
import re
import pandas as pd
import mysql.connector

elements = [
        "Cheese Burger Sandwich",
        "Shawarma Chicken Sandwich",
        "Shawarma Meat Sandwich",
        "Falafel Sandwich",
        "Crespi Chicken Sandwich",
        "Zinger Chicken Sandwich",
        "Pepperoni Pizza",
        "Mixed Pizza",
        "Hot Dog Pizza",
        "Four Seasons Pizza",
        "Hummus Plate",
        "French Fries Plate",
        "Vegetables Soup",
        "Strawberry Donut",
        "Vanilla Donut",
        "Chocolate Donut",
        "Chocolate Waffle",
        "Pan Cake",
        "Pepsi Can",
        "Pepsi Cup",
        "Pepsi Bottle",
        "Fresh Strawberry Juice"
]
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
def replace_with_food(text):
    elements_lower = [element.lower() for element in elements]
    if text is None or pd.isna(text):
        return text # Return the original text if it's None or NaN
    pattern = "|".join(map(re.escape, elements_lower))
    modified_text = re.sub(pattern, 'food', text)
    return modified_text
from fuzzywuzzy import fuzz

def collect_elements_from_text(text):
    # Convert elements to lowercase for case-insensitive matching
    elements_lower = [element.lower() for element in elements]

    # If the input text is None or empty, return an empty list
    if text is None or pd.isna(text):
        return []

    # Convert the input text to lowercase
    text = text.lower()

    # Find the closest matches using fuzzy matching
    matches = []
    for element in elements_lower:
        similarity = fuzz.partial_ratio(text, element)
        if similarity >= 80:  # Adjust the threshold as needed
            matches.append(element)

    # Return unique matches
    unique_matches = list(set(matches))
    return unique_matches
def add_order(message,user_id):
    nlp = spacy.load("en_core_web_sm")
    mySqlConnector = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='restaurant'
    )

    cursor = mySqlConnector.cursor()
    doc = nlp(message)
    total_numbers = 0
    numbers = []
    for token in doc:
        if token.pos_ == "NUM":
            total_numbers += 1
            x = number_mapping.get(token.text.lower(), None)
            if x is not None:
                numbers.append(int(x))
            else:
                numbers.append(int(token.text))
    food = collect_elements_from_text(message)
    food_count = len(food)
    if food_count != total_numbers or food_count==0 or total_numbers==0:
        return 'Please specify the quantity of each meal, for example (i need two Cheese Burger Sandwich and one of Pepperoni Pizza'
    else:
        query = "SELECT cart_id FROM chat_bots WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        cart_id = 0
        print(len(result))
        if len(result) == 0 or result[0][0] == None:
            visitor_id = []
            query ="INSERT INTO visitors (user_id, table_id) VALUES (%s,1);"
            cursor.execute(query, (user_id,))
            mySqlConnector.commit()
            query = "SELECT id FROM visitors WHERE user_id = %s ;"
            cursor.execute(query, (user_id,))
            visitor_id = cursor.fetchall()
            query = "INSERT INTO carts (visitor_id) VALUES (%s);"
            cursor.execute(query, (visitor_id[len(visitor_id)-1][0],))
            mySqlConnector.commit()
            cart_id = cursor.lastrowid
            print("ccccccccccccccccccc", cart_id)
            query = "INSERT INTO chat_bots (user_id,cart_id) VALUES (%s,%s);"
            cursor.execute(query, (user_id,cart_id))
            mySqlConnector.commit()


        if result != None:
            matches = collect_elements_from_text(message)
            print(matches,"    dfdfdffddfdfdf     ",numbers)
            menu_id =[]
            item_size_id = []
            prices = []
            pricess = []
            total_price = 0
            for match in matches:
                query = "SELECT id FROM menu_items WHERE name = %s;"
                cursor.execute(query, (match,))
                menu_id.append(cursor.fetchall())
            for menu in menu_id:
                query = "SELECT id FROM item_sizes WHERE menu_item_id = %s AND (size_id = 2 OR size_id = 4);"
                cursor.execute(query, (menu[0][0],))
                item_size_id.append(cursor.fetchall())
            for menu in menu_id:
                query = "SELECT price FROM item_sizes WHERE menu_item_id = %s AND (size_id = 2 OR size_id = 4);"
                cursor.execute(query, (menu[0][0],))
                prices.append(cursor.fetchall().pop())
            for i,price in enumerate(prices):
                pricess.append(prices[i][0])
            print(numbers)
            print(pricess)

            for i, match in enumerate(matches):
                if cart_id == 0:
                    cart_id = result[0][0]
                item_size_idd = item_size_id[i][0][0]
                quantity = numbers[i]
                price = pricess[i]
                total_price += quantity*price
                insert_query = """
                    INSERT INTO orders (cart_id, item_size_id, quantity,payment)
                    VALUES (%s, %s, %s,%s);
                    """
                print(cart_id,"      ",item_size_idd,"           ", quantity)
                cursor.execute(insert_query, (cart_id, item_size_idd, quantity,price*quantity))
                mySqlConnector.commit()
            update_query = "UPDATE carts SET final_price = %s WHERE id = %s"
            params = (total_price, cart_id)
            cursor.execute(update_query, params)
            mySqlConnector.commit()
            return "anything else?"
    cursor.close()
    mySqlConnector.close()


add_order("give me two Cheese Burger Sandwich please",8)


