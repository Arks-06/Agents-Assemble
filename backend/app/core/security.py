# manages the cryptographic operations for the application,
# handles hashing user passwords using secure algorithms and generates the signed JWT tokens that serve as users' digital passports

from datetime import datetime, timedelta, timezone
from typing import Any, Union
import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a provided password matches the hashed version in the database."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Converts a plain text password into a secure, salted hash."""
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], role: str) -> str:
    """
    Generates the JWT. 
    'subject' is the user's ID. 'role' is either 'admin' or 'viewer'.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "exp": expire,  # Expiration time
        "sub": str(subject),  # The User ID
        "role": role  # Role-Based Access Control claim
    }

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt