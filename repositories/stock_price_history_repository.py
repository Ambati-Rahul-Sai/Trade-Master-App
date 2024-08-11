import psycopg2
from psycopg2 import sql

from domain_classes.stock_price_history import StockPriceHistory


class StockPriceHistoryRepository:
    def __init__(self):
        self.connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            dbname='trademaster',
            password='Rahul_21'
        )
        self.cursor = self.connection.cursor()

    def add_stock_price_history(self, history):
        query = sql.SQL("INSERT INTO stock_price_history (stock_symbol, price, year) VALUES (%s, %s, %s)")
        self.cursor.execute(query, (history.stock_symbol, history.price, history.year))
        self.connection.commit()

    def get_stock_price_history(self, stock_symbol, from_year, to_year):
        query = sql.SQL("SELECT * FROM stock_price_history WHERE stock_symbol = %s AND year BETWEEN %s AND %s")
        self.cursor.execute(query, (stock_symbol, from_year, to_year))
        history = self.cursor.fetchall()
        return [StockPriceHistory(*record) for record in history]

    def get_average_stock_value(self, stock_symbol, from_year, to_year):
        query = sql.SQL("SELECT AVG(price) FROM stock_price_history WHERE stock_symbol = %s AND year BETWEEN %s AND %s")
        self.cursor.execute(query, (stock_symbol, from_year, to_year))
        average = self.cursor.fetchone()
        return average[0]
