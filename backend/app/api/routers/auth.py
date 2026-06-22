# handles user identity and database security,
# provides endpoints for registering new accounts with hashed passwords and logging in to generate the secure JWT access tokens for authentication

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from app.api.deps import SessionDep
from app.models.core import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.core.security import get_password_hash, verify_password, create_access_token

# creates a grouping for all auth-related routes
router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, session: SessionDep):
    """Creates a new user with a hashed password."""
    # if the email is already taken
    result = await session.execute(select(User).filter(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists in the system."
        )
    
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticates a user and returns a JWT access token."""
    result = await session.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()
    
    # the user doesn't exist or the password hash doesn't match
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.id, role=user.role.value)
    
    return Token(access_token=access_token)