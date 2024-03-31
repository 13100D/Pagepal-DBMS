import time
import mysql.connector
import bcrypt


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="testing_password",
  database="PagePal"
)

mycursor = mydb.cursor()

def register(username, password):
    # Hash the password
    hashed_password = str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
    mycursor.execute("INSERT INTO Address (firstline, secondline, city, state, country, pincode) VALUES (NULL, NULL, NULL, NULL, NULL, NULL);")
    print(mycursor.fetchone())
    if mycursor.rowcount > 0:
        print("Inserted {} rows.".format(mycursor.rowcount))
    else:
        print("No rows were inserted.")
    mycursor.execute("INSERT INTO Users (username, password, passwordattempt, logintries, loginsuccesful, blocklogin, addressid, paypalcoins, productpreferencescart, vendor) VALUES (%s,%s,'',0,FALSE,FALSE,(SELECT LAST_INSERT_ID()),0,NULL,FALSE);",("'"+username+"'","'"+password+"'"))
    print(mycursor.fetchone())
    if mycursor.rowcount > 0:
        print("Inserted {} rows.".format(mycursor.rowcount))
    else:
        print("No rows were inserted.")
    mydb.commit()
    print("Registration successful!")



def login(username, password):
    hashed_password = str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
    #not used rn kek
    loginsuccess=False
    print("loginprocedurestarted")
    startts = time.time()
    while (time.time()-startts<=3):
        mycursor.execute("SELECT loginsuccesful,userid FROM Users WHERE username = %s AND password = %s", (username, password))
        row = mycursor.fetchone()
        userid=row[1]
        if row[0]:
            mycursor.execute("UPDATE Users SET loginsuccesful = FALSE WHERE username = %s AND password =%s", (username,password))
            loginsuccess=True
            break
        time.sleep(0.1)
    if (not loginsuccess):
        print("invalid credentials")
    
        

while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            login(username, password)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

