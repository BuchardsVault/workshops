from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from mangum import Mangum

# Domain Entities
from models.account_entity import Account, CheckingAccount, SavingsAccount
from models.transaction_entity import Transaction
from models.user_entity import User

# Request / Response Schemas
from models.schemas import (
    AccountCreate,
    AccountResponse,
    AmountPayload,
    BalanceResponse,
    TokenData,
    TransactionResponse,
    TransferRequest,
    TransferResponse,
    UserCreate,
    UserResponse,
)

from repositories.account_repository import AccountRepository
from repositories.user_repository import UserRepository
from auth import (
    auth_router,
    get_current_user,
    hash_password,
    require_roles,
)
import services.transaction_service as transaction_service

app = FastAPI(title="Simple Bank Application API (Object-Oriented)")

# Mount login & auth endpoints from security.py (/api/auth/login)
app.include_router(auth_router)

user_repo = UserRepository()
account_repo = AccountRepository()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Verification Helper ---


def verify_account_owner(account_id: int, current_user_id: int) -> Account:
    account = account_repo.find_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this account",
        )
    return account


# --- User Registration Route ---


@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate):
    if user_repo.find_by_email(data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(data.password)
    user_id = user_repo.create(data.name, data.email, hashed_pw)
    return {"userId": user_id, "name": data.name, "email": data.email}


# --- Account Routes ---


@app.get("/api/accounts", response_model=List[AccountResponse])
def get_all_accounts(admin: TokenData = Depends(require_roles(["admin"]))):
    """Admin-only: Retrieve all bank accounts."""
    accounts = account_repo.find_all()
    result = []
    for acc in accounts:
        user = user_repo.find_by_id(acc.user_id)
        result.append({
            "accountId": acc.account_id,
            "userName": user.name if user else "Unknown",
            "balance": acc.balance,
            "accountType": acc.account_type,
        })
    return result


@app.get("/api/accounts/my-accounts", response_model=List[AccountResponse])
def get_my_accounts(current_user: TokenData = Depends(get_current_user)):
    """User-only: Retrieve accounts owned by the authenticated caller."""
    user = user_repo.find_by_id(current_user.user_id)
    accounts = account_repo.find_by_user(current_user.user_id)
    return [
        {
            "accountId": acc.account_id,
            "userName": user.name if user else "Unknown",
            "balance": acc.balance,
            "accountType": acc.account_type,
        }
        for acc in accounts
    ]


@app.post("/api/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(data: AccountCreate, current_user: TokenData = Depends(get_current_user)):
    if data.userId != current_user.user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create an account for another user",
        )

    user = user_repo.find_by_id(data.userId)
    if not user:
        raise HTTPException(status_code=404, detail="User ID does not exist")

    account_id = account_repo.create(
        user_id=data.userId,
        account_type=data.accountType.upper(),
        initial_balance=Decimal("0.00"),
    )
    created_account = account_repo.find_by_id(account_id)
    if not created_account:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve created account"
        )

    return {
        "accountId": created_account.account_id,
        "userName": user.name,
        "balance": created_account.balance,
        "accountType": created_account.account_type,
    }


@app.get("/api/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, current_user: TokenData = Depends(get_current_user)):
    account = verify_account_owner(account_id, current_user.user_id)
    user = user_repo.find_by_id(account.user_id)
    return {
        "accountId": account.account_id,
        "userName": user.name if user else "Unknown",
        "balance": account.balance,
        "accountType": account.account_type,
    }


# --- Transaction Routes ---


@app.post("/api/accounts/{account_id}/deposit", response_model=BalanceResponse)
def deposit(account_id: int, data: AmountPayload, current_user: TokenData = Depends(get_current_user)):
    verify_account_owner(account_id, current_user.user_id)
    try:
        transaction_service.deposit(account_id, data.amount)
        current_balance = transaction_service.balance_check(account_id)
    except ValueError as e:
        status_code = 404 if "not found" in str(e).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(e))

    return {"accountId": account_id, "balance": current_balance}


@app.post("/api/accounts/{account_id}/withdraw", response_model=BalanceResponse)
def withdraw(account_id: int, data: AmountPayload, current_user: TokenData = Depends(get_current_user)):
    verify_account_owner(account_id, current_user.user_id)
    try:
        transaction_service.withdraw(account_id, data.amount)
        current_balance = transaction_service.balance_check(account_id)
    except ValueError as e:
        status_code = 404 if "not found" in str(e).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(e))

    return {"accountId": account_id, "balance": current_balance}


@app.post("/api/accounts/{account_id}/transfer", response_model=TransferResponse)
def transfer(account_id: int, data: TransferRequest, current_user: TokenData = Depends(get_current_user)):
    verify_account_owner(account_id, current_user.user_id)
    try:
        transaction_service.transfer(account_id, data.toAccountId, data.amount)
        source_balance = transaction_service.balance_check(account_id)
        target_balance = transaction_service.balance_check(data.toAccountId)
    except ValueError as e:
        status_code = 404 if "not found" in str(e).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(e))

    return {
        "message": "Transfer successful",
        "sourceAccountId": account_id,
        "sourceBalance": source_balance,
        "targetAccountId": data.toAccountId,
        "targetBalance": target_balance,
    }


@app.get("/api/accounts/{account_id}/transactions", response_model=List[TransactionResponse])
def get_transactions(account_id: int, current_user: TokenData = Depends(get_current_user)):
    verify_account_owner(account_id, current_user.user_id)
    history = transaction_service.transaction_history(account_id)
    return [
        {"type": t.txn_type, "amount": t.amount, "date": t.created_at}
        for t in history
    ]
# Mount static assets (JS/CSS/images) from the dist folder
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")


# Catch-all: serve index.html for any client-side routes not matched by API
@app.get("/{full_path:path}")
def serve_spa(full_path: str):
  return FileResponse("frontend/dist/index.html")
    
handler = Mangum(app)