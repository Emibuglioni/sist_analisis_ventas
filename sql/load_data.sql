-- Crear db
CREATE DATABASE IF NOT EXISTS ventas_db;
USE ventas_db;

-- Crear tablas según la estructura de los archivos
CREATE TABLE IF NOT EXISTS categories (
    CategoryID INT PRIMARY KEY,
    CategoryName VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS countries (
    CountryID INT PRIMARY KEY,
    CountryName VARCHAR(100) NOT NULL,
    CountryCode VARCHAR(3)
);

CREATE TABLE IF NOT EXISTS cities (
    CityID INT PRIMARY KEY,
    CityName VARCHAR(100) NOT NULL,
    Zipcode VARCHAR(10),
    CountryID INT,
    FOREIGN KEY (CountryID) REFERENCES countries(CountryID)
);

CREATE TABLE IF NOT EXISTS customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    MiddleInitial CHAR(1),
    LastName VARCHAR(50) NOT NULL,
    CityID INT,
    Address VARCHAR(200),
    FOREIGN KEY (CityID) REFERENCES cities(CityID)
);

CREATE TABLE IF NOT EXISTS employees (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    MiddleInitial CHAR(1),
    LastName VARCHAR(50) NOT NULL,
    BirthDate DATE,
    Gender CHAR(1),
    CityID INT,
    HireDate DATE,
    FOREIGN KEY (CityID) REFERENCES cities(CityID)
);

CREATE TABLE IF NOT EXISTS products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    CategoryID INT,
    Class VARCHAR(50),
    ModifyDate DATETIME(3),
    Resistant BOOLEAN,
    IsAllergic BOOLEAN,
    VitalityDays INT,
    FOREIGN KEY (CategoryID) REFERENCES categories(CategoryID)
);

CREATE TABLE IF NOT EXISTS sales (
    SalesID INT PRIMARY KEY,
    SalesPersonID INT,
    CustomerID INT,
    ProductID INT,
    Quantity INT NOT NULL,
    Discount DECIMAL(5,2),
    TotalPrice DECIMAL(10,2) NOT NULL,
    SalesDate DATETIME(3),
    TransactionNumber VARCHAR(50),
    FOREIGN KEY (SalesPersonID) REFERENCES employees(EmployeeID),
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

-- Cargar datos desde archivos CSV 
LOAD DATA LOCAL INFILE 'C:\\Users\\lenovo\\Desktop\\Data Engineer\\Proyecto Integrador\\data\\categories.csv'
INTO TABLE categories
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(CategoryID, CategoryName);

LOAD DATA LOCAL INFILE 'C:\\Users\\lenovo\\Desktop\\Data Engineer\\Proyecto Integrador\\data\\countries.csv'
INTO TABLE countries
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(CountryID, CountryName, CountryCode);

LOAD DATA LOCAL INFILE 'C:\\Users\\lenovo\\Desktop\\Data Engineer\\Proyecto Integrador\\data\\cities.csv'
INTO TABLE cities
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(CityID, CityName, Zipcode, CountryID);

LOAD DATA LOCAL INFILE 'C:\\Users\\lenovo\\Desktop\\Data Engineer\\Proyecto Integrador\\data\\customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(CustomerID, FirstName, MiddleInitial, LastName, CityID, Address);

LOAD DATA LOCAL INFILE 'C:\\Users\\lenovo\\Desktop\\Data Engineer\\Proyecto Integrador\\data\\employees.csv'
INTO TABLE employees
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(EmployeeID, FirstName, MiddleInitial, LastName, BirthDate, Gender, CityID, HireDate);

-- Para products y sales, usamos variables @var para transformar las fechas
LOAD DATA LOCAL INFILE 'C:\\Users\\lenovo\\Desktop\\Data Engineer\\Proyecto Integrador\\data\\products.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(ProductID, ProductName, Price, CategoryID, Class, @ModifyDate, Resistant, IsAllergic, VitalityDays)
SET ModifyDate = DATE_ADD(
    DATE_ADD(
        DATE_ADD(
            CURRENT_TIMESTAMP(3),
            INTERVAL SUBSTRING_INDEX(SUBSTRING_INDEX(@ModifyDate, '.', 1), ':', 1) MINUTE
        ),
        INTERVAL SUBSTRING_INDEX(SUBSTRING_INDEX(@ModifyDate, '.', 1), ':', -1) SECOND
    ),
    INTERVAL SUBSTRING_INDEX(@ModifyDate, '.', -1) * 100 MICROSECOND
);

LOAD DATA LOCAL INFILE 'C:\\Users\\lenovo\\Desktop\\Data Engineer\\Proyecto Integrador\\data\\sales.csv'
INTO TABLE sales
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(SalesID, SalesPersonID, CustomerID, ProductID, Quantity, Discount, TotalPrice, @SalesDate, TransactionNumber)
SET SalesDate = DATE_ADD(
    DATE_ADD(
        DATE_ADD(
            CURRENT_TIMESTAMP(3),
            INTERVAL SUBSTRING_INDEX(SUBSTRING_INDEX(@SalesDate, '.', 1), ':', 1) MINUTE
        ),
        INTERVAL SUBSTRING_INDEX(SUBSTRING_INDEX(@SalesDate, '.', 1), ':', -1) SECOND
    ),
    INTERVAL SUBSTRING_INDEX(@SalesDate, '.', -1) * 100 MICROSECOND
); 