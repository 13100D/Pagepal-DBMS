import time
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="testing_password",
  database="pagepal"
)

