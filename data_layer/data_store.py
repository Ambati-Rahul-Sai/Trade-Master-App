from domain_classes import Stock


class DataStore:
    instance = None

    @staticmethod
    def get_instance():
        if DataStore.instance is None:
            DataStore()
        return DataStore.instance

    def __init__(self):
        if DataStore.instance is not None:
            raise Exception("An instance of DataStore already exists!")
        else:
            DataStore.instance = self
            self.users = {}
            self.stocks = {
                "SBI": Stock("SBI", 847.85),
                "ITC": Stock("ITC", 489.10),
                "TCS": Stock("TCS", 4283.05),
                "HDFC": Stock("HDFC", 1659.15)
            }
            self.transactions = {}

    def add_user(self, user):
        self.users[user.username] = user

    def get_user(self, username):
        return self.users.get(username)

    def get_stock(self, stock_symbol):
        return self.stocks.get(stock_symbol)

    def get_stocks(self):
        return list(self.stocks.values())

    def add_buy_transaction(self, transaction_info, stock_info):
        stock_symbol, quantity = stock_info
        if transaction_info.username not in self.transactions:
            self.transactions[transaction_info.username] = {}
            self.transactions[transaction_info.username]["orders"] = []
            self.transactions[transaction_info.username]["stocks"] = {}
        if stock_symbol not in self.transactions[transaction_info.username]["stocks"]:
            self.transactions[transaction_info.username]["stocks"][stock_symbol] = 0
        self.transactions[transaction_info.username]["stocks"][stock_symbol] += quantity
        self.transactions[transaction_info.username]["orders"].append(transaction_info)

    def add_sell_transaction(self, transaction_info, stock_info):
        stock_symbol, quantity = stock_info
        self.transactions[transaction_info.username]["stocks"][stock_symbol] -= quantity
        self.transactions[transaction_info.username]["orders"].append(transaction_info)

    def get_transactions(self, username):
        return self.transactions.get(username, {})
