from __future__ import annotations

import uuid
from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

from sqlalchemy import ARRAY, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

IST = ZoneInfo("Asia/Kolkata")


def ist_now() -> datetime:
    return datetime.now(IST)


def new_uuid() -> uuid.UUID:
    return uuid.uuid4()


class Base(DeclarativeBase):
    """Base for ORM Models."""


class Publication(Base):
    __tablename__ = "publications"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=new_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    feed_url: Mapped[str | None] = mapped_column(String, nullable=True)

    articles: Mapped[list["Article"]] = relationship(
        back_populates="publication",
        cascade="all, delete-orphan",
    )


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=new_uuid)
    canonical_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    publication_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("publications.id", ondelete="CASCADE"),
        nullable=False,
    )
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=ist_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=ist_now,
        onupdate=ist_now,
    )

    publication: Mapped["Publication"] = relationship(back_populates="articles")
    passages: Mapped[list["Passage"]] = relationship(
        back_populates="article",
        cascade="all, delete-orphan",
    )


class Passage(Base):
    __tablename__ = "passages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=new_uuid)
    article_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[List[float]] = mapped_column(ARRAY(Float), nullable=False)

    article: Mapped["Article"] = relationship(back_populates="passages")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=new_uuid)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=ist_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=ist_now,
        onupdate=ist_now,
    )

    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=new_uuid)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    retrieved_doc: Mapped[List[str] | None] = mapped_column(ARRAY(String), nullable=True)
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=ist_now)

    session: Mapped["ChatSession"] = relationship(back_populates="messages")