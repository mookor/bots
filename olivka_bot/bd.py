import sqlite3
import datetime


class DataBase:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("motiv_olivka.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def execute(self, query, task=""):
        self.cursor.execute(query, task)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def add_duty(self, task):
        query = """ INSERT or IGNORE INTO Duty(User_id, Name , Phone , Email)
              VALUES(?,?,?,?) """
        self.execute(query, task)
        self.commit()

    def get_users(self):
        query = "SELECT User_id FROM Duty"
        self.execute(query)
        rows = self.cursor.fetchall()
        rows = [r[0] for r in rows]
        return rows

    def get_duty_by_id(self, user_id):
        user_id = (user_id,)
        query = f"SELECT * FROM Duty WHERE User_id == (?)"
        self.execute(query, task=user_id)
        rows = self.cursor.fetchall()
        rows = [r for r in rows[0]]
        name = rows[1]
        phone = rows[2]
        email = rows[3]
        return name, phone, email

    def add_order(self, name, order):
        order_time = datetime.datetime.now()
        task = (
            name,
            order,
            order_time,
        )
        query = "INSERT INTO Orders(Name, Order_products, Order_time) VALUES(?,?,?)"
        self.execute(query, task)
        self.commit()

    def get_today_orders(self):
        today = datetime.datetime.now()
        today_day = today.day
        today_year = today.year
        today_month = today.month
        today_hour = 20
        today_threshold = datetime.datetime(
            today_year, today_month, today_day, today_hour
        )
        yesterday_threshold = datetime.datetime(
            today_year, today_month, today_day - 1, today_hour
        )
        task = (
            yesterday_threshold,
            today_threshold,
        )
        query = "SELECT * FROM Orders WHERE Order_time BETWEEN ? AND ?"
        self.execute(query, task=task)
        rows = self.cursor.fetchall()
        return rows


# bd = DataBase()
# # x = bd.get_duty_by_id(1)
# bd.add_order("qwe", "qwe qwe")
# bd.get_today_orders()
# print(x)
