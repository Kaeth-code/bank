
import os
import random


FOLDER = "bankFiles/"
DETAILS = "account_details.txt"
CHEQUE = "chequing_money.txt"
SAVE = "savings_money.txt"
CARD = "card_info.txt"




'''
Gives the text on a line using line number
@Input = line number
@Output = text on that line
'''
def getLine(lineNum, fileName):
    line = ""
    try:
        f = open(FOLDER + fileName)
        line = f.readlines()
        
        info = line[lineNum].split(" ")
        return info[1][0:-1]
    



    except PermissionError:
        print("An error has occured. This program doesn't have permission to open the file.")

    except FileNotFoundError:
        print("An error has occured. "+  fileName + " doesn't exist.")
    
    except Exception as e:
        print("An unexpected error occurred: " , e)
    
    return None



'''
Finds the line after given word
@Input = username, filename
@Output = the line number
'''
def findLine(whichUsername, fileName):
    count = 0

    try:
        f = open(FOLDER + fileName)
        lines = f.readlines()

        while(count < (len(lines)-1)/5):
            lineCalc = 1 + (count*4)
            applications = lines[lineCalc].split(" ")
            if(applications[1][0:-1] == whichUsername):

                return lineCalc
            
            count += 1
        
    except PermissionError:
        print("An error has occured. This program doesn't have permission to open the file.")

    except FileNotFoundError:
        print("An error has occured. "+  fileName + " doesn't exist.")
    
    except Exception as e:
        print("An unexpected error occurred: " , e)
    return None


'''
Provides the text of a line so edit Info can replace the line with the money
@Input = int(line number) str(password), str(account)
@Output = nothing
'''
def editMoney(lineNum, totalAmount, account):
    lineText = "Money: " + str(totalAmount) + "\n"
    editInfo(lineNum, lineText, account)



'''
Edits the password to something the user wants it to be
@Input = line number in which the password is held and the new password
@Output = nothing
'''
def editInfo(lineNum, lineText, fileName):
    try:
        f = open(FOLDER + fileName)
        lines = f.readlines()
        lines[lineNum] = lineText
        f.close()

        os.remove(FOLDER + fileName)

        f = open(FOLDER + fileName, "a")
        text = "".join(lines)
        f.write(text)
        f.close()
        
    except PermissionError:
        print("An error has occured. This program doesn't have permission to open the file.")

    except FileNotFoundError:
        print("An error has occured. "+  fileName + " doesn't exist.")
    
    except Exception as e:
        print("An unexpected error occurred: " , e)



'''
Asks user whether they want to quit. Quits if y
@Input = nothing
@Output = nothing
'''
def userQuit():
    doQuit = input("Do you want to quit? ")
    if(doQuit == "y"):
        quit()
    return 
