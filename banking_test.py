import unittest
from Banking import (
    authenticate,
    accounts,
    deposit,
    withdraw,
    transfer,
    MAX_DEPOSIT_AMOUNT
)


class TestBankingSystem(unittest.TestCase):
    def setUp(self):
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

    # FOR AUTHENTICATION TESTS

    def test_successful_login_with_correct_pin(self):
        account = authenticate("12345", "1111")
        self.assertIsNotNone(
            account,
            "Account should authenticate successfully with correct PIN."
        )

    def test_failed_login_with_wrong_pin_four_times(self):
        for i in range(4):
            account = authenticate("12345", "9999")
            self.assertIsNone(
                account,
                f"Attempt {i+1}: Authentication should fail with wrong PIN."
            )

    def test_login_with_invalid_account_number(self):
        account = authenticate("00000", "1111")
        self.assertIsNone(
            account,
            "Invalid account number should not authenticate.")

    # FOR DEPOSIT TESTS

    def test_deposit_php_successful(self):
        account = accounts["12345"]
        old_balance = account["balance"]
        new_balance = deposit(account, 200, "PHP")
        self.assertEqual(
            new_balance,
            old_balance + 200,
            "PHP deposit should correctly increase the balance."
        )

    def test_deposit_usd_successful_conversion(self):
        account = accounts["12345"]
        old_balance = account["balance"]
        new_balance = deposit(account, 10, "USD")
        self.assertEqual(
            new_balance,
            old_balance + 500,
            "USD deposit should convert to PHP correctly."
        )

    def test_deposit_eur_successful_conversion(self):
        account = accounts["12345"]
        old_balance = account["balance"]
        new_balance = deposit(account, 5, "EUR")
        self.assertEqual(
            new_balance,
            old_balance + 275,
            "EUR deposit should convert to PHP correctly."
        )

    def test_deposit_exceeding_max_limit(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            deposit(account, MAX_DEPOSIT_AMOUNT + 1, "PHP")
        self.assertEqual(
            str(context.exception),
            (
                f"Deposit amount exceeds the max limit of "
                f"{MAX_DEPOSIT_AMOUNT} PHP."
            )
        )


    def test_deposit_with_unsupported_currency(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            deposit(account, 100, "AUD")
        self.assertEqual(
            str(context.exception),
            "Unsupported currency: AUD"
        )

    def test_deposit_with_negative_amount(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            deposit(account, -50, "USD")
        self.assertEqual(
            str(context.exception),
            "Amount must be a positive number and not zero or negative."
        )

    def test_deposit_with_zero_amount(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            deposit(account, 0, "USD")
        self.assertEqual(
            str(context.exception),
            "Amount must be a positive number and not zero or negative."
        )

    def test_deposit_with_non_numeric_amount(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            deposit(account, "hundred", "USD")
        self.assertEqual(
            str(context.exception),
            "Amount must be a positive number and not zero or negative."
        )

    # FOR TRANSACTIONS TEST

    def test_transaction_log_after_deposit(self):
        account = accounts["12345"]
        deposit(account, 150, "PHP")
        self.assertIn(
            "Deposited 150.00 PHP (converted to 150.00 PHP)",
            account["transactions"]
        )

    # FOR WITHDRAWAL TESTS

    def test_withdraw_success_and_transaction_log(self):
        account = accounts["12345"]
        withdraw(account, 100)
        self.assertIn("Withdrew 100.00", account["transactions"])

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

    def test_withdraw_non_numeric_amount(self):
        account = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            withdraw(account, "fifty")
        self.assertEqual(str(context.exception), "Amount must be a number.")

    def test_withdraw_overdraft_protection(self):
        account = accounts["67890"]
        with self.assertRaises(ValueError):
            withdraw(account, account["balance"] + 1)

    # FOR TRANSFER TESTS

    def test_successful_fund_transfer(self):
        sender = accounts["12345"]
        receiver = accounts["67890"]
        amount = 300.0
        old_sender = sender["balance"]
        old_receiver = receiver["balance"]

        transfer(sender, "67890", amount)

        self.assertEqual(sender["balance"], old_sender - amount)
        self.assertEqual(receiver["balance"], old_receiver + amount)
        self.assertIn("Transferred 300.00 to 67890", sender["transactions"])
        self.assertIn("Received 300.00 from sender", receiver["transactions"])

    def test_transfer_negative_amount(self):
        sender = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            transfer(sender, "67890", -50)
        self.assertEqual(str(context.exception), "Amount must be positive.")

    def test_transfer_zero_amount(self):
        sender = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            transfer(sender, "67890", 0)
        self.assertEqual(str(context.exception), "Amount must be positive.")

    def test_transfer_non_numeric_amount(self):
        sender = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            transfer(sender, "67890", "one hundred")
        self.assertEqual(str(context.exception), "Amount must be a number.")

    def test_transfer_insufficient_funds(self):
        sender = accounts["12345"]
        with self.assertRaises(ValueError) as context:
            transfer(sender, "67890", sender["balance"] + 100)
        self.assertEqual(str(context.exception), "Insufficient balance.")

    def test_transfer_to_non_existent_account(self):
        sender = accounts["12345"]
        old_balance = sender["balance"]
        with self.assertRaises(ValueError) as context:
            transfer(sender, "00000", 50)
        self.assertEqual(
            str(context.exception),
            "Receiver account not found. Transfer canceled."
        )
        self.assertEqual(
            sender["balance"],
            old_balance,
            "Balance should remain unchanged after failed transfer."
        )


if __name__ == "__main__":
    unittest.main()
