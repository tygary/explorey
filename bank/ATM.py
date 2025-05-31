from pysondb import db
import random
import os

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
    
DEFAULT_NEW_ACCOUNT_BALANCE = 100
DEFAULT_WITHDRAWL_AMOUNT = 20


class ATM(object):
    def __init__(self):
        self.db = db.getDb("bank/ATM.json")
        self.starting_balance = DEFAULT_NEW_ACCOUNT_BALANCE
        self.withdrawl_amount = DEFAULT_WITHDRAWL_AMOUNT
        self.current_teller_account_number = None  # Store the currently signed-in teller

    def set_current_teller(self, account_number):
        self.current_teller_account_number = account_number

    def get_current_teller(self):
        if self.current_teller_account_number:
            return self.get_account(self.current_teller_account_number)
        return None

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

    def create_account(self, name_file_path):
        account_number = random.randint(1, 65536)
        while self.db.getBy({"account_number": account_number}):
            account_number = random.randint(1, 65536)
        new_name_path = f"/home/admin/explorey/images/atm/{account_number}.jpg"
        os.rename(name_file_path, new_name_path)
        new_account = Account(account_number, name_file_path=new_name_path, balance=self.starting_balance)
        self.db.add(new_account.to_json())
        print(f"Account created: {new_account.to_json()}")
        
        return account_number

    def make_teller(self, account_number):
        account = self.get_account(account_number)
        if account:
            account.is_teller = True
            self.update_account(account)
            print(f"Account {account_number} set as teller.")
        else:
            print(f"Account {account_number} not found.")


    def deposit(self, account_number, amount: int):
        account = self.get_account(account_number)
        if account:
            account.balance += int(amount)
            self.update_account(account)
            print(f"Deposited {amount} to account {account_number}. New balance: {account.balance}")
            return self.get_account(account_number)
        else:
            print(f"Account {account_number} not found.")
            return None


    def withdraw(self, account_number):
        amount = self.withdrawl_amount
        account = self.get_account(account_number)
        if account:
            account.balance -= amount
            self.update_account(account)
            print(f"Withdrew {amount} from account {account_number}. New balance: {account.balance}")
            return (self.get_account(account_number), amount)
        else:
            print(f"Account {account_number} not found.")
            return (None, 0)
        
    def transfer(self, from_account_number, to_account_number, amount):
        from_account = self.get_account(from_account_number)
        to_account = self.get_account(to_account_number)
        
        if from_account and to_account:
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                self.update_account(from_account)
                self.update_account(to_account)
                print(f"Transferred {amount} from account {from_account_number} to account {to_account_number}.")
                return (self.get_account(from_account_number), self.get_account(to_account_number))
            else:
                 
                return (None, None)
        else:
            print(f"One or both accounts not found: {from_account_number}, {to_account_number}.")
            return (None, None)

    def get_top_accounts(self):
        """
        Returns the top 20 accounts with the highest balance.
        """
        accounts = [Account.from_json(acc) for acc in self.db.getAll()]
        return sorted([acc for acc in accounts if acc.balance > 0], key=lambda acc: acc.balance, reverse=True)[:20]

    def get_bankruptcy_roll(self):
        """
        Returns the top 20 accounts with the most debt (negative balance).
        """
        accounts = [Account.from_json(acc) for acc in self.db.getAll()]
        return sorted([acc for acc in accounts if acc.balance < 0], key=lambda acc: acc.balance)[:20]
    
    def get_sign_on_bonus(self):
        """
        Returns the current sign-on bonus for new accounts.
        """
        return self.starting_balance

    def apply_interest(self, interest_rate, debt_interest_rate):
        """
        Applies interest to all accounts based on their balance.
        Positive balances get the interest rate, negative balances get the debt interest rate.
        """
        accounts = self.db.getAll()
        for account_json in accounts:
            account = Account.from_json(account_json)
            if account.balance >= 0:
                account.balance += int(account.balance * (interest_rate))
            else:
                account.balance += int(account.balance * (debt_interest_rate))
            self.update_account(account)
            print(f"Applied interest to account {account.account_number}. New balance: {account.balance}")