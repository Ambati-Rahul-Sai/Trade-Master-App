from datetime import datetime
from threading import Lock

from data_layer import DataStore
from domain_classes import BuyTransaction, SellTransaction, Stock
from service_layer.stock_service import StockService


class StockServiceImpl(StockService):
    def __init__(self):
        self.data_store = DataStore.get_instance()
        self.lock = Lock()

    def get_available_stocks(self):
        return self.data_store.get_stocks()

    def calculate_average_stock_value(self, stock_symbol, from_year, to_year):
        stock = self.data_store.get_stock(Stock(stock_symbol))
        if stock:
            average = self.data_store.calculate_average(stock_symbol, from_year, to_year)
            return average
        else:
            print("Invalid stock symbol! Please try again.")

    def buy_stock(self, username, stock_symbol, quantity, transaction_type):
        with self.lock:
            stock = self.data_store.get_stock(Stock(stock_symbol))
            if stock:
                available_quantity = stock.quantity
                if quantity <= available_quantity:
                    transaction_date = datetime.now()
                    self.data_store.add_buy_transaction(BuyTransaction(username, stock_symbol, quantity, transaction_date, transaction_type))
                    new_quantity = available_quantity - quantity
                    self.data_store.update_stock(Stock(stock_symbol, quantity=new_quantity))
                    print(f"Bought {quantity} share(s) of {stock_symbol} for {username}")
                else:
                    print(f"Invalid Quantity! There are currently {available_quantity} share(s) of {stock_symbol}")
            else:
                print("Invalid stock symbol! Please try again.")

    def sell_stock(self, username, stock_symbol, quantity, transaction_type):
        with self.lock:
            stock = self.data_store.get_stock(Stock(stock_symbol))
            if stock:
                bought = self.data_store.total_stocks_bought(username, stock_symbol, "BUY")
                sold = self.data_store.total_stocks_sold(username, stock_symbol, "SELL")
                available_quantity = bought - sold
                if quantity <= available_quantity:
                    transaction_date = datetime.now()
                    self.data_store.add_sell_transaction(SellTransaction(username, stock_symbol, quantity, transaction_date, transaction_type))
                    new_quantity = available_quantity + quantity
                    self.data_store.update_stock(Stock(stock_symbol, quantity=new_quantity))
                    print(f"Sold {quantity} share(s) of {stock_symbol} for {username}")
                else:
                    print(f"Invalid Quantity! You have currently {available_quantity} share(s) of {stock_symbol}")
            else:
                print("Invalid stock symbol! Please try again.")

