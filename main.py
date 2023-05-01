import mysql.connector

connection = mysql.connector.connect(user = 'root', database = 'banking_app', password = '!098c2cPa$$word')
cursor = connection.cursor()

#Log in functionality
def logIn():
    logID = int(input("input userID"))
    logPass = input("enter your password")

    grabLogData = (f"SELECT userID, userPassword, userFirstName, userLastName FROM users WHERE userID={logID}")
    try:
        cursor.execute(grabLogData)
    except:
        print("user not found")

    for item in cursor:
        if item[1] == logPass:
            userID = logID
            userPass = logPass
            userFirstName = item[2]
            userLastName = item[3]
            print(f"Welcome {userFirstName}")
        else:
            print("Wrong Password")
            logIn()
    return userID

def checkBalance(userID):
    grabAccData = (f"SELECT userCheckingBalance, userSavingsBalance FROM accounts WHERE userID={userID}")
    cursor.execute(grabAccData)

    for item in cursor:
        print(f"Your checking balance is: {item[0]}")
        print(f"Your savings balance is: {item[1]} ")

def editBalances(userID):
    accountChoice = input("Which account would you like to access? ")
    if accountChoice == "Checking":
        account = "userCheckingAccount"
    elif accountChoice == "Savings":
        account = "userSavingsAccount"
    
    actionChoice = ""
    while actionChoice != "deposit":
        actionChoice = input("Would you like to deposit or withdrawl?")
        print(actionChoice)
    
    if actionChoice == "withdrawl":
        amount = input("How much would you like to withdrawl? ")
        withdrawl = (f"UPDATE accounts SET {account} = {account} - {amount} WHERE userID = {userID}")

    if actionChoice == "deposit":
        amount = input("How much would you like to deposit? ")
        withdrawl = (f"UPDATE accounts SET {account} = {account} + {amount} WHERE userID = {userID}")


userID = logIn()
checkBalance(userID)
editBalances(userID)
checkBalance(userID)




cursor.close()
connection.close()