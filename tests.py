import main as m
import unittest
import mysql.connector
import string
import random

#Comment out all calls for any of the functions that print widgets (i.e. accountPage(), logInPage()) in main.py for tests to run correctly

connection = mysql.connector.connect(user = 'root', database = 'banking_app', password = '!098c2cPa$$word')
cursor = connection.cursor()

class testFuncs(unittest.TestCase):
    def testLoginFunc(self):
        m.userID = 0
        m.logIn(1, "password")
        self.assertEqual(m.userID, 1)

    def testCheckSavings(self):
        ID = 1
        cursor.execute(f"SELECT userSavingsBalance FROM accounts WHERE userID={ID}")

        trueBal = 0
        for items in cursor:
            trueBal = items[0]

        self.assertEqual(m.checkSavings(ID), trueBal)

    def testCheckChecking(self):
        ID = 1
        cursor.execute(f"SELECT userCheckingBalance FROM accounts WHERE userID={ID}")

        trueBal = 0
        for items in cursor:
            trueBal = items[0]

        self.assertEqual(m.checkChecking(ID), trueBal)

    def testWithdraw(self):
        ID = 1
        amount = 100
        expectedBal = m.checkSavings(ID) - amount

        m.withdraw(ID, "Savings", 100)

        newBal = m.checkSavings(ID)

        self.assertEqual(newBal, expectedBal)

    def testDeposit(self):
        ID = 1
        amount = 100
        expectedBal = m.checkSavings(ID) + amount

        m.deposit(ID, "Savings", 100)

        newBal = m.checkSavings(ID)

        self.assertEqual(newBal, expectedBal)

    def testCreateAcc(self):
        m.createAccount("password5", "test", "func")
        m.logIn(5, "password5")

        self.assertEqual(m.userID, 5)

    def testModAcc(self):
        initName = random.choice(string.ascii_letters)
        m.modifyAccount(2, initName, "name")
        connection.commit()
        cursor.execute("SELECT userFirstName FROM users WHERE userID=2")
        newName = ""
        for items in cursor:
            newName = items[0]
        self.assertEqual(newName, initName)

    def testDelAcc(self):
        m.delAcc(5, "password5")
        self.assertEquals(m.logIn(5, "password5"), "")







if __name__ == '__main__':
    unittest.main()

cursor.close()
connection.close()


