# test.py — full repository check (run: uv run stage2_check.py)
import os
from decimal import Decimal

# Fresh database every run: no UNIQUE-email collisions, no stale WITHDRAWAL rows
if os.path.exists("banking.db"):
    os.remove("banking.db")

from db import init_db
from repositories.user_repository import UserRepository
from repositories.account_repository import AccountRepository
from repositories.transaction_repository import TransactionRepository

init_db()
users = UserRepository()
accounts = AccountRepository()
txns = TransactionRepository()

# --- Users ---
uid = users.create("Stage2 Test", "stage2@example.com")
print("user:", users.find_by_id(uid).get_dict())
print("by email:", users.find_by_email("stage2@example.com").get_dict())

# --- Accounts ---
aid = accounts.create(uid, "SAVINGS", Decimal("75.50"))
a = accounts.find_by_id(aid)
print(f"account: id={a.account_id} type={a.account_type} balance={a.balance} ({type(a.balance).__name__})")
print("balance lookup:", accounts.get_balance(aid))
print("accounts for user:", [x.account_id for x in accounts.find_by_user(uid)])

# --- Transactions ---
txns.deposit(aid, Decimal("50.00"))
txns.withdraw(aid, Decimal("30.00"))
print("balance (expect 95.50):", accounts.get_balance(aid))

# Overdraft: must raise AND leave no trace
try:
    txns.withdraw(aid, Decimal("999.00"))
    print("BUG: overdraft allowed!")
except ValueError as e:
    print("overdraft rejected:", e)
print("balance still (expect 95.50):", accounts.get_balance(aid))

# History: expect exactly 2 rows, WITHDRAW newest-first, amounts as Decimal
history = txns.find_by_account(aid)
print(f"history ({len(history)} rows, expect 2):")
for t in history:
    print("  ", t.get_dict())