-- Create Office table first, as it's referenced by other tables
CREATE TABLE Office (
    address VARCHAR(255) PRIMARY KEY,
    size INT,
    office_id INT,
    vacancy BOOLEAN
);

-- Create Department table
CREATE TABLE Department (
    dep_id INT PRIMARY KEY,
    emp_count INT,
    head_of_department VARCHAR(255)
);

-- Create Branch table
CREATE TABLE Branch (
    Branch_id INT PRIMARY KEY,
    branch_address VARCHAR(255) REFERENCES Office (address),
    employee_count INT,
    no_customers INT
);

-- Create Sales table
CREATE TABLE Sales (
    sale_id INT PRIMARY KEY,
    profit DECIMAL(10, 2),
    costs DECIMAL(10, 2),
    item VARCHAR(255)
);

-- Create Papers table
CREATE TABLE Papers (
    class_id INT PRIMARY KEY,
    stock INT,
    cost DECIMAL(10, 2)
);

-- Create Binders table
CREATE TABLE Binders (
    class_id INT PRIMARY KEY,
    stock INT,
    cost DECIMAL(10, 2),
    capacity INT
);

-- Create Managers table
CREATE TABLE Managers (
    m_id INT PRIMARY KEY,
    branch_id INT REFERENCES Branch (Branch_id),
    year_joined INT,
    name VARCHAR(255),
    age INT
);

-- Create Employees table
CREATE TABLE Employees (
    e_id INT PRIMARY KEY,
    m_id INT REFERENCES Managers (m_id),
    year_joined INT,
    name VARCHAR(255),
    age INT,
    dep_id INT REFERENCES Department (dep_id)
);

-- Create Lease table
CREATE TABLE Lease (
    lease_id INT PRIMARY KEY,
    office_id INT REFERENCES Office (office_id),
    status VARCHAR(255),
    start_date DATE,
    end_date DATE
);