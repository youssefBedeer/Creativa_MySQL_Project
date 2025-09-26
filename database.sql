USE real_estate;

CREATE TABLE IF NOT EXISTS Employee (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Office_NUM INT
);

CREATE TABLE IF NOT EXISTS Sales_office (
    NUM INT AUTO_INCREMENT PRIMARY KEY,
    Location VARCHAR(255) NOT NULL,
    Manager_ID INT UNIQUE,
    FOREIGN KEY (Manager_ID) REFERENCES Employee(ID)
);


CREATE TABLE IF NOT EXISTS Property (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Address VARCHAR(255) NOT NULL,
    City VARCHAR(100) NOT NULL,
    State VARCHAR(100) NOT NULL,
    Zip VARCHAR(20) NOT NULL,
    Office_NUM INT NOT NULL,
    FOREIGN KEY (Office_NUM) REFERENCES Sales_office(NUM)
);

CREATE TABLE IF NOT EXISTS Owner (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Ownership (
    Property_ID INT NOT NULL,
    Owner_ID INT NOT NULL,
    Percent_owned DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (Property_ID, Owner_ID),
    FOREIGN KEY (Property_ID) REFERENCES Property(ID),
    FOREIGN KEY (Owner_ID) REFERENCES Owner(ID)
);



-- Insert into Employee
INSERT INTO Employee (Name, Office_NUM) VALUES
('Ali Hassan', NULL),
('Mona Ibrahim', NULL),
('Khaled Mostafa', NULL);

-- Insert into Sales_office
INSERT INTO Sales_office (Location, Manager_ID) VALUES
('Cairo', 1),   -- Ali Hassan هو المدير
('Alexandria', 2),  -- Mona Ibrahim هي المديرة
('Giza', 3);    -- Khaled Mostafa هو المدير

-- Update Employee.Office_NUM (علشان يربط كل موظف بالمكتب بتاعه)
UPDATE Employee SET Office_NUM = 1 WHERE ID = 1;
UPDATE Employee SET Office_NUM = 2 WHERE ID = 2;
UPDATE Employee SET Office_NUM = 3 WHERE ID = 3;

-- Insert into Property
INSERT INTO Property (Address, City, State, Zip, Office_NUM) VALUES
('12 Tahrir St', 'Cairo', 'Cairo', '11511', 1),
('25 Corniche Rd', 'Alexandria', 'Alex', '21915', 2),
('50 Pyramids Rd', 'Giza', 'Giza', '12556', 3);

-- Insert into Owner
INSERT INTO Owner (Name) VALUES
('Hany Saad'),
('Sara Adel'),
('Omar Fathy');

-- Insert into Ownership (property-owner relation)
INSERT INTO Ownership (Property_ID, Owner_ID, Percent_owned) VALUES
(1, 1, 100.0),   -- Hany owns Cairo property
(2, 2, 60.0),    -- Sara owns 60% of Alexandria property
(2, 3, 40.0);    -- Omar owns 40% of Alexandria property
