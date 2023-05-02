import tkinter
from tkinter import messagebox, StringVar
import mysql.connector

window = tkinter.Tk()
window.title("South Austin Bank")
window.geometry('340x440')

userID = 0

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

def createAccount(newPass, newFirstName, newLastName):
    connection = mysql.connector.connect(user = 'root', database = 'banking_app', password = '!098c2cPa$$word')
    cursor = connection.cursor()
    grabData = ("SELECT userID FROM users")
    cursor.execute(grabData)
    newID = 1
    for item in cursor:
        newID += 1

    addUser = (f"INSERT INTO users (userID, userPassword, userFirstName, userLastName) VALUES ({newID}, '{newPass}', '{newFirstName}', '{newLastName}')")
    addBal = (f"INSERT INTO accounts VALUES ({newID}, 0, 0)")
    cursor.execute(addUser)
    cursor.execute(addBal)

    messagebox.showinfo(title="", message=f"Your ID is {newID}")
    cursor.close()
    connection.commit()
    connection.close()

def delAcc(userID, password):
    connection = mysql.connector.connect(user = 'root', database = 'banking_app', password = '!098c2cPa$$word')
    cursor = connection.cursor()
    grabUserInfo = (f"SELECT userPassword FROM users WHERE userID={userID}")
    cursor.execute(grabUserInfo)

    for item in cursor:
        if item[0] == password:
            deleteUser = (f"DELETE FROM users WHERE userID={userID}")
            deleteAccount = (f"DELETE FROM accounts WHERE userID={userID}")
            cursor.execute(deleteUser)
            cursor.execute(deleteAccount)
            messagebox.showinfo(title="", message="Your Account Has Been Deleted")
            logInPage()
        else:
            messagebox.showinfo(title="", message="Wrong Password")
            return ""

    cursor.close()
    connection.commit()
    connection.close()

def modifyAccount(userID, newfName, newlName):
    connection = mysql.connector.connect(user = 'root', database = 'banking_app', password = '!098c2cPa$$word')
    cursor = connection.cursor()
    print(userID)

    modAcc = (f"UPDATE users SET userFirstName = '{newfName}', userLastName = '{newlName}' WHERE userID = {userID}")
    cursor.execute(modAcc)

    messagebox.showinfo(title="", message=f"Hello, {newfName} {newlName}")
    accountPage()

    cursor.close()
    connection.commit()
    connection.close()

def refreshBal():
    checking_bal.config(text=checkChecking(userID))
    savings_bal.config(text=checkSavings(userID))

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

#login widgets
login_label = tkinter.Label(frame, text="Login")
ID_label = tkinter.Label(frame, text="ID")
ID_entry = tkinter.Entry(frame)
password_entry = tkinter.Entry(frame, show="*")
password_label = tkinter.Label(frame, text="Password")
login_button = tkinter.Button(frame, text="Login", command=lambda : logIn(ID_entry.get(), password_entry.get()))
new_acc_button = tkinter.Button(frame, text="Create Account", command= lambda : createAccPage())

#account widgets
acc_page_label = tkinter.Label(frame, text="Account Page")
checking_label = tkinter.Label(frame, text="Checking Balance: ")
checking_bal = tkinter.Label(frame, text="")
savings_label = tkinter.Label(frame, text="Checking Balance: ")
savings_bal = tkinter.Label(frame, text="")
edit_bal_button = tkinter.Button(frame, text="Edit Balances", command= lambda : editBalPage())
logout_button = tkinter.Button(frame, text="Log Out", command= lambda : logInPage())
del_acc_button = tkinter.Button(frame, text="Delete Account", command= lambda : delAccPage())
refreshBal_button = tkinter.Button(frame, text="Refresh Accounts", command= lambda : refreshBal())
mod_account_button = tkinter.Button(frame, text="Modify Acount Info", command= lambda : modAccPage())

#add edit balance widgets
edit_balances_label = tkinter.Label(frame, text="Edit Balances")
account_label = tkinter.Label(frame, text="Account")
account_entry = tkinter.OptionMenu(frame, variable1, *OPTIONS1)
amount_label = tkinter.Label(frame, text="Amount")
amount_entry = tkinter.Entry(frame)
action_label = tkinter.Label(frame, text="Action")
action_entry = tkinter.OptionMenu(frame, variable2, *OPTIONS2)
perform_button = tkinter.Button(frame, text="Submit", command= lambda : editBalances(userID, variable1.get(), amount_entry.get(), variable2.get()))
cancel_edit_button = tkinter.Button(frame, text="Cancel", command= lambda : accountPage())

#create account widgets
create_account_label = tkinter.Label(frame, text="Create Account")
new_password_label = tkinter.Label(frame, text="Password")
new_password_entry = tkinter.Entry(frame)
fname_label = tkinter.Label(frame, text="First Name")
fname_entry = tkinter.Entry(frame)
lname_label = tkinter.Label(frame, text="Last Name")
lname_entry = tkinter.Entry(frame)
create_account_button = tkinter.Button(frame, text="Create Account", command= lambda : createAccount(new_password_entry.get(), fname_entry.get(), lname_entry.get()))
login_page_button = tkinter.Button(frame, text="Log In", command= lambda : logInPage())

#del account widgets
del_acc_label = tkinter.Label(frame, text="Delete Account")
confirm_pass_label = tkinter.Label(frame, text="Confirm Password")
confirm_pass_entry = tkinter.Entry(frame, show="*")
delete_button = tkinter.Button(frame, text="Confirm Deletion", command= lambda : delAcc(userID, confirm_pass_entry.get()))
cancel_del_button = tkinter.Button(frame, text="Cancel", command= lambda : accountPage())

#mod acc widgets
mod_acc_label = tkinter.Label(frame, text="Modify Information")
new_fname_label = tkinter.Label(frame, text="New First Name")
new_fname_entry = tkinter.Entry(frame)
new_lname_label = tkinter.Label(frame, text="New Last Name")
new_lname_entry = tkinter.Entry(frame)
mod_acc_button = tkinter.Button(frame, text="Change", command= lambda : modifyAccount(userID, new_fname_entry.get(), new_lname_entry.get()))
cancel_mod_button = tkinter.Button(frame, text="Cancel", command= lambda : accountPage())

#clear widgets
def clear_frame():
    for widgets in frame.winfo_children():
        widgets.grid_forget()

def logInPage():
    clear_frame()
    login_label.grid(row=0, column=0, columnspan=2)
    ID_label.grid(row=1, column=0)
    ID_entry.grid(row=1, column=1)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1)
    login_button.grid(row=3, column=0, columnspan=2)
    new_acc_button.grid(row=4, column=0, columnspan=2)

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
    logout_button.grid(row=4, column=0, columnspan=2)
    del_acc_button.grid(row=5, column=0, columnspan=2)
    refreshBal_button.grid(row=6, column=0, columnspan=2)
    mod_account_button.grid(row=7, column=0, columnspan=2)

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
    cancel_edit_button.grid(row=5, column=0, columnspan=2)

def createAccPage():
    clear_frame()
    create_account_label.grid(row=0, column=0, columnspan=2)
    new_password_label.grid(row=1, column=0,)
    new_password_entry.grid(row=1, column=1)
    fname_label.grid(row=2, column=0)
    fname_entry.grid(row=2, column=1)
    lname_label.grid(row=3, column=0)
    lname_entry.grid(row=3, column=1)
    create_account_button.grid(row=4, column=0, columnspan=2)
    login_page_button.grid(row=5, column=0, columnspan=2)

def delAccPage():
    clear_frame()
    del_acc_label.grid(row=0, column=0, columnspan=2)
    confirm_pass_label.grid(row=1, column=0,)
    confirm_pass_entry.grid(row=1, column=1)
    delete_button.grid(row=2, column=0, columnspan=2)
    cancel_del_button.grid(row=3, column=0, columnspan=2)

def modAccPage():
    clear_frame()
    create_account_label.grid(row=0, column=0, columnspan=2)
    new_fname_label.grid(row=1, column=0)
    new_fname_entry.grid(row=1, column=1)
    new_lname_label.grid(row=2, column=0)
    new_lname_entry.grid(row=2, column=1)
    mod_acc_button.grid(row=3, column=0, columnspan=2)
    cancel_mod_button.grid(row=4, column=0, columnspan=2)



frame.pack()

logInPage()

window.mainloop()