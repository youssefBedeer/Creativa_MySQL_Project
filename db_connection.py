import pymysql
from pymysql.cursors import DictCursor

# Singleton Database Connection Class
class Database:
    __instance = None  # attribute to hold single instance
    
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__new__(cls)
        return cls.__instance
    
    def __init__(self, host="localhost", user="root", password="123456789", db="mysql"):
        if not hasattr(self, "connection"):  # prevent reinitializing
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db,
                cursorclass=DictCursor
            )
            
            self.cursor = self.connection.cursor()
            self.__instance.database = db
    
    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()
    
    def commit(self):
        self.connection.commit()
    
    def close(self):
        self.cursor.close()
        self.connection.close()


