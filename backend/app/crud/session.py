from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import GameSession, SessionQuestionState, Team


def list_sessions(db: Session) -> list[GameSession]:
    stmt = (
        select(GameSession)
        .options(joinedload(GameSession.teams))
        .order_by(GameSession.created_at.desc())
    )
    return list(db.scalars(stmt).unique().all())


def get_session(db: Session, session_id: int) -> GameSession | None:
    stmt = (
        select(GameSession)
        .where(GameSession.id == session_id)
        .options(
            joinedload(GameSession.teams),
            joinedload(GameSession.question_states),
            joinedload(GameSession.template),
            joinedload(GameSession.result),
        )
    )
    return db.scalars(stmt).unique().first()


def get_state(db: Session, session_id: int, question_id: int) -> SessionQuestionState | None:
    stmt = select(SessionQuestionState).where(
        SessionQuestionState.session_id == session_id,
        SessionQuestionState.question_id == question_id,
    )
    return db.scalars(stmt).first()


def get_team(db: Session, team_id: int) -> Team | None:
    return db.get(Team, team_id)
