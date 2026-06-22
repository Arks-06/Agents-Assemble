# central registry for database schema

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Every database model created (User, Workspace) will inherit from this Base.
    This allows SQLAlchemy to track all tables in one central registry.
    """
    pass