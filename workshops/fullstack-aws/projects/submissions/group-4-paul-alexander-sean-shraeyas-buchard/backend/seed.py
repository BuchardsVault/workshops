# seed.py
from decimal import Decimal
from db import init_db, users_collection as users_col, accounts_collection as accounts_col, transactions_collection as txns_col, db
from repositories.user_repository import UserRepository
from repositories.account_repository import AccountRepository
from repositories.transaction_repository import TransactionRepository

# Wipe everything, including the ID counters, for a truly clean slate
for col in (users_col, accounts_col, txns_col, db["counters"]):
    col.delete_many({})
init_db()

users, accts, txns = UserRepository(), AccountRepository(), TransactionRepository()

uid = users.create("Buchard Joseph", "buchard@example.com")
uid2 = users.create("Test Teammate", "teammate@example.com")
a1 = accts.create(uid, "CHECKING", Decimal("500.00"))
a2 = accts.create(uid, "SAVINGS", Decimal("1000.00"))
a3 = accts.create(uid2, "CHECKING", Decimal("250.00"))
txns.deposit(a1, Decimal("75.00"))
txns.withdraw(a1, Decimal("25.00"))

print(f"Seeded: {len(list(users_col.find()))} users, "
      f"{len(list(accounts_col.find()))} accounts, "
      f"{len(list(txns_col.find()))} transactions")