import os
from mutualFunctions import getLine, findLine, editMoney, userQuit


FOLDER = "bankFiles/"
CHEQUE = "chequing_money.txt"
SAVE = "savings_money.txt"
CARD = "card_info.txt"

def main():
    username = login()
    while(True):
        whatToDo = int(input("Do you want to 1.Deposit money, 2.Withdraw Money, or 3.Check your balance? "))
        if(whatToDo == 1):
            deposit(username)
        elif(whatToDo == 2):
            withdraw(username)
        elif(whatToDo == 3):
            checkBalance(username)
        userQuit()        


def login():
    incorrect = 0
    while(True):
        userCardNumber = input("Type in your Card Number: ")
        
        cardLine = findCardLine(userCardNumber, CARD)
        if(cardLine != None):
            cardNumber = getLine(cardLine, CARD)

            pinLine = findCardLine(cardNumber, CARD) + 1
            pin = getLine(pinLine, CARD)
            userPin = input("Type in your pin: ")

            if(pin == userPin):
                usernameLine = findCardLine(userCardNumber, CARD) - 1
                username = getLine(usernameLine, CARD)
                return username
                

        
        print("Your card number or pin is incorrect. Please try again.")
        incorrect += 1
        if(incorrect == 3):
            quit()

def deposit(username):
    moneyLine = findLine(username, CHEQUE) + 1
    if(moneyLine != None):
        moneyAmount = float(getLine(moneyLine, CHEQUE))
        depositAmount = float(input("How much money will you deposit into the account? "))

        totalAmount = moneyAmount + depositAmount
        editMoney(moneyLine, totalAmount, CHEQUE)
        
        print("You now have $%.2f in your chequing account." % (totalAmount))


def withdraw(username):
    moneyLine = findLine(username, CHEQUE) + 1
    if(moneyLine != None):
        moneyAmount = float(getLine(moneyLine, CHEQUE))
        depositAmount = float(input("How much money will you withdraw into the account? "))

        totalAmount = moneyAmount - depositAmount
        if(totalAmount >= 0):
            editMoney(moneyLine, totalAmount, CHEQUE)
            print("You now have $%.2f in your chequing account." % (totalAmount))
            
        
        else:
            print("You don't have enough money to withdraw.")



def checkBalance(username):
    whichAccount = int(input("Which account balance would you like to see? (chequing = 1, savings = 2)"))
    if(whichAccount == 1):
        moneyLine = findLine(username, CHEQUE) + 1
        moneyAmount = float(getLine(moneyLine, CHEQUE))
        print("You have $%.2f in your chequing account." %(moneyAmount))

    elif(whichAccount == 2):
        moneyLine = findLine(username, SAVE) + 1
        moneyAmount = float(getLine(moneyLine, SAVE))
        print("You have $%.2f in your chequing account." %(moneyAmount))


'''
Finds the line after given word
@Input = username, filename
@Output = the line number
'''
def findCardLine(whichCard, fileName):
    count = 0

    try:
        f = open(FOLDER + fileName)
        lines = f.readlines()
        count = 2 #Starting Line Number

        while(count < len(lines)):
            username = lines[count].split(" ")
            if(username[1][0:-1] == whichCard):

                return count
            
            count += 5
        
    except PermissionError:
        print("An error has occured. This program doesn't have permission to open the file.")

    except FileNotFoundError:
        print("An error has occured. "+  fileName + " doesn't exist.")
    
    except Exception as e:
        print("An unexpected error occurred: " , e)
    return None



if __name__=="__main__": 
    main()