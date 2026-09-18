# repositories/transaction_repository.py
from datetime import datetime
from decimal import Decimal
from bson.decimal128 import Decimal128
from db import accounts_collection as accounts_col, transactions_collection as txns_col, get_next_id
from models.transaction_entity import Transaction


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _to_txn(doc) -> Transaction:
    return Transaction(
        doc["txn_id"],
        doc["account_id"],
        doc["txn_type"],
        doc["amount"].to_decimal(),
        doc.get("created_at"),
    )


class TransactionRepository:

    def transfer(self, from_account_id: int, to_account_id: int, amount: Decimal) -> tuple[int, int]:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if from_account_id == to_account_id:
            raise ValueError("Cannot transfer to the same account")
        source = accounts_col.find_one({"_id": from_account_id}, {"balance": 1})
        if source is None:
            raise ValueError(f"Account {from_account_id} not found")
        target = accounts_col.find_one({"_id": to_account_id}, {"balance": 1})
        if target is None:
            raise ValueError(f"Account {to_account_id} not found")
        source_balance = source["balance"].to_decimal()
        if source_balance < amount:
            raise ValueError("Insufficient funds")
        accounts_col.update_one(
            {"_id": from_account_id},
            {"$set": {"balance": Decimal128(str(source_balance - amount))}},
        )
        accounts_col.update_one(
            {"_id": to_account_id},
            {"$set": {"balance": Decimal128(str(target["balance"].to_decimal() + amount))}},
        )
        created_at = _now()
        out_id = get_next_id("transactions")
        txns_col.insert_one({
            "_id": out_id, "txn_id": out_id, "account_id": from_account_id,
            "txn_type": "TRANSFEROUT", "amount": Decimal128(str(amount)),
            "created_at": created_at,
        })
        in_id = get_next_id("transactions")
        txns_col.insert_one({
            "_id": in_id, "txn_id": in_id, "account_id": to_account_id,
            "txn_type": "TRANSFERIN", "amount": Decimal128(str(amount)),
            "created_at": created_at,
        })
        return out_id, in_id


    def deposit(self, account_id: int, amount: Decimal) -> int:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        acct = accounts_col.find_one({"_id": account_id}, {"balance": 1})
        if acct is None:
            raise ValueError(f"Account {account_id} not found")
        new_balance = acct["balance"].to_decimal() + amount
        accounts_col.update_one(
            {"_id": account_id},
            {"$set": {"balance": Decimal128(str(new_balance))}},
        )
        txn_id = get_next_id("transactions")
        txns_col.insert_one({
            "_id": txn_id, "txn_id": txn_id, "account_id": account_id,
            "txn_type": "DEPOSIT", "amount": Decimal128(str(amount)),
            "created_at": _now(),
        })
        return txn_id

    def withdraw(self, account_id: int, amount: Decimal) -> int:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        acct = accounts_col.find_one({"_id": account_id}, {"balance": 1})
        if acct is None:
            raise ValueError(f"Account {account_id} not found")
        balance = acct["balance"].to_decimal()
        if balance < amount:
            raise ValueError("Insufficient funds")
        accounts_col.update_one(
            {"_id": account_id},
            {"$set": {"balance": Decimal128(str(balance - amount))}},
        )
        txn_id = get_next_id("transactions")
        txns_col.insert_one({
            "_id": txn_id, "txn_id": txn_id, "account_id": account_id,
            "txn_type": "WITHDRAW", "amount": Decimal128(str(amount)),
            "created_at": _now(),
        })
        return txn_id

    def find_by_id(self, txn_id: int) -> Transaction | None:
        doc = txns_col.find_one({"_id": txn_id})
        return _to_txn(doc) if doc else None

    def find_by_account(self, account_id: int) -> list[Transaction]:
        return [_to_txn(d) for d in
                txns_col.find({"account_id": account_id}).sort("_id", -1)]