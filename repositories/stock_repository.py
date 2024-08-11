import psycopg2
from psycopg2 import sql

from domain_classes import Stock


class StockRepository:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            dbname='trademaster',
            password='Rahul_21'
        )
        self.cursor = self.connection.cursor()

    def create_stock(self, stock):
        query = sql.SQL("INSERT INTO stocks (symbol, price, quantity) VALUES (%s, %s, %s)")
        self.cursor.execute(query, (stock.symbol, stock.price, stock.quantity))
        self.connection.commit()

    def get_stock(self, stock):
        query = sql.SQL("SELECT symbol, price, quantity FROM stocks WHERE symbol = %s")
        self.cursor.execute(query, (stock.symbol,))
        stock = self.cursor.fetchone()
        if stock:
            return Stock(*stock)
        return None

    def get_stocks(self):
        query = sql.SQL("SELECT symbol, price, quantity FROM stocks")
        self.cursor.execute(query)
        stocks = self.cursor.fetchall()
        if stocks:
            return [Stock(*stock) for stock in stocks]

    def update_stock(self, stock):
        if stock.price and stock.quantity:
            query = sql.SQL("UPDATE stocks SET price = %s, quantity = %s WHERE symbol = %s")
            self.cursor.execute(query, (stock.price, stock.quantity, stock.symbol))
        elif stock.price:
            query = sql.SQL("UPDATE stocks SET price = %s WHERE symbol = %s")
            self.cursor.execute(query, (stock.price, stock.symbol))
        elif stock.quantity:
            query = sql.SQL("UPDATE stocks SET quantity = %s WHERE symbol = %s")
            self.cursor.execute(query, (stock.quantity, stock.symbol))
        self.connection.commit()

    def delete_stock(self, stock):
        query = sql.SQL("DELETE FROM stocks WHERE symbol = %s")
        self.cursor.execute(query, (stock.symbol,))
        self.connection.commit()

