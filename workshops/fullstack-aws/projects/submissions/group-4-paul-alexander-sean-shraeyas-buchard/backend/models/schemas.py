# Schemas.py is utilized for formatting JSON responses and defining validation rules for API requests

# Pydantic is utilized within FastAPI so I will be using this
# BaseModel is the foundation for the data structure and validation
# Emailstr validated proper emails
# Field ensures proper constraints within fields
from pydantic import BaseModel, EmailStr, Field

# Using decimal in order to keep transactions precise (floats can have some odd interactions)
from decimal import Decimal

# User Schemas

# Validates incoming data when creating a user
class UserCreate(BaseModel):
    name: str = Field(min_length = 1)
    email: EmailStr
    password: str = Field(min_length = 1)

    model_config = {
      "json_schema_extra": {
          "example": {
              "name": "John Doe",
              "email": "john.doe@example.com",
              "password": "pass1234"
            }
        }
    }

# Formats the response returned after fetching or creating a user
class UserResponse(BaseModel):
    userId: int
    name: str
    email: str

    model_config = {
      "json_schema_extra": {
          "example": {
              "userId": 1,
              "name": "John Doe",
              "email": "john.doe@example.com",
            }
        }
    }
    
# Validates incoming data when logging in
class LoginRequest(BaseModel):
        email: EmailStr
        password: str = Field(min_length = 1)

        model_config = {
          "json_schema_extra": {
              "example": {
                  "email": "john.doe@example.com",
                  "password": "pass1234"
                }
            }
        }

# Bearer is an authentication scheme and we use it to authorize API requests
# It is also set as a default value for convenience in API responses
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "your_access_token_here",
                "token_type": "bearer",
            }
        }
    }

# Schraeyas contributed the TokenData schema for token payload validation
class TokenData(BaseModel):
    user_id: int
    role: str
    email: str | None = None

    model_config = {
      "json_schema_extra": {
          "example": {
              "user_id": 1,
              "role": "user",
              "email": "john.doe@example.com",
            }
        }
    }

# Account Schemas

# Validates incoming data when creating an account
class AccountCreate(BaseModel):
    userId: int
    accountType: str

    model_config = {
      "json_schema_extra": {
          "example": {
              "userId": 1,
              "accountType": "SAVINGS",
            }
        }
    }

# Formats the response returned after fetching an account
class AccountResponse(BaseModel):
    accountId: int
    userName: str
    balance: Decimal
    accountType: str

    model_config = {
      "json_schema_extra": {
          "example": {
              "accountId": 1,
              "userName": "John Doe",
              "balance": 250.00,
              "accountType": "SAVINGS",
            }
        }
    }

# Formats the response returned after creating an account
class AccountCreatedResponse(BaseModel):
    accountId: int
    accountType: str

    model_config = {
      "json_schema_extra": {
          "example": {
              "accountId": 1,
              "accountType": "SAVINGS",
            }
        }
    }

# Transaction Schemas

# Validates incoming data for operations such as withdrawals and deposits
class AmountPayload(BaseModel):
    # gt=0 means that the amount must be above 0
    amount: Decimal = Field(gt=0, description="Amount must be positive")

    model_config = {
      "json_schema_extra": {
          "example": {
              "amount": 100.50,
            }
        }
    }

# Formats response for showing an account's balance
class BalanceResponse(BaseModel):
    accountId: int
    balance: Decimal

    model_config = {
      "json_schema_extra": {
          "example": {
              "accountId": 1,
              "balance": 350.50,
            }
        }
    }

# Formats details for transaction history
class TransactionResponse(BaseModel):
    type: str
    amount: Decimal
    date: str

    model_config = {
      "json_schema_extra": {
          "example": {
              "type": "DEPOSIT",
              "amount": 100.50,
              "date": "2026-09-15 14:30:00",
            }
        }
    }

# Validates incoming data when transferring funds to another account
class TransferRequest(BaseModel):
    toAccountId: int
    # gt=0 means that the amount must be above 0
    amount: Decimal = Field(gt=0, description="Amount must be positive")

    model_config = {
      "json_schema_extra": {
          "example": {
              "toAccountId": 2,
              "amount": 50.00,
            }
        }
    }

# Formats the response after a successful transfer
class TransferResponse(BaseModel):
    message: str
    sourceAccountId: int
    sourceBalance: Decimal
    targetAccountId: int
    targetBalance: Decimal

    model_config = {
      "json_schema_extra": {
          "example": {
              "message": "Transfer successful",
              "sourceAccountId": 1,
              "sourceBalance": 200.50,
              "targetAccountId": 2,
              "targetBalance": 150
            }
        }
    }
