import random
import math
import os

accounts = {
    "1529483": {
        "PIN": 2783,
        "balance": 12450,
        "transactions": [
            {'type': 'deposit', 'amount': 2060, 'time': '2023-03-27 08:13:06'},
            {'type': 'deposit', 'amount': 280, 'time': '2023-06-13 18:03:05'},
            {'type': 'deposit', 'amount': 3840, 'time': '2023-06-28 14:35:26'},
            {'type': 'deposit', 'amount': 165, 'time': '2023-08-24 23:19:06'},
            {'type': 'deposit', 'amount': 895, 'time': '2023-12-01 23:55:01'}
        ]
    },
    "1738920": {
        "PIN": 8194,
        "balance": 5870,
        "transactions": [
            {'type': 'deposit', 'amount': 2080, 'time': '2023-01-27 21:50:00'},
            {'type': 'withdraw', 'amount': 2175, 'time': '2023-06-14 09:46:09'},
            {'type': 'withdraw', 'amount': 1915, 'time': '2023-10-26 08:30:43'},
            {'type': 'deposit', 'amount': 1725, 'time': '2023-10-28 04:34:41'},
            {'type': 'withdraw', 'amount': 3535, 'time': '2023-12-11 19:51:44'}
        ]
    },
    "1624704": {
        "PIN": 7321,
        "balance": 20390,
        "transactions": [
            {'type': 'deposit', 'amount': 1080, 'time': '2023-02-16 04:17:15'},
            {'type': 'withdraw', 'amount': 1700, 'time': '2023-06-06 14:01:28'},
            {'type': 'deposit', 'amount': 2550, 'time': '2023-06-10 08:36:43'},
            {'type': 'deposit', 'amount': 565, 'time': '2023-06-13 06:26:13'},
            {'type': 'withdraw', 'amount': 2715, 'time': '2023-08-19 07:39:28'}
        ]
    }
}

atm_storage = {
    10: 20,
    20: 20,
    50: 20,
    100: 20,
    200: 20
}


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def inputList(cast=int):
    return [cast(x) for x in input("").split(" ") if x != ""]


def validate_amount(number):
    return number % 10 == 0


def add_deposit(amount, cash_input):
    account["balance"] += amount
    for k, v in zip(atm_storage.keys(), cash_input):
        atm_storage[k] += v


def deposit():
    clear()
    print("Deposit\n")
    while True:
        amount = None
        while True:
            amount = int(input("Enter Deposit Amount or (0) to return to Options: "))
            if amount == 0:
                clear()
                return
            elif validate_amount(amount):
                break
            else:
                clear()
                print("Deposit.\n\nInvalid Deposit Amount. Please Try Again...\n")

        print("\nPlease Enter Cash to Deposit,\n(Enter values for 10, 20, 50, 100, 200): ")
        while True:
            cash_input = inputList()
            s = sum(k * v for k, v in zip(atm_storage.keys(), cash_input))
            if s == amount:
                add_deposit(amount, cash_input)
                clear()
                print(f"Deposit successful.\nTransferred {amount} to account.\nCurrent Balance: {account['balance']}\n")
                i = input("Press Anything to Continue...")
                clear()
                return
            else:
                clear()
                print("Deposit.\nInput and Cash Mismatch. Please Try again.\n")
                break


def get_cash_comb(amount, max=5):
    list = sorted([k for k in atm_storage.keys() if atm_storage[k]], reverse=True)
    if not len(list):
        return []

    solutions = []
    s = [0]
    count = 1

    while len(s):

        fill = False
        x = [list[i] for i in s]
        while sum(x) <= amount:

            if count > atm_storage[list[s[-1]]]:
                break

            if sum(x) == amount:
                y = sorted(set(x), reverse=True)
                solutions.append({i: x.count(i) for i in y})

            if len(solutions) >= max:
                fill = True
                break

            s.append(s[-1])
            x = [list[i] for i in s]
            count += 1

        if fill:
            break

        while len(s) and s[-1] >= len(list) - 1:
            s.pop()

        if len(s):
            s[-1] += 1
            count = 1

    return solutions


def withdraw():
    clear()
    print("Withdraw.\n")
    amount = None
    while True:
        amount = int(input("Enter Withdraw Amount or (0) to return to Options: "))
        if amount == 0:
            clear()
            return
        elif validate_amount(amount):
            cash_output = get_cash_comb(amount)
            if len(cash_output):
                break
            else:
                clear()
                print("Withdraw.\n\nWithdraw Amount Unavailable. Please Try Again...\n")
        else:
            clear()
            print("Withdraw.\n\nInvalid Withdraw Amount. Please Try Again...\n")

    c = random.choice(cash_output)
    account['balance'] -= amount
    for key in c:
        atm_storage[key] -= c[key]

    clear()
    print(f"Withdraw successful.\nWithdrew {amount} from account.\nCurrent Balance: {account['balance']}\n")
    print(atm_storage)
    i = input("Press Anything to Continue...")
    clear()


def info():
    clear()
    print(f"Info.\n\nBalance: {account['balance']}")
    print("Transactions:\n")
    for t in transactions:
        print(f" {t['time']}\n {'Withdrew' if t['type'] == 'withdraw' else 'Deposited'} {t['amount']}\n")
    i = input("Press Anything to Continue...")
    clear()


# 1529483
# 2783
running = True
clear()
while True:
    print("Welcome to ATM. To Proceed,")
    while True:
        accountCardNo = input("Enter Card Number or (0) to Exit: ")
        if int(accountCardNo) == 0:
            running = False
            break

        account = accounts.get(accountCardNo, None)
        if account:
            password = account.get("PIN")
            balance = account.get("balance")
            transactions = account.get("transactions")
            clear()
            break
        else:
            clear()
            print("Card is Invalid. Please try again...")

    if not running:
        break

    loggedIn = False
    max = 3
    for counter in range(max + 1):
        pin = int(input("Enter Card PIN: "))
        if password == pin:
            clear()
            print("Login successful.")
            loggedIn = True
            break

        else:
            if counter < max:
                clear()
                print(f"PIN is Incorrect. Please try again ({max - counter} left)")

    if not loggedIn:
        clear()
        print(f"Login failed... Card is locked.\n")
        continue

    while True:

        print(f"Balance: {account['balance']}\n\nOptions:\n(1) Deposit\n(2) Withdraw\n(3) Info\n(4) End")
        option = int(input("Choose Option: "))
        if option == 1:
            deposit()
        elif option == 2:
            withdraw()
        elif option == 3:
            info()
        elif option == 4:
            clear()
            break

