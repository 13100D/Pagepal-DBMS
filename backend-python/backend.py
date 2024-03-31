import time
import mysql.connector
import bcrypt


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="testing_password",
  database="pagepal"
)


def register(username, password):
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # Store the username and hashed password in the database
    database[username] = hashed_password
    print("Registration successful!")



def login(username, password):
    # Check if the username exists in the database
    if username in database:
        # Check if the password matches the hashed password in the database
        if bcrypt.checkpw(password.encode('utf-8'), database[username]):
            print("Login successful!")
        else:
            print("Invalid password!")
    else:
        print("Username not found!")


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

