import mysql.connector


def cancel_reservation(message,user_id):
    mySqlConnector = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='restaurant'
    )
    cursor = mySqlConnector.cursor()
    query = "SELECT appointment_id FROM chat_bots WHERE user_id = %s;"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    print(len(result),"fffffffffffffff")

    if result[0][0] == None:
        return "you dont have any reservation yet, you can order by saying (new order) or you can request the menu to see our meals or if you want you can make a reservation from here "
    else:
        query = "UPDATE chat_bots SET appointment_id = NULL WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        mySqlConnector.commit()
        query = "DELETE FROM appointments WHERE user_id = %s AND ended = 0;"
        cursor.execute(query, (user_id,))
        mySqlConnector.commit()
        return "your appointment canceled successfully, do you want anything else?"
# cancel_reservation("sdsds",2)