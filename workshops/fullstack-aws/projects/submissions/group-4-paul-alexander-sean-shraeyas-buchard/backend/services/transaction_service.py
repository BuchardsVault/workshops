from repositories.account_repository import AccountRepository
account_repository = AccountRepository()
from repositories.transaction_repository import TransactionRepository
from decimal import Decimal

transaction_repository = TransactionRepository()
def transfer(from_account_id, to_account_id, amount: Decimal):
    return transaction_repository.transfer(from_account_id,to_account_id,amount)

#Checks if account is valid and returns accounts balance
def balance_check(account_id):
    #Recieving objects from repository
    account = account_repository.find_by_id(account_id)
    account = account_repository.find_by_id(account_id)
    #To check if the account exhist
    if account is None:
        raise ValueError("Account ID not found")
    return account.balance 

# Validates account and amount then will execute the deposit. Returns a string with a message
def deposit(account_id, amount):
    return transaction_repository.deposit(account_id, amount)
   

# Validates account and amount then will execute the withdraw. Returns a string with a message
def withdraw(account_id, amount):
    return transaction_repository.withdraw(account_id, amount)
    

#Should just recieve a list of a accounts transaction history
def transaction_history(account_id):
    return transaction_repository.find_by_account(account_id)
