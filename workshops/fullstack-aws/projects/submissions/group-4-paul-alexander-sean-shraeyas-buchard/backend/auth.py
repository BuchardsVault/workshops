# auth.py. Core authentication, password hashing, token management, 
# and role-based access control for the banking API.

from datetime import UTC, datetime, timedelta
import os
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from pydantic import BaseModel, EmailStr
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
from repositories.user_repository import UserRepository
from models.schemas import LoginRequest, TokenResponse, TokenData

# --- Configuration ---
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-bank-key-change-in-prod")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

password_hash = PasswordHash((Argon2Hasher(), BcryptHasher()))
http_bearer = HTTPBearer()
user_repo = UserRepository()

# Credit: Schraeyas for router prefix and endpoint scaffolding
auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# --- Cryptographic Helpers ---


def hash_password(password: str) -> str:
  return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str | None) -> bool:
  if not hashed_password:
    return False
  try:
    return password_hash.verify(plain_password, hashed_password)
  except Exception:
    return False


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
  to_encode = data.copy()
  expire = (
      datetime.now(UTC) + expires_delta
      if expires_delta
      else datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  )
  to_encode.setdefault("scope", "user")
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict | None:
  try:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
  except jwt.PyJWTError:
    return None


# --- FastAPI Dependency Guards ---


# Credit: Schraeyas for token payload validation pattern returning TokenData
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> TokenData:
    
  token = credentials.credentials
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )

  payload = verify_token(token)
  if not payload:
    raise credentials_exception

  sub = payload.get("sub")
  if sub is None:
    raise credentials_exception

  try:
    role = payload.get("role", "user")
    return TokenData(user_id=int(sub), role=role, email=payload.get("email"))
  except (ValueError, TypeError):
    raise credentials_exception


# Credit: Schraeyas for the require_roles dependency factory pattern
def require_roles(allowed_roles: List[str]):
  def role_checker(current_user: TokenData = Depends(get_current_user),) -> TokenData:
    if current_user.role not in allowed_roles:
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="Operation not permitted for current role",
      )
    return current_user

  return role_checker


# --- Authentication Routes ---

# Credit: Schraeyas for initial login route design (adapted for MongoDB UserRepository & Email)
@auth_router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = user_repo.find_by_email(data.email)

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={
            "sub": str(user.user_id),
            "role": getattr(user, "role", "user"),
            "email": user.email,
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}