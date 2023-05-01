import mysql.connector

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

#Log in functionality
def logIn():
    logID = int(input("input userID"))
    logPass = input("enter your password")

    grabLogData = (f"SELECT userID, userPassword, userFirstName, userLastName FROM users WHERE userID={logID}")
    grabData = ("SELECT userID FROM users")
    cursor.execute(grabData)
    maxID = 0
    for item in cursor:
        maxID += 1
    if logID > maxID:
        print("user not found")
        return logIn()
    cursor.execute(grabLogData)

    userID = 0
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

def withdraw(userID):
    accountChoice = input("Which account would you like to access? ")
    account = ""
    if accountChoice == "Checking":
        account = "userCheckingBalance"
    elif accountChoice == "Savings":
        account = "userSavingsBalance"
    else:
        print("Please choose a valid account type.")
        withdraw(userID)

    amount = input("How much would you like to withdrawl? ")
    withdrawl = (f"UPDATE accounts SET {account} = {account} - {amount} WHERE userID = {userID}")
    cursor.execute(withdrawl)

def deposit(userID):
    accountChoice = input("Which account would you like to access? ")
    account = ""
    if accountChoice == "Checking":
        account = "userCheckingBalance"
    elif accountChoice == "Savings":
        account = "userSavingsBalance"
    else:
        print("Please choose a valid account type.")
        deposit(userID)

    amount = input("How much would you like to withdrawl? ")
    deposit = (f"UPDATE accounts SET {account} = {account} + {amount} WHERE userID = {userID}")
    cursor.execute(deposit)

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

if input("Do you need to create an account?") == "Yes":
    createAccount()

userID = logIn()
print(f"returned USERID: {userID}")
checkBalance(userID)
if input("Do you want to edit your balance? ") == "Yes":
    transactionComplete = False
    while not transactionComplete:
        actionChoice = input("Would you like to deposit or withdraw?")
        if actionChoice == "deposit":
            deposit(userID)
            transactionComplete = True
        elif actionChoice == "withdraw":
            withdraw(userID)
            transactionComplete = True
    checkBalance(userID)

if input("Do you want to delete your account account? ") == "Yes":
    delAcc(userID)

cursor.close()
connection.commit()
connection.close()