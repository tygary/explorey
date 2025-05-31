from pysondb import db
import random
import os

class Account(object):
    def __init__(self, account_number, name_file_path, balance=0, is_teller=False, is_board=False):
        self.account_number = account_number
        self.name_file_path = name_file_path
        self.is_teller = is_teller
        self.balance = balance
        self.is_board = is_board

    @staticmethod
    def from_json(json_data):
        account_number = json_data.get("account_number")
        name_file_path = json_data.get("name_file_path")
        balance = json_data.get("balance", 0)
        is_teller = json_data.get("is_teller", False)
        is_board = json_data.get("is_board", False) 
        return Account(account_number, name_file_path, balance, is_teller, is_board)

    def to_json(self):
        return {
            "account_number": self.account_number,
            "name_file_path": self.name_file_path,
            "balance": self.balance,
            "is_teller": self.is_teller,
            "is_board": self.is_board
        }
    
DEFAULT_NEW_ACCOUNT_BALANCE = 100
DEFAULT_WITHDRAWL_AMOUNT = 20


class ATM(object):
    def __init__(self):
        self.db = db.getDb("bank/ATM.json")
        self.starting_balance = DEFAULT_NEW_ACCOUNT_BALANCE
        self.withdrawl_amount = DEFAULT_WITHDRAWL_AMOUNT
        self.exchange_rate = 1.0  # Default exchange rate of 1 bean buck to 1 bean
        self.current_teller_account_number = None  # Store the currently signed-in teller

    def set_current_teller(self, account_number):
        self.current_teller_account_number = account_number

    def set_withdrawl_amount(self, amount):
        self.withdrawl_amount = amount

    def get_withdrawl_amount(self):
        return self.withdrawl_amount

    def set_starting_balance(self, amount):
        self.starting_balance = amount
    
    def set_exchange_rate(self, exchange_rate):
        """
        Sets the exchange rate for converting bean bucks to beans.
        """
        self.exchange_rate = exchange_rate

    def get_current_teller(self):
        if self.current_teller_account_number:
            return self.get_account(self.current_teller_account_number)
        return None
    
    def pay_teller_based_on_amount(self, amount):
        """
        Pays the current teller based on the amount deposited.
        The payment is 10% of the deposit amount plus a flat fee of 10 beans.
        """
        if self.current_teller_account_number:
            teller = self.get_account(self.current_teller_account_number)
            if teller:
                payment = int(0.1 * amount + 5)  
                teller.balance += payment
                self.update_account(teller)
                print(f"Paid {payment} beans to teller {teller.account_number}. New balance: {teller.balance}")
            else:
                print(f"Teller account {self.current_teller_account_number} not found.")
        else:
            print("No current teller set.")

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
        converted_amount = int(amount * self.exchange_rate)
        account = self.get_account(account_number)
        if account:
            account.balance += int(converted_amount)
            self.update_account(account)
            print(f"Deposited {amount} converted to {converted_amount} to account {account_number}. New balance: {account.balance}")
            self.pay_teller_based_on_amount(converted_amount)
            return (self.get_account(account_number), amount, converted_amount, self.exchange_rate)
        else:
            print(f"Account {account_number} not found.")
            return (None, 0, 0, self.exchange_rate)


    def withdraw(self, account_number):
        amount = self.withdrawl_amount
        converted_amount = int(amount * self.exchange_rate)
        account = self.get_account(account_number)
        if account:
            account.balance -= converted_amount
            self.update_account(account)
            print(f"Withdrew {amount} converted to {converted_amount} from account {account_number}. New balance: {account.balance}")
            self.pay_teller_based_on_amount(converted_amount // 2)
            return (self.get_account(account_number), amount, converted_amount, self.exchange_rate)
        else:
            print(f"Account {account_number} not found.")
            return (None, 0, 0, self.exchange_rate)
        
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
                self.pay_teller_based_on_amount(amount)
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
        self.pay_teller_based_on_amount(0)  
        for account_json in accounts:
            account = Account.from_json(account_json)
            if account.balance >= 0:
                account.balance += int(account.balance * (interest_rate))
            else:
                account.balance += int(account.balance * (debt_interest_rate))
            self.update_account(account)
            print(f"Applied interest to account {account.account_number}. New balance: {account.balance}")