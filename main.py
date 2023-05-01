import tkinter
from tkinter import messagebox, StringVar
import functions as fn
import mysql.connector

window = tkinter.Tk()
window.title("South Austin Bank")
window.geometry('340x440')

userID = 1

def logIn(loginID, logPass):
    try:
        logID = int(loginID)
    except:
        messagebox.showinfo(title="", message="Invalid ID")
        return ""
    connection = mysql.connector.connect(user = 'root', database = 'banking_app', password = '!098c2cPa$$word')
    cursor = connection.cursor()
    global userID

    grabLogData = (f"SELECT userID, userPassword, userFirstName, userLastName FROM users WHERE userID={logID}")
    grabData = ("SELECT userID FROM users")
    cursor.execute(grabData)
    maxID = 0
    for item in cursor:
        maxID += 1
    if logID > maxID:
        messagebox.showinfo(title="", message="User not found.")
        return ""

    cursor.execute(grabLogData)

    for item in cursor:
        if item[1] == logPass:
            userID = logID
            messagebox.showinfo(title="", message=f"Welcome, {item[2]}")
            accountPage()
        else:
            messagebox.showinfo(title="", message=f"Wrong Password")
            return ""
    cursor.close()
    connection.commit()
    connection.close()

def checkSavings(userID):
    connection = mysql.connector.connect(user = 'root', database = 'banking_app', password = '!098c2cPa$$word')
    cursor = connection.cursor()

    grabAccData = (f"SELECT userSavingsBalance FROM accounts WHERE userID={userID}")
    cursor.execute(grabAccData)

    for item in cursor:
        return item[0]
    
    cursor.close()
    connection.commit()
    connection.close()

def checkChecking(userID):
    connection = mysql.connector.connect(user = 'root', database = 'banking_app', password = '!098c2cPa$$word')
    cursor = connection.cursor()
    print(userID)

    grabAccData = (f"SELECT userCheckingBalance FROM accounts WHERE userID={userID}")
    cursor.execute(grabAccData)

    for item in cursor:
        return item[0]
    
    cursor.close()
    connection.commit()
    connection.close()

def withdraw(userID, accountChoice, amount):
    connection = mysql.connector.connect(user = 'root', database = 'banking_app', password = '!098c2cPa$$word')
    cursor = connection.cursor()
    try:
        value = int(amount)
    except:
        messagebox.showinfo(title="", message="Invalid Amount Type")
        return ""
    
    account = ""
    if accountChoice == "Checking":
        account = "userCheckingBalance"
    elif accountChoice == "Savings":
        account = "userSavingsBalance"
    else:
        messagebox.showinfo(title="", message="Invalid Account")
        return ""

    withdrawl = (f"UPDATE accounts SET {account} = {account} - {value} WHERE userID = {userID}")
    cursor.execute(withdrawl)
    messagebox.showinfo(title="", message=f"{value} withdrawn from {accountChoice}.")
    accountPage()

    cursor.close()
    connection.commit()
    connection.close()

def deposit(userID, accountChoice, amount):
    connection = mysql.connector.connect(user = 'root', database = 'banking_app', password = '!098c2cPa$$word')
    cursor = connection.cursor()
    try:
        value = int(amount)
    except:
        messagebox.showinfo(title="", message="Invalid Amount Type")
        return ""
    
    account = ""
    if accountChoice == "Checking":
        account = "userCheckingBalance"
    elif accountChoice == "Savings":
        account = "userSavingsBalance"

    deposit = (f"UPDATE accounts SET {account} = {account} + {value} WHERE userID = {userID}")
    cursor.execute(deposit)
    messagebox.showinfo(title="", message=f"{value} deposited in {accountChoice}.")
    accountPage()
      
    cursor.close()
    connection.commit()
    connection.close()

def editBalances(userID, account, amount, action):
    if action == "Withdraw":
        withdraw(userID, account, amount)
    elif action == "Deposit":
        deposit(userID, account, amount)


OPTIONS1 = [
    "Checking",
    "Savings"
]
variable1 = StringVar(window)
variable1.set(OPTIONS1[0])

OPTIONS2 = [
    "Deposit",
    "Withdraw"
]
variable2 = StringVar(window)
variable2.set(OPTIONS2[0])

frame = tkinter.Frame()

#create login widgets
login_label = tkinter.Label(frame, text="Login")
ID_label = tkinter.Label(frame, text="ID")
ID_entry = tkinter.Entry(frame)
password_entry = tkinter.Entry(frame, show="*")
password_label = tkinter.Label(frame, text="Password")
login_button = tkinter.Button(frame, text="Login", command=lambda : logIn(ID_entry.get(), password_entry.get()))

#create account widgets
acc_page_label = tkinter.Label(frame, text="Account Page")
checking_label = tkinter.Label(frame, text="Checking Balance: ")
checking_bal = tkinter.Label(frame, text="")
savings_label = tkinter.Label(frame, text="Checking Balance: ")
savings_bal = tkinter.Label(frame, text="")
edit_bal_button = tkinter.Button(frame, text="Edit Balances", command= lambda : editBalPage())

#add edit balance widgets
edit_balances_label = tkinter.Label(frame, text="Edit Balances")
account_label = tkinter.Label(frame, text="Account")
account_entry = tkinter.OptionMenu(frame, variable1, *OPTIONS1)
amount_label = tkinter.Label(frame, text="Amount")
amount_entry = tkinter.Entry(frame)
action_label = tkinter.Label(frame, text="Action")
action_entry = tkinter.OptionMenu(frame, variable2, *OPTIONS2)
perform_button = tkinter.Button(frame, text="Submit", command= lambda : editBalances(userID, variable1.get(), amount_entry.get(), variable2.get()))

#layout widgets
def clear_frame():
    for widgets in frame.winfo_children():
        widgets.grid_forget()

def logInPage():
    login_label.grid(row=0, column=0, columnspan=2)
    ID_label.grid(row=1, column=0)
    ID_entry.grid(row=1, column=1)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1)
    login_button.grid(row=3, column=0, columnspan=2)

def accountPage():
    clear_frame()
    checking_bal.config(text=checkChecking(userID))
    savings_bal.config(text=checkSavings(userID))
    acc_page_label.grid(row=0, column=0, columnspan=2)
    checking_label.grid(row=1, column=0,)
    checking_bal.grid(row=1, column=1)
    savings_label.grid(row=2, column=0)
    savings_bal.grid(row=2, column=1)
    edit_bal_button.grid(row=3, column=0, columnspan=2)

def editBalPage():
    clear_frame()
    edit_balances_label.grid(row=0, column=0, columnspan=2)
    account_label.grid(row=1, column=0,)
    account_entry.grid(row=1, column=1)
    amount_label.grid(row=2, column=0)
    amount_entry.grid(row=2, column=1)
    action_label.grid(row=3, column=0)
    action_entry.grid(row=3, column=1)
    perform_button.grid(row=4, column=0, columnspan=2)


frame.pack()

logInPage()

window.mainloop()