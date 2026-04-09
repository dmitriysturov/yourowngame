from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import GameStatus


class GameSession(Base):
    __tablename__ = "game_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("game_templates.id", ondelete="RESTRICT"), nullable=False)
    status: Mapped[GameStatus] = mapped_column(SAEnum(GameStatus), default=GameStatus.new, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_finished: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    template: Mapped["GameTemplate"] = relationship()
    teams: Mapped[list["Team"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", order_by="Team.display_order"
    )
    question_states: Mapped[list["SessionQuestionState"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
    result: Mapped["GameResult | None"] = relationship(
        back_populates="session", cascade="all, delete-orphan", uselist=False
    )


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    session: Mapped[GameSession] = relationship(back_populates="teams")


class SessionQuestionState(Base):
    __tablename__ = "session_question_states"
    __table_args__ = (UniqueConstraint("session_id", "question_id", name="uq_session_question"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    is_opened: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_played: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    answer_revealed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    selected_by_team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    opened_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    played_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    answer_revealed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    session: Mapped[GameSession] = relationship(back_populates="question_states")
    question: Mapped["Question"] = relationship(back_populates="session_states")


class GameResult(Base):
    __tablename__ = "game_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    winner_team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    winner_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    final_scores: Mapped[dict] = mapped_column(JSON, default=dict)
    stats: Mapped[dict] = mapped_column(JSON, default=dict)

    session: Mapped[GameSession] = relationship(back_populates="result")
