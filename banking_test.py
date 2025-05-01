import unittest
from Banking import authenticate, accounts, deposit, withdraw, MAX_DEPOSIT_AMOUNT


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        # Reset account balances and transaction histories before each test
        accounts["12345"].update({
            "balance": 1000.0,
            "transactions": [],
            "failed_attempts": 0,
            "last_failed_time": None
        })
        accounts["67890"].update({
            "balance": 500.0,
            "transactions": [],
            "failed_attempts": 0,
            "last_failed_time": None
        })

    def test_successful_login(self):
        account = authenticate("12345", "1111")
        self.assertIsNotNone(account)

    def test_failed_login(self):
        for _ in range(4):  # 3 failed attempts should lock the account
            account = authenticate("12345", "9999")
            self.assertIsNone(account)

    def test_invalid_account(self):
        account = authenticate("00000", "1111")  # Invalid account number
        self.assertIsNone(account)

    def test_deposit_positive_amount_php(self):
        account = accounts["12345"]
        old_balance = account["balance"]
        new_balance = deposit(account, 200, "PHP")
        self.assertEqual(new_balance, old_balance + 200)

    def test_deposit_positive_amount_usd(self):
        account = accounts["12345"]
        old_balance = account["balance"]
        new_balance = deposit(account, 10, "USD")
        self.assertEqual(new_balance, old_balance + 500)

    def test_deposit_positive_amount_eur(self):
        account = accounts["12345"]
        old_balance = account["balance"]
        new_balance = deposit(account, 5, "EUR")
        self.assertEqual(new_balance, old_balance + 275)

    def test_deposit_exceeds_limit(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            deposit(account, MAX_DEPOSIT_AMOUNT + 1, "PHP")
        self.assertEqual(
            str(context.exception),
            f"Deposit amount exceeds the max limit of {MAX_DEPOSIT_AMOUNT} PHP."
        )

    def test_deposit_invalid_currency(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            deposit(account, 100, "AUD")
        self.assertEqual(str(context.exception), "Unsupported currency: AUD")

    def test_deposit_negative_amount(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            deposit(account, -50, "USD")
        self.assertEqual(
            str(context.exception),
            "Amount must be a positive number and not zero or negative."
        )

    def test_deposit_zero_amount(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            deposit(account, 0, "USD")
        self.assertEqual(
            str(context.exception),
            "Amount must be a positive number and not zero or negative."
        )

    def test_deposit_string_amount(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            deposit(account, "hundred", "USD")
        self.assertEqual(
            str(context.exception),
            "Amount must be a positive number and not zero or negative."
        )

    def test_withdraw_negative_amount(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            withdraw(account, -100)
        self.assertEqual(str(context.exception), "Amount must be positive.")

    def test_withdraw_zero_amount(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            withdraw(account, 0)
        self.assertEqual(str(context.exception), "Amount must be positive.")

    def test_withdraw_string_amount(self):
        account = accounts["12345"]
        with self.assertRaises(TypeErrorError) as context:
            withdraw(account, "fifty")
        self.assertEqual(str(context.exception), "Amount must be a number.")


if __name__ == "__main__":
    unittest.main()
