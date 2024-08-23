import mysql.connector
def query(query,id):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'restaurant'
    }
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = (query)
        cursor.execute(query,(id,))
        cnx.commit()
        for row in cursor:
            return row

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cnx:
            cursor.close()
            cnx.close()