from threading import Lock
from data_layer import DataStore
from domain_classes import BuyTransaction, SellTransaction


class StockService:

    def buy_stock(self, username, stock_symbol, quantity):
        pass

    def sell_stock(self, username, stock_symbol, quantity):
        pass

    def get_available_stocks(self):
        pass


class StockServiceImpl(StockService):
    def __init__(self):
        self.data_store = DataStore.get_instance()
        self.lock = Lock()

    def buy_stock(self, username, stock_symbol, quantity):
        with self.lock:
            transaction_info = BuyTransaction(username, stock_symbol, quantity)
            stock_info = [stock_symbol, quantity]
            self.data_store.add_buy_transaction(transaction_info, stock_info)
            print(f"Bought {quantity} share(s) of {stock_symbol} for {username}")

    def sell_stock(self, username, stock_symbol, quantity):
        with self.lock:
            user_transactions = self.data_store.get_transactions(username)
            if stock_symbol not in user_transactions["stocks"]:
                print(f"Transaction Failed: You haven't bought the stock-{stock_symbol} yet, so you can't sell it.")
            elif quantity > user_transactions["stocks"][stock_symbol]:
                print(f"Invalid quantity! You can't sell more shares than you have purchased.\n"
                      f"You have bought only {user_transactions["stocks"][stock_symbol]} shares of {stock_symbol}")
            else:
                transaction_info = SellTransaction(username, stock_symbol, quantity)
                stock_info = [stock_symbol, quantity]
                self.data_store.add_sell_transaction(transaction_info, stock_info)
                print(f"Sold {quantity} share(s) of {stock_symbol} for {username}")

    def get_available_stocks(self):
        return self.data_store.get_stocks()
