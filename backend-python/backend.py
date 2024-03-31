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
    mycursor.execute(f'''INSERT INTO Address (firstline, secondline, city, state, country, pincode)
VALUES (NULL, NULL, NULL, NULL, NULL, NULL);''')
    print(f'''INSERT INTO Users (username, password, passwordattempt, logintries, loginsuccesful, blocklogin, addressid, paypalcoins, productpreferencescart, vendor)
VALUES (
    -- Provide values for the new user
    '''+"'"+username+"'"+''', -- Username
    '''+"'"+password+"'"+''', -- Initial password
    '', -- Password attempt (initially empty)
    0, -- Initial login tries
    FALSE, -- Initial login successful status
    FALSE, -- Initial login block status
    (SELECT LAST_INSERT_ID()), -- Example addressid (replace with appropriate value)
    0, -- Initial PayPal coins balance
    NULL, -- Initial product preferences cart (can be NULL or empty)
    FALSE -- Not a vendor (change to TRUE if user is a vendor)
    );''')

    print("Registration successful!")



def login(username, password):
    hashed_password = str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
    #not used rn kek


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

