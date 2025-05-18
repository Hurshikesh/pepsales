from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, func
from app.database import metadata

User = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("name", String, nullable=False),
)

Notification = Table(
    "notifications",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("type", String, nullable=False),
    Column("content", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
)
