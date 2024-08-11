import unittest
from threading import Thread

from service_layer import AccountServiceImpl, StockServiceImpl
from domain_classes import BuyTransaction, SellTransaction, User


class TestTradeMaster(unittest.TestCase):

    def setUp(self):
        self.account_service = AccountServiceImpl()
        self.stock_service = StockServiceImpl()
        self.username = "tester4"
        self.email = "tester4@test.com"
        self.password = "1234"

    def test_create_account(self):
        self.account_service.create_account(self.username, self.password, self.email)
        user = self.stock_service.data_store.get_user(User(self.username))
        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.username)

    def test_buy_stock(self):
        self.stock_service.buy_stock(self.username, "AMZN", 10, "Buy")
        transactions = self.account_service.get_transaction_history(self.username)
        self.assertEqual(len(transactions), 1)
        self.assertIsInstance(transactions[0], BuyTransaction)
    #
    def test_concurrent_buy_sell_stock(self):
        self.account_service.create_account(self.username, self.password, self.email)
        threads = [
            Thread(target=self.stock_service.buy_stock, args=(self.username, "AMZN", 10, "Buy")),
            Thread(target=self.stock_service.sell_stock, args=(self.username, "AMZN", 5, "Sell"))
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        transactions = self.account_service.get_transaction_history(self.username)
        self.assertEqual(len(transactions), 3)
        self.assertIsInstance(transactions[1], BuyTransaction)
        self.assertIsInstance(transactions[2], SellTransaction)


if __name__ == '__main__':
    unittest.main()
