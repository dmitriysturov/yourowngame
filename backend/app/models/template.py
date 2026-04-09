from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class GameTemplate(Base):
    __tablename__ = "game_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    categories: Mapped[list["Category"]] = relationship(
        back_populates="template", cascade="all, delete-orphan", order_by="Category.order"
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("game_templates.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    template: Mapped[GameTemplate] = relationship(back_populates="categories")
    questions: Mapped[list["Question"]] = relationship(
        back_populates="category", cascade="all, delete-orphan", order_by="Question.order"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    has_media: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    media_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    category: Mapped[Category] = relationship(back_populates="questions")
    session_states: Mapped[list["SessionQuestionState"]] = relationship(back_populates="question")
