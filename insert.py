import os
import sqlite3
import random

db_path = os.path.join(os.getcwd(), "real_estate.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# ----------------- Data Pools -----------------
cities = [
    ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"),
    ("Houston", "TX"), ("Phoenix", "AZ"), ("Miami", "FL"),
    ("Boston", "MA"), ("Seattle", "WA"), ("Denver", "CO"),
    ("Dallas", "TX"), ("San Diego", "CA")
]

first_names = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona",
               "George", "Hannah", "Ivan", "Julia", "Kevin", "Laura",
               "Michael", "Nina", "Oscar", "Paula", "Quinn", "Rachel",
               "Steve", "Tina", "Uma", "Victor", "Wendy", "Xander",
               "Yvonne", "Zack"]

last_names = ["Johnson", "Smith", "Brown", "Taylor", "Anderson", "Clark",
              "Lopez", "Martinez", "Wilson", "White", "Harris", "Lewis",
              "Walker", "Hall", "Allen", "Young"]

street_names = ["Main St", "Highland Ave", "Maple St", "Sunset Blvd",
                "Oak St", "Pine Rd", "Cedar Ave", "River Rd", "Lake Shore Dr",
                "Broadway", "Ocean Dr"]

# ----------------- Inserts -----------------

# Sales Offices
for city, state in cities[:8]:  # 8 offices
    cursor.execute("INSERT INTO Sales_office (Location, Manager_ID) VALUES (?, NULL);", (city,))

# Employees
for office_num in range(1, 9):
    for _ in range(random.randint(5, 10)):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        cursor.execute("INSERT INTO Employee (Name, Office_NUM) VALUES (?, ?);", (name, office_num))

# Assign random Managers
for office_num in range(1, 8+1):
    cursor.execute("SELECT ID FROM Employee WHERE Office_NUM=?;", (office_num,))
    emp_list = [row[0] for row in cursor.fetchall()]
    manager = random.choice(emp_list)
    cursor.execute("UPDATE Sales_office SET Manager_ID=? WHERE NUM=?;", (manager, office_num))

# Properties
for office_num in range(1, 9):
    for _ in range(random.randint(20, 30)):
        city, state = random.choice(cities)
        address = f"{random.randint(100, 9999)} {random.choice(street_names)}"
        zip_code = f"{random.randint(10000, 99999)}"
        cursor.execute("""
        INSERT INTO Property (Address, City, State, Zip, Office_NUM)
        VALUES (?, ?, ?, ?, ?);
        """, (address, city, state, zip_code, office_num))

# Owners
for _ in range(100):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    cursor.execute("INSERT INTO Owner (Name) VALUES (?);", (name,))

# Ownerships
cursor.execute("SELECT ID FROM Property;")
all_properties = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT ID FROM Owner;")
all_owners = [row[0] for row in cursor.fetchall()]

for prop in all_properties:
    owners = random.sample(all_owners, random.randint(1, 3))
    share = round(100 / len(owners), 2)
    for owner in owners:
        cursor.execute("INSERT INTO Ownership (Property_ID, Owner_ID, Percent_owned) VALUES (?, ?, ?);",
                       (prop, owner, share))

# Commit
conn.commit()
conn.close()

print("✅ Test data inserted!")
