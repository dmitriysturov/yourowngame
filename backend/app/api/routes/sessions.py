from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.session import get_session, list_sessions
from app.db.session import get_db
from app.models.enums import GameStatus
from app.schemas.common import MessageResponse
from app.schemas.session import (
    BoardStateResponse,
    GameResultRead,
    GameSessionCreate,
    GameSessionDetail,
    GameSessionRead,
    QuestionActionPayload,
    SessionQuestionStateRead,
    TeamRead,
    TeamScoreUpdate,
)
from app.services.game_service import GameService

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=GameSessionDetail, status_code=status.HTTP_201_CREATED)
def create_session(payload: GameSessionCreate, db: Session = Depends(get_db)) -> GameSessionDetail:
    return GameService.create_session(db, payload)


@router.get("", response_model=list[GameSessionRead])
def get_sessions(db: Session = Depends(get_db)) -> list[GameSessionRead]:
    return list_sessions(db)


@router.get("/{session_id}", response_model=GameSessionDetail)
def get_session_detail(session_id: int, db: Session = Depends(get_db)) -> GameSessionDetail:
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/{session_id}/start", response_model=GameSessionDetail)
def start_session(session_id: int, db: Session = Depends(get_db)) -> GameSessionDetail:
    return GameService.start_session(db, session_id)


@router.post("/{session_id}/finish", response_model=GameSessionDetail)
def finish_session(session_id: int, db: Session = Depends(get_db)) -> GameSessionDetail:
    return GameService.finish_session(db, session_id)


@router.post("/{session_id}/recreate", response_model=GameSessionDetail, status_code=status.HTTP_201_CREATED)
def recreate_session(session_id: int, db: Session = Depends(get_db)) -> GameSessionDetail:
    return GameService.recreate_session(db, session_id)


@router.get("/{session_id}/board", response_model=BoardStateResponse)
def board_state(session_id: int, db: Session = Depends(get_db)) -> BoardStateResponse:
    session, categories = GameService.board_state(db, session_id)
    return BoardStateResponse(session_id=session.id, status=session.status, categories=categories)


@router.post("/{session_id}/questions/{question_id}/open", response_model=SessionQuestionStateRead)
def open_question(
    session_id: int,
    question_id: int,
    payload: QuestionActionPayload,
    db: Session = Depends(get_db),
) -> SessionQuestionStateRead:
    return GameService.open_question(db, session_id, question_id, payload.selected_by_team_id)


@router.post("/{session_id}/questions/{question_id}/reveal-answer", response_model=SessionQuestionStateRead)
def reveal_answer(session_id: int, question_id: int, db: Session = Depends(get_db)) -> SessionQuestionStateRead:
    return GameService.reveal_answer(db, session_id, question_id)


@router.post("/{session_id}/questions/{question_id}/play", response_model=SessionQuestionStateRead)
def mark_played(session_id: int, question_id: int, db: Session = Depends(get_db)) -> SessionQuestionStateRead:
    return GameService.mark_played(db, session_id, question_id)


@router.post("/{session_id}/questions/{question_id}/close", response_model=SessionQuestionStateRead)
def close_question(session_id: int, question_id: int, db: Session = Depends(get_db)) -> SessionQuestionStateRead:
    return GameService.close_question(db, session_id, question_id)


@router.patch("/{session_id}/teams/{team_id}/score", response_model=TeamRead)
def update_score(
    session_id: int,
    team_id: int,
    payload: TeamScoreUpdate,
    db: Session = Depends(get_db),
) -> TeamRead:
    if payload.score is None and payload.delta == 0:
        raise HTTPException(status_code=400, detail="Provide either non-zero delta or explicit score")
    return GameService.update_team_score(db, session_id, team_id, delta=payload.delta, score=payload.score)


@router.get("/{session_id}/winner", response_model=GameResultRead)
def get_winner(session_id: int, db: Session = Depends(get_db)) -> GameResultRead:
    return GameService.get_winner(db, session_id)


@router.post("/{session_id}/reset", response_model=MessageResponse)
def reset_session(session_id: int, db: Session = Depends(get_db)) -> MessageResponse:
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    for team in session.teams:
        team.score = 0
    for state in session.question_states:
        state.is_opened = False
        state.is_played = False
        state.answer_revealed = False
        state.selected_by_team_id = None
        state.opened_at = None
        state.played_at = None
        state.answer_revealed_at = None
        state.closed_at = None
    session.status = GameStatus.new
    session.finished_at = None
    session.is_finished = False
    session.result = None
    db.commit()
    return MessageResponse(message="Session state has been reset")
