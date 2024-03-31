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
userid INT PRIMARY KEY AUTO_INCREMENT,
username VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
passwordattempt VARCHAR(255),
logintries INT,
loginsuccesful BOOLEAN,
blocklogintill INT,
addressid INT,
paypalcoins INT,
productpreferencescart TEXT,
vendor BOOLEAN,
FOREIGN KEY (addressid) REFERENCES Address(addressid)
);
-- Vendor table
CREATE TABLE Vendor (
vendorid INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(255),
contact VARCHAR(100),
addressid INT,
FOREIGN KEY (addressid) REFERENCES Address(addressid)
);
-- RefurbishmentCenter table
CREATE TABLE RefurbishmentCenter (
center_id INT PRIMARY KEY AUTO_INCREMENT,
addressid INT,
contact VARCHAR(100),
FOREIGN KEY (addressid) REFERENCES Address(addressid)
);
-- Catalogue table
CREATE TABLE Catalogue (
book_id INT PRIMARY KEY AUTO_INCREMENT,
book_name VARCHAR(255),
price INT,
quantity INT,
vendor_id INT,
status VARCHAR(100),
FOREIGN KEY (vendor_id) REFERENCES Vendor(vendorid)
);
-- OrderedHistory table
CREATE TABLE OrderedHistory (
transactionid INT PRIMARY KEY AUTO_INCREMENT,
cartid INT,
timestamp TIMESTAMP,
userid INT,
book_id INT,
book_quantity INT,
total_cost DECIMAL(10, 2),
status VARCHAR(100),
FOREIGN KEY (userid) REFERENCES Users(userid),
FOREIGN KEY (book_id) REFERENCES Catalogue(book_id)
);
-- DonatedHistory table
CREATE TABLE DonatedHistory (
transactionid INT PRIMARY KEY AUTO_INCREMENT,
userid INT,
timestamp TIMESTAMP,
book_id INT,
book_quantity INT,
total_cost DECIMAL(10, 2),
status VARCHAR(100),
FOREIGN KEY (userid) REFERENCES Users(userid),
FOREIGN KEY (book_id) REFERENCES Catalogue(book_id)
);
CREATE TRIGGER login_attempt
BEFORE UPDATE ON Users
FOR EACH ROW
BEGIN
    DECLARE attempt_count INT;
    DECLARE block_time INT;

    IF NEW.passwordattempt = NEW.password THEN
        SET NEW.loginsuccessful = TRUE;
        SET NEW.blocklogin = FALSE;
        SET NEW.logintries = 0;
    ELSE
        SET attempt_count = NEW.logintries + 1;

        IF attempt_count >= 3 THEN
            SET NEW.blocklogin = TRUE;
            SET block_time = UNIX_TIMESTAMP() + 60;
            SET NEW.blocklogintill = block_time;
        ELSE
            SET NEW.blocklogin = FALSE;
        END IF;

        SET NEW.logintries = attempt_count;
    END IF;
END;
