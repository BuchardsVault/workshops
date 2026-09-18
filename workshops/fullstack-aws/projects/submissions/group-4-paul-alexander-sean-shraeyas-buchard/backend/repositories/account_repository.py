# repositories/account_repository.py
from decimal import Decimal
from bson.decimal128 import Decimal128
from db import accounts_collection as accounts_col, get_next_id
from models.account_entity import Account


def _to_account(doc) -> Account:
    return Account(
        doc["account_id"],
        doc["user_id"],
        doc["account_type"],
        doc["balance"].to_decimal(),      # Decimal128 -> Decimal at the boundary
        doc.get("created_at"),
    )


class AccountRepository:

    def create(self, user_id: int, account_type: str,
               initial_balance: Decimal = Decimal("0.00")) -> int:
        account_id = get_next_id("accounts")
        accounts_col.insert_one({
            "_id": account_id,
            "account_id": account_id,
            "user_id": user_id,
            "account_type": account_type,
            "balance": Decimal128(str(initial_balance)),   # Decimal -> Decimal128
        })
        return account_id

    def find_by_id(self, account_id: int) -> Account | None:
        doc = accounts_col.find_one({"_id": account_id})
        return _to_account(doc) if doc else None

    def find_by_user(self, user_id: int) -> list[Account]:
        return [_to_account(d) for d in
                accounts_col.find({"user_id": user_id}).sort("_id", 1)]
        
    # Retrieves all accounts sorted by account_id ascending.
    def find_all(self) -> list[Account]:
        
        cursor = accounts_col.find().sort("_id", 1)
        return [_to_account(doc) for doc in accounts_col.find().sort("_id", 1)]

    def get_balance(self, account_id: int) -> Decimal | None:
        doc = accounts_col.find_one({"_id": account_id}, {"balance": 1})
        return doc["balance"].to_decimal() if doc else None