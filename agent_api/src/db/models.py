from datetime import datetime

from typing import List
import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB

from sqlalchemy import ForeignKey, String, Integer, DateTime, func, Text, Float

class Base(DeclarativeBase):
    "Base for ORM Models"


class Publication(Base):
    __tablename__ = "publications"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=func.uuid_generate_v4())
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    feed_url: Mapped[str] = mapped_column(String, nullable=True)
    metadata: Mapped[dict] = mapped_column(JSONB, nullable=True)


class Article(Base):
    __tablename__ = "articles"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=func.uuid_generate_v4())
    canonical_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    publication_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable = False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())

    passages: Mapped[List[Passages]] = relationship(back_populates = "article")


class Passages(Base):
    __tablename__ = "passages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=func.uuid_generate_v4())
    article_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid = True), ForeignKey("articles.id"), nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[List[float]] = mapped_column(ARRAY(Float), nullable=False)

    article: Mapped[Article] = relationship(back_populates = "passages")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=func.uuid_generate_v4())
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())

    messages: Mapped[List[ChatMessage]] = relationship(back_populates="session")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=func.uuid_generate_v4())
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    retrieved_doc: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
    latency_ms: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())

    session: Mapped[ChatSession] = relationship(back_populates="messages")




