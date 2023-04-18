print("Hello World")
import mysql.connector



connection = mysql.connector.connect(user = 'root', database = 'example', password = '!098c2cPa$$word')



cursor = connection.cursor()



testQuery = ("SELECT * FROM table_name")



cursor.execute(testQuery)



for item in cursor:
    print(item)



cursor.close()

connection.close()