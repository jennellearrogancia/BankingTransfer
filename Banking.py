import sys
import time


accounts = {
    "12345": {
        "pin": "1111",
        "balance": 1000.0,
        "transactions": [],
        "failed_attempts": 0,
        "last_failed_time": None
    },
    "67890": {
        "pin": "2222",
        "balance": 500.0,
        "transactions": [],
        "failed_attempts": 0,
        "last_failed_time": None
    },
}


LOCKOUT_TIME = 3600
MAX_FAILED_ATTEMPTS = 3


def authenticate(account_number, pin):
    account = accounts.get(account_number)
    if not account:
        return None

    if account["failed_attempts"] >= MAX_FAILED_ATTEMPTS:
        current_time = time.time()
        time_since_last_failed = current_time - account["last_failed_time"]

        if time_since_last_failed < LOCKOUT_TIME:
            lockout_remaining = LOCKOUT_TIME - time_since_last_failed
            print(
                f"Account locked. Try again in {int(lockout_remaining)} seconds."
            )
            return None

        account["failed_attempts"] = 0

    if account["pin"] == pin:
        account["failed_attempts"] = 0
        return account
    else:
        account["failed_attempts"] += 1
        account["last_failed_time"] = time.time()
        return None


EXCHANGE_RATES = {
    "USD": 50,
    "EUR": 55,
    "GBP": 65,
}

MAX_DEPOSIT_AMOUNT = 50000


def deposit(account, amount, currency="PHP"):
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError(
            "Amount must be a positive number and not zero or negative."
        )

    if currency != "PHP":
        if currency not in EXCHANGE_RATES:
            raise ValueError(f"Unsupported currency: {currency}")
        amount_in_php = amount * EXCHANGE_RATES[currency]
    else:
        amount_in_php = amount

    if amount_in_php > MAX_DEPOSIT_AMOUNT:
        raise ValueError(
            f"Deposit amount exceeds the max limit of {MAX_DEPOSIT_AMOUNT} PHP."
        )

    account["balance"] += amount_in_php
    account["transactions"].append(
        f"Deposited {amount:.2f} {currency} "
        f"(converted to {amount_in_php:.2f} PHP)"
    )
    return account["balance"]
