# Using decimal in order to keep transactions precise (floats can have some odd interactions)
from decimal import Decimal

# Using datetime a timestamp for the account
from datetime import datetime

# Parent class to store account data and do deposits and withdrawal
class Account:

# init here to assign values
    def __init__(self, account_id: int, user_id: int, account_type: str, balance: Decimal, created_at: str | None = None):
        self.account_id = account_id
        self.user_id = user_id
        self.account_type = account_type
        self.balance = balance
        # Gets timestamp if given, creates one in a formatted fashion if not (Month-Day-Year Hour:Minute:Second)
        self.created_at = created_at or datetime.now().strftime("%m-%d-%Y %H:%M:%S")

# Deposits money to the account
    def deposit(self, amount: Decimal) -> Decimal:

        # Decimal value that must be positive according to business rules
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        return self.balance

# Withdraws money from the account
    def withdraw(self, amount: Decimal) -> Decimal:

        # Prevent negative withdrawals (giving yourself money)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        # Cannot withdraw more than current balance according to business rules
        if amount > self.balance:
            raise ValueError("Cannot withdraw more than balance")
        
        self.balance -= amount
        return self.balance

#Returns the current balance of the account
    def getBalance(self):
        return self.balance

# Child classes for future functionality and naming the accounts
class SavingsAccount(Account):
    def __init__(self, account_id: int, user_id: int, balance: Decimal, created_at: str | None = None):

        # Super init calls init constructor from the parent class so it can initalize with the given values
        super().__init__(account_id, user_id, "SAVINGS", balance, created_at)


class CheckingAccount(Account):
    def __init__(self, account_id: int, user_id: int, balance: Decimal, created_at: str | None = None):
    
        # Super init calls init constructor from the parent class so it can initalize with the given values
        super().__init__(account_id, user_id, "CHECKING", balance, created_at)
