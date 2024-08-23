import mysql.connector
def order_complete(message,user_id):
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
        query = "DELETE FROM chat_bots WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        mySqlConnector.commit()
        message = """Thank you for using our chat bots!
         We value your feedback and would appreciate it if you could take a moment to review our service.
          Your insights help us improve and serve you better."""
        cursor.close()
        mySqlConnector.close()
        return message


# print(order_complete("nope, thanks", 2))