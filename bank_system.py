from datetime import datetime
import json
import os
import uuid


class User:
    def __init__(self, user_id, full_name, phone, password):
        self.user_id = user_id
        self.full_name = full_name
        self.phone = phone
        self.password = password
        self.accounts = []

    def authenticate(self, password):
        return self.password == password

    def add_account(self, account):
        self.accounts.append(account.account_number)

    def get_accounts(self):
        return self.accounts


class BankAccount:
    def __init__(self, account_number, user_id, currency='USD', balance=0.0, transactions=None):
        self.account_number = account_number
        self.user_id = user_id
        self.balance = balance
        self.currency = currency
        self.transactions = transactions or []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(Transaction('deposit', amount, self.account_number).__dict__)

    def withdraw(self, amount):
        self.balance -= amount
        self.transactions.append(Transaction('withdraw', amount, self.account_number).__dict__)

    def transfer(self, to_account, amount):
        self.balance -= amount
        to_account.balance += amount
        t = Transaction('transfer', amount, self.account_number, to_account.account_number).__dict__
        self.transactions.append(t)
        to_account.transactions.append(t)

    def get_statement(self):
        return self.transactions


class Transaction:
    def __init__(self, type_, amount, from_account, to_account=None):
        self.transaction_id = str(uuid.uuid4())
        self.type = type_
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class BankSystem:
    def __init__(self, filename='bank_data.json'):
        self.users = {}
        self.accounts = {}
        self.filename = filename
        self.blocked_users = {}
        self.load_from_file()

    def register_user(self, name, phone, password):
        if phone in self.users:
            raise ValueError("User already exists.")
        user_id = len(self.users) + 1
        user = User(user_id, name, phone, password)
        self.users[phone] = user
        self.save_to_file()
        return user

    def login(self, phone, password):
        if self.blocked_users.get(phone, 0) >= 3:
            raise Exception("User is blocked after 3 failed attempts.")
        user = self.users.get(phone)
        if user and user.authenticate(password):
            self.blocked_users[phone] = 0
            return user
        else:
            self.blocked_users[phone] = self.blocked_users.get(phone, 0) + 1
            raise Exception("Incorrect credentials.")

    def create_account(self, user, currency='USD'):
        account_number = str(uuid.uuid4())[:8]
