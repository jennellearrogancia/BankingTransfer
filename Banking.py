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


def withdraw(account, amount):
    if not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number.")
    if amount <= 0:
        raise ValueError("Amount must be positive.")
    if account["balance"] >= amount:
        account["balance"] -= amount
        account["transactions"].append(f"Withdrew {amount:.2f}")
        return account["balance"]
    else:
        raise ValueError("Insufficient balance.")


def transfer(sender, receiver_account_number, amount):
    if not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number.")
    if amount <= 0:
        raise ValueError("Amount must be positive.")
    if sender["balance"] < amount:
        raise ValueError("Insufficient balance.")

    receiver = accounts.get(receiver_account_number)
    if not receiver:
        raise ValueError("Receiver account not found. Transfer canceled.")

    sender["balance"] -= amount
    receiver["balance"] += amount
    sender["transactions"].append(
        f"Transferred {amount:.2f} to {receiver_account_number}"
    )
    receiver["transactions"].append(f"Received {amount:.2f} from sender")


def view_transactions(account):
    return account["transactions"]


def main():
    print("Welcome to the Simple Banking System")
    acc_no = input("Enter your Account Number: ")
    pin = input("Enter your PIN: ")

    account = authenticate(acc_no, pin)
    if not account:
        print("Invalid credentials. Exiting...")
        sys.exit()

    while True:
        print("\n1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. View Transactions")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            print(f"Your balance is: {account['balance']:.2f}")
        elif choice == "2":
            amount = float(input("Enter amount to deposit: "))
            deposit(account, amount)
            print("Deposit successful.")
        elif choice == "3":
            try:
                amount_input = input("Enter amount to withdraw: ")
                amount = float(amount_input)
                withdraw(account, amount)
                print("Withdrawal successful.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "4":
            receiver = input("Enter receiver's account number: ")
            amount = float(input("Enter amount to transfer: "))
            try:
                transfer(account, receiver, amount)
                print("Transfer successful.")
            except ValueError as e:
                print(e)
        elif choice == "5":
            txns = view_transactions(account)
            if not txns:
                print("No transactions yet.")
            else:
                for txn in txns:
                    print("-", txn)
        elif choice == "6":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
