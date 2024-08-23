import mysql.connector
import spacy

import Add_order as add


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
def remove_order(message,user_id):
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

    food_message = add.replace_with_food(message.lower())
    doc = nlp(food_message)
    food_count = 0
    for token in doc:
        if token.text.lower() == "food":
            food_count += 1
    if food_count != total_numbers:
        return 'Please specify the quantity of each meal, for example (i need to remove two Cheese Burger Sandwich)'
    else:
        query = "SELECT cart_id FROM chat_bots WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()


        if len(result) == 0:
            return 'you dont have any order yet, you can order by saying (new order) or you can request the menu to see our meals or if youu want you can make a reservation from here '
        if len(result) != 0:
            cart_id = result[0][0]
            matches = add.collect_elements_from_text(message)
            menu_ids = []
            menu_idss = []
            item_size_ids = []
            item_size_idss = []
            i = 0
            for match in matches:

                query = "SELECT id FROM menu_items WHERE name = %s;"
                cursor.execute(query, (match,))
                menu_ids.append(cursor.fetchall())
                menu_idss.append(menu_ids[i][0][0])
                i += 1
            print(menu_idss)
            i = 0
            for menu_id in menu_idss:

                query = "SELECT id FROM item_sizes WHERE menu_item_id = %s AND size_id = 2;"
                cursor.execute(query, (menu_id,))
                item_size_ids.append(cursor.fetchall())
                item_size_idss.append(item_size_ids[i][0][0])
                i += 1
            i = 0
            for i, item_size_id in enumerate(item_size_idss):
                query = "UPDATE orders SET quantity = quantity - %s WHERE cart_id = %s AND item_size_id = %s;"
                try:
                    cursor.execute(query, (int(numbers[i]), cart_id, int(item_size_id)))
                    mySqlConnector.commit()  # Commit the transaction
                    print(f"Updated quantity for cart_id={cart_id}, item_size_id={item_size_id} by {numbers[i]}.")
                except Exception as e:
                    print(f"Failed to update quantity: {e}")
    cursor.close()
    mySqlConnector.close()
    return "Anything else?"
# remove_order("remove 1 Cheese Burger Sandwich Shawarma Chicken Sandwich one please",2)






