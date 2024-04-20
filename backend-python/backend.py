import time
import mysql.connector
import bcrypt
from datetime import datetime, timedelta


try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="testing_password",
    database="PagePal"
    )
except:
    print("Database connection failed!")
    exit()

mycursor = mydb.cursor()

# def register(username, password):
#     # Hash the password
#     hashed_password = str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
#     mycursor.execute("INSERT INTO Address (firstline, secondline, city, state, country, pincode) VALUES (NULL, NULL, NULL, NULL, NULL, NULL);")
#     mycursor.execute("INSERT INTO Users (username, password, passwordattempt, logintries, loginsuccesful, blocklogintill, addressid, paypalcoins, productpreferencescart, vendor) VALUES (%s,%s,'',0,FALSE,%s,(SELECT LAST_INSERT_ID()),0,NULL,FALSE);",(username,password,int(time.time())))
#     mydb.commit()
#     print("Registration successful!")

def book_donation_page(userid):
    print("Welcome to the donation page!")
    print("Please enter the details of the book you would like to donate.\n")
    book_name = input("Book Name: ")
    author = input("Author: ")
    genre = input("Genre: ")
    quantity = int(input("Quantity: "))
    price = 50

    if not book_name or not genre or quantity <= 0:
        print("Enter valid details")
        return

    collection_date_str = input("Select a date for book collection (YYYY-MM-DD): ")
    try:
        collection_date = datetime.strptime(collection_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please enter date in YYYY-MM-DD format.")
        return
    status = None
    if collection_date == datetime.now().date():
        status = "collected"
        print("Your delivery has been collected, refurbished and is ready to be sold")
        time.sleep(3)

        mycursor.execute("SELECT book_id, quantity, price FROM Catalogue WHERE book_name = %s", (book_name,))
        existing_book = mycursor.fetchone()

        if existing_book:
            b_id, existing_quantity, price = existing_book
            mycursor.execute("UPDATE Catalogue SET quantity = %s WHERE book_id = %s", (existing_quantity + quantity, b_id))
            print("\nBook added to catalogue!\n")
        else:
            mycursor.execute("INSERT INTO Catalogue (book_name, author, genre, quantity) VALUES (%s, %s, %s, %s)", (book_name, author, genre, quantity))
    else:
        print("Your delivery will be collected on", collection_date)
        status = "pending"
    
    mycursor.execute("INSERT INTO DonatedHistory (userid, timestamp, book_id, book_quantity, total_cost, collection_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (userid, datetime.now(), b_id, quantity, price, collection_date, "Pending"))
    mydb.commit()


def register(username, password):
    if username is None or len(username) < 3:
        print("Error: Minimum of 3 characters are required for the username.")
        return
    elif not username[0].isalpha():
        print("Error: Username can only begin with alphabets.")
        return

    try:
        mydb.start_transaction()
        mycursor.execute("SELECT COUNT(*) FROM Users WHERE username = %s", (username,))
        result = mycursor.fetchone()
        if result and result[0] > 0:
            print("Error: Username already exists. Please choose a different username.")
            mydb.rollback()
            return
        mycursor.execute("INSERT INTO Address (firstline, secondline, city, state, country, pincode) VALUES (NULL, NULL, NULL, NULL, NULL, NULL);")
        mycursor.execute("INSERT INTO Users (username, password, passwordattempt, logintries, loginsuccesful, blocklogintill, addressid, paypalcoins, productpreferencescart, vendor) VALUES (%s,%s,'',0,FALSE,%s,(SELECT LAST_INSERT_ID()),0,NULL,FALSE);",(username,password,int(time.time())))
        mydb.commit()
        print("Registration successful!")
    except mysql.connector.Error as err:
        if "chk_username_length" in str(err):
            print("Error: Minimum of 3 characters are required for the username.")
        elif "chk_username_start_alpha" in str(err):
            print("Error: Username can only begin with alphabets.")
        else:
            print("Error during registration:", err)
        mydb.rollback()


def show_catalog(userid, cart):
    mycursor.execute("SELECT book_id, book_name, price, quantity, genre FROM Catalogue WHERE quantity > 0;")
    available_items = mycursor.fetchall()
    print("Available Items:\n")
    i = 1
    for item in available_items:
        print(f"{i}. Name: {item[1]}, Price: {item[2]}, Quantity: {item[3]}, Genre: {item[4]}")
        i+=1
    print('''\nWhat would you like to do?
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
            mydb.commit()
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
        print("\n------------℄------------")
        print('''📖 PagePal में आपका स्वागत है! 📖
            1. View Catalogue
            2. View Cart
            3. Donate!
            4. Logout
            ''')
        print("------------℄------------\n")
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
                        cart.remove(item)
                    mycursor.execute("UPDATE Catalogue SET quantity = quantity - %s WHERE book_id = %s;", (item[1], item[0]))
                    mycursor.execute("INSERT INTO OrderedHistory (userid, book_id, book_quantity, total_cost) VALUES (%s, %s, %s, %s);", (userid, item[0], item[1], item[2]*item[3]))
                mydb.commit()
                print("Purchase of Rs. %s successful!\nThank you for your purchase!", cost)

        elif (choice == "3"):
            book_donation_page(userid)

        elif (choice == "4"):
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
        print("\n------------℄------------")
        print("1. Register")
        print("2. Login")
        print("3. Quit")
        print("------------℄------------\n")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Note: Usernames are NOT case-sensitive.")
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

