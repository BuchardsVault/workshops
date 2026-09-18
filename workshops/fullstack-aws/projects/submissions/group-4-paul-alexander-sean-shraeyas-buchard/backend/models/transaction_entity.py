# Using datetime a timestamp for the account
from datetime import datetime
# Using decimal in order to keep transactions precise (floats can have some odd interactions)
from decimal import Decimal

# Transaction class to store transaction history and allowed it to be retrieved through a dictionary
class Transaction:
    def __init__(self, txn_id: int, account_id: int, txn_type: str, amount: Decimal, created_at: str | None = None):
        self.txn_id = txn_id
        self.account_id = account_id
        self.txn_type = txn_type
        self.amount = amount
        # Gets timestamp if given, creates one in a formatted fashion if not (Month-Day-Year Hour:Minute:Second)
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Only allow strings in valid_types to be used within txn_type and clarify with error
        valid_types = {"DEPOSIT", "WITHDRAW", "TRANSFERIN", "TRANSFEROUT"}
        if txn_type not in valid_types:
            raise ValueError(f"Invalid transaction type. Must be one of {valid_types}")

    def get_dict(self) -> dict:
        return {"txn_id": self.txn_id, "account_id": self.account_id, "txn_type": self.txn_type, "amount": self.amount, "created_at": self.created_at}
