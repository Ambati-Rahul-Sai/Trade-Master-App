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
        print("2. Log in")
        print("3. View Available Stocks")
        print("4. Calculate Average Stock Value")
        print("5. Forgot Password")
        print("6. Exit")

    @staticmethod
    def display_login_menu():
        print("1. View Available Stocks")
        print("2. Place Buy Order")
        print("3. Place Sell Order")
        print("4. Calculate Average Stock Value")
        print("5. View Transaction History")
        print("6. Update Account")
        print("7. Delete Account")
        print("8. Log out")

    def get_available_stocks(self):
        stocks = self.stock_service.get_available_stocks()
        for stock in stocks:
            print(f"Stock: {stock.symbol:<10} Price: {stock.price:<10} Quantity: {stock.quantity:<10}")

    def calculate_average_stock_value(self):
        stock_symbol = input("Enter stock symbol: ")
        from_year = int(input("From year: "))
        to_year = int(input("To year: "))
        result = self.stock_service.calculate_average_stock_value(stock_symbol, from_year, to_year)
        if result:
            return [stock_symbol, from_year, to_year, result]
        # print("Invalid Data!")
        return []

    def handle_login_input(self, username):
        print(f"{username} logged in")
        while True:
            self.display_login_menu()
            option = int(input("Enter your choice: "))

            if option == 1:
                # View Available Stocks

                self.get_available_stocks()

            elif option == 2:
                # Place Buy Order

                stock_symbol = input("Enter stock symbol: ")
                quantity = int(input("Enter quantity: "))
                transaction_type = "Buy"
                self.stock_service.buy_stock(username, stock_symbol, quantity, transaction_type)

            elif option == 3:
                # Place Sell Order

                stock_symbol = input("Enter stock symbol: ")
                quantity = int(input("Enter quantity: "))
                transaction_type = "Sell"
                self.stock_service.sell_stock(username, stock_symbol, quantity, transaction_type)

            elif option == 4:
                # Calculate Average Stock Value

                details = self.calculate_average_stock_value()
                if details:
                    print(
                        f"Average Stock Value of {details[0]} from year {details[1]} to year {details[2]} is: {details[3]}")

            elif option == 5:
                # View Transaction History

                transactions = self.account_service.get_transaction_history(username)
                if transactions:
                    print("Your Transactions:\n")
                    for transaction in transactions:
                        t_type = "Bought" if transaction.transaction_type == "Buy" else "Sold"
                        print(
                            f"\t{t_type} {transaction.quantity} share(s) of {transaction.stock_symbol} on {transaction.date}")
                else:
                    print("You haven't done any transactions yet!")

            elif option == 6:
                # Update Account

                new_password = input("Enter new password: ")
                new_email = input("Enter new email: ")
                self.account_service.update_account(username, new_password, new_email)

            elif option == 7:
                # Delete Account

                self.account_service.delete_account(username)
                print(f"Deleted Account for {username}!")
                break

            elif option == 8:
                # Log out

                print("Logging out...")
                break

            else:
                print("Invalid choice! Please try again.")

    def handle_user_input(self):
        while True:
            self.display_menu()
            choice = int(input("Enter your choice: "))

            if choice == 1:
                # Create Account

                username = input("Enter username: ")
                if not username:
                    print("Username cannot be empty! Please try again.")
                    continue

                email = input("Enter email: ")
                if not email:
                    print("Email cannot be empty! Please try again.")
                    continue

                password = input("Enter password: ")
                if not password:
                    print("Password cannot be empty! Please try again")
                    continue

                done = self.account_service.create_account(username, password, email)
                if not done:
                    continue

                self.handle_login_input(username)

            elif choice == 2:
                # Log in

                username = input("Enter username: ")
                if not username:
                    print("Username cannot be empty! Please try again.")
                    continue

                password = input("Enter password: ")
                if not password:
                    print("Password cannot be empty! Please try again")
                    continue

                existing_user = self.account_service.get_user(username, password)
                if not existing_user:
                    print("Invalid Credentials! Please try again.")
                    continue

                self.handle_login_input(username)

            elif choice == 3:
                # View Available Stocks

                self.get_available_stocks()

            elif choice == 4:
                # Calculate Average Stock Value

                details = self.calculate_average_stock_value()
                if details:
                    print(
                        f"Average Stock Value of {details[0]} from year {details[1]} to year {details[2]} is: {details[3]}")

            elif choice == 5:
                # Forgot Password

                username = input("Enter username: ")

                existing_user = self.account_service.get_user(username)
                if not existing_user:
                    print("Username does not exist!")
                    continue

                new_password = input("Enter new password: ")
                self.account_service.update_account(username, new_password)

            elif choice == 6:
                print("Closing TradeMaster, See you again!")
                break

            else:
                print("Invalid choice! Please try again.")
