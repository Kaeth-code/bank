import os
import random
from mutualFunctions import getLine, findLine, editMoney, userQuit, editInfo

#comments
FOLDER = "bankFiles/"
DETAILS = "account_details.txt"
CHEQUE = "chequing_money.txt"
SAVE = "savings_money.txt"
CARD = "card_info.txt"


def main():
    usertype = login()
    if(usertype == "admin"):
        admin()
    else:
        user(usertype)


'''
Asks the user to type in a username and password
@Input = None
@Output = String('admin' or username)
'''
def login():
    incorrect = 0
    while(True):
        username = input("Type in your username: ")
        
        
        if(username == "KaetharansBank123"):
            password = input("Type in your password: ")
            if(password == "Kaetharan@19"):
                return  "admin"
        
        lineNum = findLine(username, DETAILS) + 1
        if(lineNum != None):
        
            passwordLine = findNextLine(username, DETAILS)
            if(passwordLine == "_"):
                password = input("Type in a password to use in your new account: ")
                editPassword(lineNum, password)

                cardLine = findCardLine(username, CARD) 
                cardNumber = getLine(cardLine, CARD)
                print("Your card number is:" , cardNumber)
                
                pinNumber = input("Type in a pin for your card: ")
                editPin(cardLine + 1, pinNumber)
                return username
                

            else:
                password = input("Type in your password: ")
                


                if(password == passwordLine):
                    return username
                

        else:
            print("Your username or password is incorrect. Please try again.")
            incorrect += 1
            if(incorrect == 3):
                quit()


'''
Displays the ui for the admin user
@Input = None
@Output = None
'''
def admin():
    while(True):
        whatToDo = int(input("Do you want to deposit money into an account (1), or make a user (2)? "))

        if(whatToDo == 1):
            username = input("Which account do you want to deposit money into? ")
            moneyLine = findLine(username, CHEQUE) + 1
            if(moneyLine != None):
                moneyAmount = float(getLine(moneyLine, CHEQUE))
                depositAmount = float(input("How much money will you deposit into the account? "))

                totalAmount = moneyAmount + depositAmount
                editMoney(moneyLine, totalAmount)
                
                print(username, " now has : $%.2f" % (totalAmount))

            else:
              print("This user does not exist.")


        elif(whatToDo == 2):
            username = input("What is the username of the account? ")
            initialDeposit = input("How much how the user deposited? ")
            cardNumber = makeCardNumber()
            setCardDetails(username, cardNumber, CARD)
            createUser(username, DETAILS)
            doInitialDeposit(username, initialDeposit, CHEQUE)
            doInitialDeposit(username, 0, SAVE)
            
            print("User created")


        userQuit()

'''
Displays the ui for the customer user
@Input = username
@Output = None
'''
def user(username):
    while(True):
        whatToDo = int(input("Do you want to check your balance (1), transfer with money (2), or pay someone (3)? "))

        if(whatToDo == 1):
            whichAccount = int(input("Do you want to see the balance of your chequing account (1) or your savings account(2)? "))
            if(whichAccount == 1):
                account = CHEQUE
                accountName = "chequing"

            elif(whichAccount == 2):
                account = SAVE
                accountName = "savings"

            moneyAmount =float(findNextLine(username, account)) 
            print("Your %s balance is : $%.2f" % (accountName, moneyAmount))
        


        elif(whatToDo == 2):
            whichAccount = int(input("Do you want to transfer to your chequing account (1) or to your savings account(2)? "))
            transferAmount = float(input("How much money do you want to transfer? "))
            if(whichAccount == 1):
                accountTo = CHEQUE
                accountFrom = SAVE
                

            elif(whichAccount == 2):
                accountTo = SAVE
                accountFrom = CHEQUE
                
            transfer(accountTo, accountFrom, transferAmount, username)
            
                
        
        elif(whatToDo == 3):
            userTo= input("Which person do you want to pay? ")
            whichAccount = int(input("Do you want to pay from your chequing account (1) or your savings account(2)? "))
            
            if(whichAccount == 1):
                account = CHEQUE
                accountName = "chequing"

            elif(whichAccount == 2):
                account = SAVE
                accountName = "savings"

            moneyLineTo = findLine(userTo, CHEQUE) + 1
            moneyLineFrom = findLine(username, account) + 1

            if(userTo != username):

                if(moneyLineTo != None and moneyLineFrom != None):
                    moneyAmountTo = float(getLine(moneyLineTo, CHEQUE))
                    moneyAmountFrom = float(getLine(moneyLineFrom, account))

                    depositAmount = float(input("How much money will you pay them? "))

                    totalAmountTo = moneyAmountTo + depositAmount
                    totalAmountFrom = moneyAmountFrom - depositAmount
                    if(totalAmountFrom < 0):
                        print("You don't have enough money to pay.")
                        continue
                    
                    
                    editMoney(moneyLineTo, totalAmountTo, CHEQUE)
                    editMoney(moneyLineFrom, totalAmountFrom, account)

                    print("You have successfully payed $%.2f to %s. You now have: $%.2f in your %s account." % (depositAmount, userTo, totalAmountFrom, accountName))

                else:
                    print("This user does not exist.")
            else:
                print("You cannot pay yourself.")
            

        userQuit()


'''
transfers from one account to another
@Input = str: accountTo, str: accountFrom, float: transferAmount, str: username
@Output = Nothing
'''
def transfer(accountTo, accountFrom, transferAmount, username):
    moneyLineTo = findLine(username,accountTo) + 1
    moneyLineFrom = findLine(username, accountFrom) + 1

    moneyAmountTo = float(getLine(moneyLineTo, accountTo))
    moneyAmountFrom= float(getLine(moneyLineFrom, accountFrom))

    totalAmountTo = moneyAmountTo + transferAmount
    totalAmountFrom = moneyAmountFrom - transferAmount

    if(totalAmountFrom < 0):
        print("You don't have enough money to transfer")
        return
    
    editMoney(moneyLineTo, totalAmountTo, accountTo)
    editMoney(moneyLineFrom, totalAmountFrom, accountFrom)


    accountNameTo = accountTo.split("_money.txt")[0]
    accountNameFrom = accountFrom.split("_money.txt")[0]

    print("""You have successfully transfered $%.2f to %s. 
    You now have: $%.2f in your %s account and $%.2f in your %s account """ % (transferAmount, accountNameTo, totalAmountTo, accountNameTo, totalAmountFrom, accountNameFrom))


'''
finds line after given line
@Input = line, fileName
@Output = string(nextLine)
'''
def findNextLine(line, fileName):
    lineNum = findLine(line, fileName) 
    if(lineNum == None):
        print("An error occured in function findLine")
        exit
    lineNum += 1           
    nextLine = getLine(lineNum, fileName)
    return nextLine


'''
generates numbers for the password if the user wants it
@Input = length of password
@Output = arr with numbers to use
'''
def makeCardNumber():
    count = 0
    card = ""
    while(count < 16):
        card += str(random.randrange(0,9))
        count += 1
    
    return card



'''
Finds the line after given word
@Input = username, filename
@Output = the line number
'''
def findCardLine(whichUsername, fileName):
    count = 0

    try:
        f = open(FOLDER + fileName)
        lines = f.readlines()
        count = 1

        while(count < len(lines)):
            username = lines[count].split(" ")
            if(username[1][0:-1] == whichUsername):

                return count + 1
            
            count += 5
        
    except PermissionError:
        print("An error has occured. This program doesn't have permission to open the file.")

    except FileNotFoundError:
        print("An error has occured. "+  fileName + " doesn't exist.")
    
    except Exception as e:
        print("An unexpected error occurred: " , e)
    return None




'''
writes username to a file
@Input = string(username), string(fileName)
@Output = nothing
'''
def createUser(username, fileName):
    try:
        f = open(FOLDER + fileName, "a")
        f.write("---------------------------------------------------------" + "\n" +
                "Username: " + username + "\n" +
                "Password: " + "_" + "\n" +
                "---------------------------------------------------------" + "\n")
        f.close()
    except PermissionError:
        print("An error has occured. This program doesn't have permission to open the file.")

    except FileNotFoundError:
        print("An error has occured. "+  fileName + " doesn't exist.")
    
    except Exception as e:
        print("An unexpected error occurred: " , e)

'''
writes username to a file
@Input = string(username), str(deposit), string(fileName) 
@Output = nothing
'''
def doInitialDeposit(username, deposit, fileName):
    try:
        f = open(FOLDER + fileName, "a")
        f.write("---------------------------------------------------------" + "\n" +
                "Username: " + username + "\n" +
                "Money: " + str(deposit) + "\n" +
                "---------------------------------------------------------" + "\n")
        f.close()
    except PermissionError:
        print("An error has occured. This program doesn't have permission to open the file.")

    except FileNotFoundError:
        print("An error has occured. "+  fileName + " doesn't exist.")
    
    except Exception as e:
        print("An unexpected error occurred: " , e)

'''
writes username and card number to a file
@Input = string(username), string(fileName)
@Output = nothing
'''
def setCardDetails(username, cardNumber, fileName):
    try:
        f = open(FOLDER + fileName, "a")
        f.write("---------------------------------------------------------" + "\n" +
                "Username: " + username + "\n" +
                "Card Number: " + cardNumber + "\n" +
                "Pin: " + "_" + "\n" +
                "---------------------------------------------------------" + "\n")
        f.close()
        
    except PermissionError:
        print("An error has occured. This program doesn't have permission to open the file.")

    except FileNotFoundError:
        print("An error has occured. "+  fileName + " doesn't exist.")
    
    except Exception as e:
        print("An unexpected error occurred: " , e)

'''
Provides the text of a line so edit Info can replace the line with the password
@Input = int(line number) str(password)
@Output = nothing
'''
def editPassword(lineNum, password):
    lineText = "Password: " + password + "\n"
    editInfo(lineNum, lineText, DETAILS)



'''
Provides the text of a line so edit Info can replace the line with the Pin
@Input = int(line number) str(pin)
@Output = nothing
'''
def editPin(lineNum, pin):
    lineText = "Pin: " + pin +  "\n"
    editInfo(lineNum, lineText, CARD)



'''
writes info to txt file
@Input = (string)password, (string)username, and (string)fileName
@Output = nothing
'''
def writeAccountInfo(password, username, fileName):
    try:
        f = open(FOLDER + fileName, "a")
        f.write("---------------------------------------------------------" + "\n" +
                "Username: " + username + "\n" +
                "Password: " + password + "\n" +
                "---------------------------------------------------------" + "\n")
        f.close()
    except PermissionError:
        print("An error has occured. This program doesn't have permission to open the file.")

    except FileNotFoundError:
        print("An error has occured. "+  fileName + " doesn't exist.")
    
    except Exception as e:
        print("An unexpected error occurred: " , e)
    


if __name__=="__main__": 
    main()