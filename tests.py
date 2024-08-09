import unittest
from threading import Thread

from service_layer import AccountServiceImpl, StockServiceImpl
from domain_classes import BuyTransaction, SellTransaction


class TestTradeMaster(unittest.TestCase):

    def setUp(self):
        self.account_service = AccountServiceImpl()
        self.stock_service = StockServiceImpl()
        self.username = "tester"

    def test_create_account(self):
        self.account_service.create_account(self.username)
        user = self.stock_service.data_store.get_user(self.username)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.username)

    def test_buy_stock(self):
        self.account_service.create_account(self.username)
        self.stock_service.buy_stock(self.username, "SBI", 10)
        transactions = self.account_service.get_transaction_history(self.username)
        self.assertEqual(len(transactions["orders"]), 1)
        self.assertIsInstance(transactions["orders"][0], BuyTransaction)

    def test_concurrent_buy_sell_stock(self):
        self.account_service.create_account(self.username)
        threads = [
            Thread(target=self.stock_service.buy_stock, args=(self.username, "SBI", 10)),
            Thread(target=self.stock_service.sell_stock, args=(self.username, "SBI", 5))
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        transactions = self.account_service.get_transaction_history(self.username)
        self.assertEqual(len(transactions["orders"]), 3)
        self.assertIsInstance(transactions["orders"][1], BuyTransaction)
        self.assertIsInstance(transactions["orders"][2], SellTransaction)


if __name__ == '__main__':
    unittest.main()
