from datetime import datetime

import psycopg2
from psycopg2 import sql

from domain_classes.transaction import Transaction, BuyTransaction, SellTransaction


class TransactionRepository:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            dbname='trademaster',
            password='Rahul_21'
        )
        self.cursor = self.connection.cursor()

    def create_transaction(self, transaction):
        query = sql.SQL("INSERT INTO transactions (username, stock_symbol, quantity, date, transaction_type) VALUES ("
                        "%s, %s, %s, %s, %s)")
        self.cursor.execute(query, (transaction.username, transaction.stock_symbol, transaction.quantity, transaction.date, transaction.transaction_type))
        self.connection.commit()

    def get_transactions_by_username(self, user):
        query = sql.SQL("SELECT stock_symbol, quantity, date, transaction_type FROM transactions WHERE username = %s")
        self.cursor.execute(query, (user.username,))
        transactions = self.cursor.fetchall()
        result = []
        for transaction in transactions:
            stock_symbol, quantity, date, transaction_type = transaction
            if isinstance(date, datetime):
                date = date
            else:
                # If 'date' is a string, parse it
                date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            if transaction_type == "BUY":
                result.append(BuyTransaction(user.username, stock_symbol, quantity, date, transaction_type))
            else:
                result.append(SellTransaction(user.username, stock_symbol, quantity, date, transaction_type))

        return result

    def delete_user_transactions(self, user):
        query = sql.SQL("DELETE FROM transactions WHERE username = %s")
        self.cursor.execute(query, (user.username,))
        self.connection.commit()

    def total_stocks(self, username, stock_symbol, transaction_type):
        query = sql.SQL("SELECT SUM(quantity) FROM transactions WHERE username = %s AND transaction_type = %s AND "
                        "stock_symbol = %s")
        self.cursor.execute(query, (username, transaction_type, stock_symbol))
        result = self.cursor.fetchone()
        return result[0] if result[0] is not None else 0

