from repositories import UserRepository, StockRepository, TransactionRepository, StockPriceHistoryRepository


class DataStore:
    instance = None

    @staticmethod
    def get_instance():
        if DataStore.instance is None:
            DataStore.instance = DataStore()
        return DataStore.instance

    def __init__(self):
        if DataStore.instance is not None:
            raise Exception("This class is a singleton!")
        self.user_repository = UserRepository()
        self.stock_repository = StockRepository()
        self.transaction_repository = TransactionRepository()
        self.stock_price_history_repository = StockPriceHistoryRepository()

    def add_user(self, user):
        self.user_repository.create_user(user)

    def get_user(self, user):
        return self.user_repository.get_user(user)

    def update_user(self, user):
        self.user_repository.update_user(user)

    def delete_user(self, user):
        self.user_repository.delete_user(user)

    def add_stock(self, stock):
        self.stock_repository.create_stock(stock)

    def get_stock(self, stock):
        return self.stock_repository.get_stock(stock)

    def get_stocks(self):
        return self.stock_repository.get_stocks()

    def update_stock(self, stock):
        self.stock_repository.update_stock(stock)

    def delete_stock(self, stock):
        self.stock_repository.delete_stock(stock)

    def total_stocks_bought(self, username, stock_symbol, transaction_type):
        return self.transaction_repository.total_stocks(username, stock_symbol, transaction_type)

    def total_stocks_sold(self, username, stock_symbol, transaction_type):
        return self.transaction_repository.total_stocks(username, stock_symbol, transaction_type)

    def calculate_average(self, stock_symbol, from_year, to_year):
        return self.stock_price_history_repository.get_average_stock_value(stock_symbol, from_year, to_year)

    def add_buy_transaction(self, transaction):
        self.transaction_repository.create_transaction(transaction)

    def add_sell_transaction(self, transaction):
        self.transaction_repository.create_transaction(transaction)

    def get_transactions(self, user):
        return self.transaction_repository.get_transactions_by_username(user)

    def delete_transactions(self, user):
        self.transaction_repository.delete_user_transactions(user)
