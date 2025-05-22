from pysondb import db


class Account(object):
    def __init__(self, account_number, name_file_path, balance=0, is_teller=False):
    
        self.account_number = account_number
        self.name_file_path = name_file_path
        self.is_teller = False
        self.balance = balance

    @staticmethod
    def from_json(json_data):
        account_number = json_data.get("account_number")
        name_file_path = json_data.get("name_file_path")
        balance = json_data.get("balance", 0)
        is_teller = json_data.get("is_teller", False)
        return Account(account_number, name_file_path, balance, is_teller)

    def to_json(self):
        return {
            "account_number": self.account_number,
            "name_file_path": self.name_file_path,
            "balance": self.balance,
            "is_teller": self.is_teller
        }
    

class ATM(object):
    def __init__(self):
        self.db = db.getDb("bank/ATM.json")

    def get_account(self, account_number):
        account_json = self.db.getBy({"account_number": account_number})
        if account_json:
            return Account.from_json(account_json[0])
        else:
            print(f"Account {account_number} not found.")
            return None

    def update_account(self, account):
        existing_account = self.get_account(account.account_number)
        if existing_account:
            self.db.update({"account_number": account.account_number}, account.to_json())
            print(f"Account {account.account_number} updated.")
        else:
            print(f"Account {account.account_number} not found.")

    def create_account(self, account_number, name_file_path):
        new_account = Account(account_number, name_file_path)
        if self.db.getBy({"account_number": account_number}):
            print(f"Account {account_number} already exists.")
            return
        self.db.add(new_account.to_json())
        print(f"Account created: {new_account.to_json()}")

    def make_teller(self, account_number):
        account = self.get_account(account_number)
        if account:
            account.is_teller = True
            self.update_account(account)
            print(f"Account {account_number} set as teller.")
        else:
            print(f"Account {account_number} not found.")


    def deposit(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            account.balance += amount
            self.update_account(account)
            print(f"Deposited {amount} to account {account_number}. New balance: {account.balance}")
        else:
            print(f"Account {account_number} not found.")


    def withdraw(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            account.balance -= amount
            self.update_account(account)
            print(f"Withdrew {amount} from account {account_number}. New balance: {account.balance}")
        else:
            print(f"Account {account_number} not found.")

    def process_interest(self, interest_rate):
        accounts = self.db.getAll()
        for account_json in accounts:
            account = Account.from_json(account_json)
            account.balance += account.balance * interest_rate
            self.update_account(account)
            print(f"Applied interest to account {account.account_number}. New balance: {account.balance}")
        