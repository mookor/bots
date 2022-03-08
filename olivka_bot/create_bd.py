import imp
from bd import DataBase

db = DataBase()
db.execute(
    "CREATE TABLE IF NOT EXISTS Duty (User_id INTEGER PRIMARY KEY, Name TEXT, Phone TEXT, Email TEXT)"
)
db.execute(
    "CREATE TABLE IF NOT EXISTS Orders (Name TEXT, Order_products TEXT, Order_time timestamp)"
)
