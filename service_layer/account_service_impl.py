from data_layer import DataStore
from domain_classes import User
from service_layer.account_service import AccountService


class AccountServiceImpl(AccountService):
    def __init__(self):
        self.data_store = DataStore.get_instance()

    def get_user(self, username, password=''):
        username = username.strip()
        return self.data_store.get_user(User(username, password))

    def create_account(self, username, password, email):
        username = username.strip()
        valid_username = self.get_user(username)
        if valid_username:
            print("Username already exists!")
            return False
        else:
            self.data_store.add_user(User(username, password, email))
            print(f"Successfully created account for {username}!")
            return True

    def update_account(self, username, new_password='', new_email=''):
        username = username.strip()
        self.data_store.update_user(User(username, new_password, new_email))
        print(f"Successfully updated account for {username}")

    def delete_account(self, username):
        username = username.strip()
        self.data_store.delete_user(User(username))
        self.data_store.delete_transactions(User(username))
        print(f"Successfully deleted account for {username}")

    def get_transaction_history(self, username):
        username = username.strip()
        return self.data_store.get_transactions(User(username))
