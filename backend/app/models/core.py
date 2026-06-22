# foundational architecture of the application
# SQLAlchemy 2.0 syntax to model Users, Workspaces, and the relational mappings required for secure, multi-tenant workspace system

from typing import List, Optional
import enum
from sqlalchemy import String, ForeignKey, Table, Column, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class RoleEnum(str, enum.Enum):
    admin = "admin"
    viewer = "viewer"

class TaskStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

# ASSOCIATION TABLE: links Users and Workspaces together
user_workspace_table = Table(
    "user_workspace",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("workspace_id", ForeignKey("workspaces.id", ondelete="CASCADE"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.viewer)

    workspaces: Mapped[List["Workspace"]] = relationship(
        secondary=user_workspace_table, back_populates="users"
    )

class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    users: Mapped[List["User"]] = relationship(
        secondary=user_workspace_table, back_populates="workspaces"
    )
    tasks: Mapped[List["AgentTask"]] = relationship(
        back_populates="workspace", cascade="all, delete-orphan"
    )

class AgentTask(Base):
    __tablename__ = "agent_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"))
    agent_name: Mapped[str] = mapped_column(String)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.pending)
    
    # Postgres JSONB allows unstructured AI output to be saved cleanly
    result: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    workspace: Mapped["Workspace"] = relationship(back_populates="tasks")