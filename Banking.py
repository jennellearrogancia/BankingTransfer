import time
import sys


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


def main():
    print("Welcome to the Simple Banking System")
    acc_no = input("Enter your Account Number: ")
    pin = input("Enter your PIN: ")

    account = authenticate(acc_no, pin)

    if not account:
        print("Invalid credentials. Exiting...")
        sys.exit()


if __name__ == "__main__":
    main()
