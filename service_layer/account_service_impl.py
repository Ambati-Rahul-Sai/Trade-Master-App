from data_layer import DataStore
from domain_classes import User
from service_layer.account_service import AccountService


class AccountServiceImpl(AccountService):
    def __init__(self):
        self.data_store = DataStore.get_instance()

    def create_account(self, username):
        self.data_store.add_user(User(username))
        print(f"Successfully created account for {username}!")

    def get_transaction_history(self, username):
        return self.data_store.get_transactions(username)
