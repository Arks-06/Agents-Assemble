# Defines the structure for authentication tokens.

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"