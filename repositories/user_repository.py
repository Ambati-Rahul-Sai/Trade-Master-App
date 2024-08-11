import psycopg2
from psycopg2 import sql

from domain_classes import User


class UserRepository:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            dbname='trademaster',
            password='Rahul_21'
        )
        self.cursor = self.connection.cursor()

    def create_user(self, user):
        query = sql.SQL("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)")
        self.cursor.execute(query, (user.username, user.password, user.email))
        self.connection.commit()

    def get_user(self, user):
        if user.password:
            query = sql.SQL("SELECT username, password, email FROM users WHERE username = %s AND password = %s")
            self.cursor.execute(query, (user.username, user.password))
        else:
            query = sql.SQL("SELECT username, password, email FROM users WHERE username = %s")
            self.cursor.execute(query, (user.username,))
        user = self.cursor.fetchone()
        if user:
            return User(*user)
        return None

    def update_user(self, user):
        if user.password and user.email:
            query = sql.SQL("UPDATE users SET password = %s, email = %s WHERE username = %s")
            self.cursor.execute(query, (user.password, user.email, user.username))
        elif user.password:
            query = sql.SQL("UPDATE users SET password = %s WHERE username = %s")
            self.cursor.execute(query, (user.password, user.username))
        elif user.email:
            query = sql.SQL("UPDATE users SET email = %s WHERE username = %s")
            self.cursor.execute(query, (user.email, user.username))
        self.connection.commit()

    def delete_user(self, user):
        query = sql.SQL("DELETE FROM users WHERE username = %s")
        self.cursor.execute(query, (user.username,))
        self.connection.commit()
