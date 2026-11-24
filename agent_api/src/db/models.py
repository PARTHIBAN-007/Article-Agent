from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB

from sqlalchemy import String, Integer, DateTime, func

class Base(DeclarativeBase):
    "Base for ORM Models"

