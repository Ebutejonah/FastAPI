#A simple banking system
class Account:
    def __init__(self, account_number, account_type, balance, account_holder):
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.account_holder = account_holder

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        try:
            self.balance -= amount
        except self.balance < amount:
            raise ValueError("Amount to be withdrawn is more than balance")

    def get_balance(self):
        return self.balance
    
    def get_account_number(self):
        return self.account_number
    
    def get_account_type(self):
        return self.account_type
    
    def get_account_details(self):
        return f"{self.account_holder} with {self.account_number} of {self.account_type}. Balance is {self.balance}"
    

class Savings_Account(Account):
    def get_account_details(self):
        return f"{self.account_holder} with {self.account_number} of {self.account_type}. Balance is {self.balance}. This is a Student Account."
    

class Current_Account(Account):
    def get_account_details(self):
        return f"{self.account_holder} with {self.account_number} of {self.account_type}. Balance is {self.balance}. This is a Current Account."