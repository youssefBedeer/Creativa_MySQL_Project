from abc import ABC, abstractmethod
import sys
import os
import pandas as pd
# أضيف المسار الرئيسي للمشروع
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_connection import Database


# --------------Command Pattern--------------#
class Commands(ABC):
    @abstractmethod
    def execute(self):
        pass

class ShowTableCommand(Commands):
    def __init__(self, table, columns:list):
        self.table = table 
        self.columns = columns 
    
    def execute(self):
        db=Database() 
        if not self.columns:
            query = f"SELECT * FROM {self.table}"
        else:
            cols = ", ".join(self.columns)
            query = f"SELECT {cols} FROM {self.table}"
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        df = pd.DataFrame(rows)
        return df
    
class GetTableColumns(Commands):
    def __init__(self, table):
        self.table = table

    def execute(self):
        db=Database()
        db.cursor.execute(f"SHOW COLUMNS FROM {self.table}")
        return [row for row in db.cursor.fetchall()]

        

class AddRowCommand(Commands):
    def __init__(self, table:str, data:dict):
        self.table = table
        self.data = data 

    def execute(self):
        db = Database()
        columns = ", ".join(self.data.keys())
        placeholders = ", ".join(['%s']*len(self.data))
        values = tuple(self.data.values())

        query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        db.cursor.execute(query, values)
        db.commit()
        print(f"Row added successfully into '{self.table}' with data = {self.data}")

class DeleteRowCommand(Commands):
    def __init__(self, table:str, column, value):
        self.table = table 
        self.column = column
        self.value = value
    
    def execute(self):
        db = Database() 
        query = f"DELETE FROM {self.table} WHERE {self.column} = %s"
        db.cursor.execute(query, (self.value,))
        db.commit() 
        print(f"User with {self.column} = '{self.value}' deleted successfully.")
# --------------Factory Pattern--------------#
