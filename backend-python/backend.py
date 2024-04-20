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
    mycursor.execute("INSERT INTO Users (username, password, passwordattempt, logintries, loginsuccesful, blocklogintill, addressid, paypalcoins, productpreferencescart, vendor) VALUES (%s,%s,'',0,FALSE,%s,(SELECT LAST_INSERT_ID()),0,NULL,FALSE);",(username,password,int(time.time())))
    mydb.commit()
    print("Registration successful!")

def show_catalog(userid, cart):
    mycursor.execute("SELECT book_id, book_name, price, quantity FROM Catalogue WHERE quantity > 0;")
    available_items = mycursor.fetchall()
    print("Available Items:")
    i = 1
    for item in available_items:
        print(f"{i}. Name: {item[1]}, Price: {item[2]}, Quantity: {item[3]}")
        i+=1
    print('''What would you like to do?
          1. Buy book
          2. Add to cart
          3. Go back''')
    choice = input("Enter your choice: ")
    if choice == "1":
        item = input("Enter the item number: ")
        item_buying = available_items[item-1]
        item_quantity = input("Enter the quantity: ")
        if item_buying[3] < item_quantity:
            print("Not enough stock!")
        else:
            mycursor.execute("UPDATE Catalogue SET quantity = quantity - %s WHERE book_id = %s;", (item_quantity, item_buying[0]))
            mycursor.execute("INSERT INTO OrderedHistory (userid, book_id, book_quantity, total_cost) VALUES (%s, %s, %s, %s);", (userid, item_buying[0], item_quantity, item_buying[2]*item_quantity))
            print("Purchase successful!")
    elif choice == "2":
        item = input("Enter the item number: ")
        item_for_cart = available_items[item-1]
        item_quantity = input("Enter the quantity: ")
        cart.append([item_for_cart[0], item_for_cart[1], item_quantity, item_for_cart[2]])
        print("Item added to cart!")
    elif choice == "3":
        pass
    else:
        print("Invalid choice!")

def user_inside(userid):
    cart = [[]]
    while True:
        print('''PagePal में आपका स्वागत है!
            1. View Catalogue
            2. View Cart
            3. Logout
            ''')
        choice = input("Enter your choice: ")
        if (choice == "1"):
            show_catalog(userid, cart)
        elif choice == "2":
            for item in cart:
                mycursor.execute("SELECT book_id, book_name, price, quantity FROM Catalogue WHERE book_id = %s;", (item[0],))
                if (item[3] > mycursor.fetchone()[3]):
                    print("Not enough stock of %s!", item[1])
                    continue
                print(f"Name: {item[1]}, Quantity: {item[2]}, Price: {item[3]}")
            print("Total: ", sum([item[1]*item[2] for item in cart]))
            choice = input("Would you like to checkout? (y/n)")
            # cart
            if (choice == 'y'):
                cost = 0 
                for item in cart:
                    mycursor.execute("SELECT quantity FROM Catalogue WHERE book_id = %s;", (item[0],))
                    if (item[2] > mycursor.fetchone()[0]):
                        print("Not enough stock of %s!", item[1])
                        continue
                    else:
                        cost += item[2]*item[3]
                    mycursor.execute("UPDATE Catalogue SET quantity = quantity - %s WHERE book_id = %s;", (item[1], item[0]))
                    mycursor.execute("INSERT INTO OrderedHistory (userid, book_id, book_quantity, total_cost) VALUES (%s, %s, %s, %s);", (userid, item[0], item[1], item[2]*item[3]))
                print("Purchase of Rs. %s successful!\nThank you for your purchase!", cost)
                
        elif (choice == "3"):
            print("Goodbye!")
            break

def login(username, password):
    hashed_password = str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
    #not used rn kek
    mycursor.execute("SELECT blocklogintill FROM Users WHERE username = %s", [username])
    blocklogintill= mycursor.fetchone()[0]
    if (blocklogintill<time.time()):
        loginsuccess=False
        print("loginprocedurestarted")
        #send password creds to database
        #still pending
        mycursor.execute("UPDATE Users SET passwordattempt = %s WHERE username = %s", (password,username))
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
        else:
            user_inside(userid)
    else:
        print("too many attempts try after", blocklogintill-time.time(), "seconds")
    
        

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
            mydb.close()
            break
        else:
            print("Invalid choice!")

