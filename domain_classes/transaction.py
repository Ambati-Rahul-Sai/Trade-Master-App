from datetime import datetime


class Transaction:
    def __init__(self, username, stock_symbol, quantity, date, transaction_type):
        self.username = username
        self.stock_symbol = stock_symbol
        self.quantity = quantity
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f') if isinstance(date, str) else date
        self.transaction_type = transaction_type

    # def __str__(self):
    #     return f"{self.__class__.__name__}: {self.stock_symbol} x {self.quantity} on {self.date}"


class BuyTransaction(Transaction):
    pass


class SellTransaction(Transaction):
    pass

