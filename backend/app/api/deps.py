# acts as security gatekeeper,
# contains the dependency functions that intercept incoming requests or WebSocket connections to validate JWT tokens and retrieve the authenticated user from PostgreSQL

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status, WebSocket, WebSocketException
from app.core.config import settings
from app.db.session import get_db
from app.models.core import User, RoleEnum

# tells FastAPI where frontend will send credentials to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """Intercepts the request, decodes the JWT, and fetches the user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    # Fetch the user from the database
    result = await session.execute(select(User).filter(User.id == int(user_id)))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Ensures the user is not just logged in, but has explicit Admin privileges."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

async def get_current_user_ws(
    websocket: WebSocket, 
    session: AsyncSession = Depends(get_db)
) -> User:
    """Authenticates a WebSocket connection."""
    
    token = websocket.headers.get("authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
    else:
        token = websocket.query_params.get("token")
        
    if not token:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Missing Token")
        
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid Token")
    except jwt.PyJWTError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid Token")
        
    result = await session.execute(select(User).filter(User.id == int(user_id)))
    user = result.scalars().first()
    
    if user is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="User not found")
        
    return user