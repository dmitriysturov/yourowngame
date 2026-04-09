from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import GameStatus
from app.schemas.common import ORMModel


class TeamCreate(BaseModel):
    name: str = Field(min_length=1)
    display_order: int = Field(default=0, ge=0)


class TeamRead(ORMModel):
    id: int
    session_id: int
    name: str
    score: int
    display_order: int


class TeamScoreUpdate(BaseModel):
    delta: int = 0
    score: int | None = None


class GameSessionCreate(BaseModel):
    template_id: int
    teams: list[TeamCreate] = Field(default_factory=list)


class SessionQuestionStateRead(ORMModel):
    id: int
    question_id: int
    session_id: int
    is_opened: bool
    is_played: bool
    answer_revealed: bool
    selected_by_team_id: int | None
    opened_at: datetime | None
    played_at: datetime | None
    answer_revealed_at: datetime | None
    closed_at: datetime | None


class GameSessionRead(ORMModel):
    id: int
    template_id: int
    status: GameStatus
    created_at: datetime
    finished_at: datetime | None
    is_finished: bool
    teams: list[TeamRead]


class GameSessionDetail(GameSessionRead):
    question_states: list[SessionQuestionStateRead]


class QuestionActionPayload(BaseModel):
    selected_by_team_id: int | None = None


class GameResultRead(ORMModel):
    winner_team_id: int | None
    winner_score: int | None
    final_scores: dict
    stats: dict


class BoardQuestionState(ORMModel):
    question_id: int
    category_id: int
    value: int
    order: int
    is_opened: bool
    is_played: bool
    answer_revealed: bool


class BoardCategoryState(BaseModel):
    category_id: int
    title: str
    order: int
    questions: list[BoardQuestionState]


class BoardStateResponse(BaseModel):
    session_id: int
    status: GameStatus
    categories: list[BoardCategoryState]
