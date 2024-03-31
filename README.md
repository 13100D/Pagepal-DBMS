# Pagepal-DBMS
e-commerce application as a project for the DBMS course


# Database Schema

1. Address:
* addressid INT PRIMARY KEY AUTO_INCREMENT
* firstline VARCHAR(255)
* secondline VARCHAR(255)
* city VARCHAR(100)
* state VARCHAR(100)
* country VARCHAR(100)
* pincode VARCHAR(20)
  
2. Users:
* userid INT PRIMARY KEY
* username VARCHAR(255) NOT NULL
* password VARCHAR(255) NOT NULL
* passwordattempt VARCHAR(255)
* logintries INT
* loginsuccesful BOOLEAN
* blocklogin BOOLEAN
* addressid INT
* paypalcoins INT
* productpreferences TEXT
* cart TEXT
* vendor BOOLEAN
* FOREIGN KEY (addressid) REFERENCES Address(addressid)
  
3. Vendor:
* vendorid INT PRIMARY KEY
* name VARCHAR(255)
* addressid INT
* FOREIGN KEY (addressid) REFERENCES Address(addressid)
4. RefurbishmentCenter:
* center_id INT PRIMARY KEY
* addressid INT
* contact VARCHAR(100)
* FOREIGN KEY (addressid) REFERENCES Address(addressid)
  
5. Catalogue:
* book_id INT PRIMARY KEY
* book_name VARCHAR(255)
* quantity INT
* vendor_id INT
* status VARCHAR(100)
* FOREIGN KEY (vendor_id) REFERENCES Vendor(vendorid)
  
6. OrderedHistory:
* transactionid INT PRIMARY KEY
* cartID INT
* userid INT
* timestamp TIMESTAMP
* book_id INT
* book_quantity INT
* total_cost DECIMAL(10, 2)
* status VARCHAR(100)
* FOREIGN KEY (userid) REFERENCES Users(userid)
* FOREIGN KEY (book_id) REFERENCES Catalogue(book_id)
  
7. DonatedHistory:
* transactionid INT PRIMARY KEY
* userid INT
* timestamp TIMESTAMP
* book_id INT
* book_quantity INT
* total_cost DECIMAL(10, 2)
* status VARCHAR(100)
* FOREIGN KEY (userid) REFERENCES Users(userid)
* FOREIGN KEY (book_id) REFERENCES Catalogue(book_id)
