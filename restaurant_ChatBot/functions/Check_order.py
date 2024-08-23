from collections import defaultdict

import mysql.connector
import spacy

import Add_order as add
def check_order(message,user_id):
    mySqlConnector = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='restaurant'
    )
    cursor = mySqlConnector.cursor()
    query = "SELECT cart_id FROM chat_bots WHERE user_id = %s;"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()

    if len(result) == 0:
        return 'you dont have any order yet, you can order by saying (new order) or you can request the menu to see our meals or if youu want you can make a reservation from here '
    if len(result) != 0:
        cart_id = result[0][0]
        query = "SELECT status FROM carts WHERE id = %s;"
        cursor.execute(query, (cart_id,))
        status = cursor.fetchall()
        print("dddddddddddddddd" , len(status))
        if len(status) == 0 or status[0][0] == "":
            status = "not ready"
        else:
            status = status[0][0]
        query = """SELECT mi.name, o.quantity
                        FROM orders o
                        JOIN item_sizes s ON o.item_size_id = s.id
                        JOIN menu_items mi ON s.menu_item_id = mi.id
                        WHERE o.cart_id = %s;"""
        cursor.execute(query,(cart_id,))
        items = cursor.fetchall()
        item_quantities = defaultdict(int)

        for i in range(len(items)):
            name, quantity = items[i]
            if i < len(items) - 1 and items[i + 1][0] == name:
                item_quantities[name] += quantity
            else:
                item_quantities[name] += quantity
        item_quantities = dict(item_quantities)
        select_query = "SELECT final_price FROM carts WHERE id = %s"
        params = (cart_id,)
        cursor.execute(select_query, params)
        result = cursor.fetchone()
        final_price = result[0]
        message = f"""your order status is {status}
        and you have ordered {item_quantities}
        and the total price for you order is {final_price}
        if you want to remove or to add anything please tell me :)"""
        cursor.close()
        mySqlConnector.close()
        return message


# print(check_order("ssss", 2))