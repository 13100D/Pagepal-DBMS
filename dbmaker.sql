CREATE DATABASE IF NOT EXISTS PagePal;
USE PagePal;
-- Address table
CREATE TABLE Address (
addressid INT PRIMARY KEY AUTO_INCREMENT,
firstline VARCHAR(255),
secondline VARCHAR(255),
city VARCHAR(100),
state VARCHAR(100),
country VARCHAR(100),
pincode VARCHAR(20)
);
-- Users table
CREATE TABLE Users (
userid INT PRIMARY KEY,
username VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
addressid INT,
paypalcoins INT,
productpreferencescart TEXT,
vendor BOOLEAN,
FOREIGN KEY (addressid) REFERENCES Address(addressid)
);
-- Vendor table
CREATE TABLE Vendor (
vendorid INT PRIMARY KEY,
name VARCHAR(255),
contact VARCHAR(100),
addressid INT,
FOREIGN KEY (addressid) REFERENCES Address(addressid)
);
-- RefurbishmentCenter table
CREATE TABLE RefurbishmentCenter (
center_id INT PRIMARY KEY,
addressid INT,
contact VARCHAR(100),
FOREIGN KEY (addressid) REFERENCES Address(addressid)
);
-- Catalogue table
CREATE TABLE Catalogue (
book_id INT PRIMARY KEY,
book_name VARCHAR(255),
quantity INT,
vendor_id INT,
status VARCHAR(100),
FOREIGN KEY (vendor_id) REFERENCES Vendor(vendorid)
);
-- OrderedHistory table
CREATE TABLE OrderedHistory (
transactioniduserid INT,
timestamp TIMESTAMP,
book_id INT,
book_quantity INT,
total_cost DECIMAL(10, 2),
status VARCHAR(100),
FOREIGN KEY (userid) REFERENCES Users(userid),
FOREIGN KEY (book_id) REFERENCES Catalogue(book_id)
);
-- DonatedHistory table
CREATE TABLE DonatedHistory (
transactionid INT PRIMARY KEY,
userid INT,
timestamp TIMESTAMP,
book_id INT,
book_quantity INT,
total_cost DECIMAL(10, 2),
status VARCHAR(100),
FOREIGN KEY (userid) REFERENCES Users(userid),
FOREIGN KEY (book_id) REFERENCES Catalogue(book_id)
);