import psycopg2
from psycopg2 import sql

from domain_classes.transaction import Transaction


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
        query = sql.SQL("SELECT username, stock_symbol, quantity, date, transaction_type FROM transactions WHERE "
                        "username = %s")
        self.cursor.execute(query, (user.username,))
        transactions = self.cursor.fetchall()
        return [Transaction(*transaction) for transaction in transactions]

    def total_stocks(self, username, stock_symbol, transaction_type):
        query = sql.SQL("SELECT SUM(quantity) FROM transactions WHERE username = %s AND transaction_type = %s AND "
                        "stock_symbol = %s")
        self.cursor.execute(query, (username, transaction_type, stock_symbol))
        result = self.cursor.fetchone()
        return result[0] if result[0] is not None else 0

