import mysql.connector
import tkinter
from tkinter import messagebox

connection = mysql.connector.connect(user = 'root', database = 'banking_app', password = '!098c2cPa$$word')
cursor = connection.cursor()

def createAccount():
    grabData = ("SELECT userID FROM users")
    cursor.execute(grabData)
    newID = 1
    for item in cursor:
        newID += 1

    newPass = input("Enter a password: ")
    newFirstName = input("Enter your first name: ")
    newLastName = input("Enter your last name: ")

    addUser = (f"INSERT INTO users (userID, userPassword, userFirstName, userLastName) VALUES ({newID}, '{newPass}', '{newFirstName}', '{newLastName}')")
    addBal = (f"INSERT INTO accounts VALUES ({newID}, 0, 0)")
    cursor.execute(addUser)
    cursor.execute(addBal)

    print(f"Your User ID is {newID}.")

def delAcc(userID):
    password = input("Enter your password: ")
    grabUserInfo = (f"SELECT userPassword FROM users WHERE userID={userID}")
    cursor.execute(grabUserInfo)

    for item in cursor:
        if item[0] == password:
            deleteUser = (f"DELETE FROM users WHERE userID={userID}")
            deleteAccount = (f"DELETE FROM accounts WHERE userID={userID}")
            cursor.execute(deleteUser)
            cursor.execute(deleteAccount)
            print("Account Deleted")
        else:
            print("Wrong Password")
            delAcc()



cursor.close()
connection.commit()
connection.close()