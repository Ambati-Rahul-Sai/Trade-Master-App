from data_layer import DataStore
from service_layer import AccountServiceImpl, StockServiceImpl


class TradeMasterApp:

    def __init__(self):
        self.account_service = AccountServiceImpl()
        self.stock_service = StockServiceImpl()
        self.data_store = DataStore.get_instance()

    @staticmethod
    def display_menu():
        print("Welcome to TradeMaster!")
        print("1. Create Account")
        print("2. View Available Stocks")
        print("3. Place Buy Order")
        print("4. Place Sell Order")
        print("5. View Transaction History")
        print("6. Exit")

    def handle_user_input(self):
        while True:
            self.display_menu()
            choice = int(input("Enter your choice: "))

            if choice == 1:
                username = input("Enter username: ")
                user = self.data_store.get_user(username)
                if user:
                    print(f"Username {username} is already taken! Please try again with different username.")
                    continue
                self.account_service.create_account(username)
            elif choice == 2:
                stocks = self.stock_service.get_available_stocks()
                for stock in stocks:
                    print(f"Stock: {stock.symbol}, Price: {stock.price}")
            elif choice == 3:
                username = input("Enter username: ")
                user = self.data_store.get_user(username)
                if not user:
                    print("Invalid username! (If you're new here, create an account.)")
                    continue
                stock_symbol = input("Enter stock symbol: ")
                stock = self.data_store.get_stock(stock_symbol)
                if not stock:
                    print("Invalid stock symbol! Please try again.")
                    continue
                quantity = int(input("Enter quantity: "))
                self.stock_service.buy_stock(username, stock_symbol, quantity)
            elif choice == 4:
                username = input("Enter username: ")
                user = self.data_store.get_user(username)
                if not user:
                    print("Invalid username! (If you're new here, create an account.)")
                    continue
                stock_symbol = input("Enter stock symbol: ")
                stock = self.data_store.get_stock(stock_symbol)
                if not stock:
                    print("Invalid stock symbol! Please try again.")
                    continue
                quantity = int(input("Enter quantity: "))
                self.stock_service.sell_stock(username, stock_symbol, quantity)
            elif choice == 5:
                username = input("Enter username: ")
                user = self.data_store.get_user(username)
                if not user:
                    print("Invalid username! (If you're new here, create an account.)")
                    continue
                user_transactions = self.account_service.get_transaction_history(username)
                orders = user_transactions["orders"]
                stocks = user_transactions["stocks"]
                print("\nYour transactions:")
                for order in orders:
                    print(order)
                print("\nYour current list of stocks:")
                for stock_symbol, quantity in stocks.items():
                    print(f"\t{stock_symbol}:\t{quantity}")
            elif choice == 6:
                print("Closing TradeMaster, See you again!")
                break
            else:
                print("Invalid choice! Please try again.")
