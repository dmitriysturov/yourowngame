from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.crud.session import get_session, get_state, get_team
from app.models import Category, GameResult, GameSession, GameStatus, Question, SessionQuestionState, Team
from app.schemas.session import BoardCategoryState, BoardQuestionState, GameSessionCreate


class GameService:
    @staticmethod
    def create_session(db: Session, payload: GameSessionCreate) -> GameSession:
        template_categories = list(
            db.scalars(
                select(Category)
                .where(Category.template_id == payload.template_id)
                .options(joinedload(Category.questions))
            )
            .unique()
            .all()
        )
        if not template_categories:
            raise HTTPException(status_code=404, detail="Template not found or has no categories")

        if not payload.teams:
            raise HTTPException(status_code=400, detail="At least one team is required")

        session = GameSession(template_id=payload.template_id)
        db.add(session)
        db.flush()

        for idx, team_payload in enumerate(payload.teams):
            db.add(Team(session_id=session.id, name=team_payload.name, display_order=team_payload.display_order or idx))

        for category in template_categories:
            for question in category.questions:
                db.add(SessionQuestionState(session_id=session.id, question_id=question.id))

        db.commit()
        db.refresh(session)
        return get_session(db, session.id)

    @staticmethod
    def start_session(db: Session, session_id: int) -> GameSession:
        session = get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        if session.status != GameStatus.new:
            raise HTTPException(status_code=409, detail="Only new sessions can be started")

        session.status = GameStatus.in_progress
        db.add(session)
        db.commit()
        return get_session(db, session_id)

    @staticmethod
    def finish_session(db: Session, session_id: int) -> GameSession:
        session = get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        if session.status != GameStatus.in_progress:
            raise HTTPException(status_code=409, detail="Only in-progress sessions can be finished")

        if any(not state.is_played for state in session.question_states):
            raise HTTPException(status_code=409, detail="Cannot finish game before all questions are played")

        session.status = GameStatus.finished
        session.is_finished = True
        session.finished_at = datetime.utcnow()

        winner = max(session.teams, key=lambda t: t.score, default=None)
        result = session.result or GameResult(session_id=session.id)
        result.winner_team_id = winner.id if winner else None
        result.winner_score = winner.score if winner else None
        result.final_scores = {team.name: team.score for team in session.teams}
        result.stats = {
            "played_questions": sum(1 for st in session.question_states if st.is_played),
            "total_questions": len(session.question_states),
        }

        db.add(session)
        db.add(result)
        db.commit()
        return get_session(db, session_id)

    @staticmethod
    def recreate_session(db: Session, session_id: int) -> GameSession:
        session = get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        payload = GameSessionCreate(
            template_id=session.template_id,
            teams=[{"name": team.name, "display_order": team.display_order} for team in session.teams],
        )
        return GameService.create_session(db, payload)

    @staticmethod
    def open_question(db: Session, session_id: int, question_id: int, selected_by_team_id: int | None) -> SessionQuestionState:
        session = get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        if session.status != GameStatus.in_progress:
            raise HTTPException(status_code=409, detail="Questions can be opened only when game is in progress")

        state = get_state(db, session_id, question_id)
        if not state:
            raise HTTPException(status_code=404, detail="Question state not found in this session")
        if state.is_played:
            raise HTTPException(status_code=409, detail="Question is already played")
        if state.is_opened:
            raise HTTPException(status_code=409, detail="Question is already opened")

        if any(st.is_opened for st in session.question_states):
            raise HTTPException(status_code=409, detail="Another question is currently opened")

        if selected_by_team_id is not None:
            team = get_team(db, selected_by_team_id)
            if not team or team.session_id != session_id:
                raise HTTPException(status_code=400, detail="Selected team does not belong to this session")

        state.is_opened = True
        state.selected_by_team_id = selected_by_team_id
        state.opened_at = datetime.utcnow()
        db.add(state)
        db.commit()
        db.refresh(state)
        return state

    @staticmethod
    def reveal_answer(db: Session, session_id: int, question_id: int) -> SessionQuestionState:
        state = get_state(db, session_id, question_id)
        if not state:
            raise HTTPException(status_code=404, detail="Question state not found in this session")
        if not state.is_opened:
            raise HTTPException(status_code=409, detail="Question must be opened before revealing answer")
        if state.answer_revealed:
            raise HTTPException(status_code=409, detail="Answer already revealed")

        state.answer_revealed = True
        state.answer_revealed_at = datetime.utcnow()
        db.add(state)
        db.commit()
        db.refresh(state)
        return state

    @staticmethod
    def mark_played(db: Session, session_id: int, question_id: int) -> SessionQuestionState:
        state = get_state(db, session_id, question_id)
        if not state:
            raise HTTPException(status_code=404, detail="Question state not found in this session")
        if not state.is_opened:
            raise HTTPException(status_code=409, detail="Question must be opened before marking as played")
        if state.is_played:
            raise HTTPException(status_code=409, detail="Question already marked as played")

        state.is_played = True
        state.played_at = datetime.utcnow()
        db.add(state)
        db.commit()
        db.refresh(state)
        return state

    @staticmethod
    def close_question(db: Session, session_id: int, question_id: int) -> SessionQuestionState:
        state = get_state(db, session_id, question_id)
        if not state:
            raise HTTPException(status_code=404, detail="Question state not found in this session")
        if not state.is_opened:
            raise HTTPException(status_code=409, detail="Question is not opened")

        if not state.is_played:
            state.is_played = True
            state.played_at = datetime.utcnow()

        state.is_opened = False
        state.closed_at = datetime.utcnow()
        db.add(state)
        db.commit()
        db.refresh(state)
        return state

    @staticmethod
    def update_team_score(db: Session, session_id: int, team_id: int, delta: int = 0, score: int | None = None) -> Team:
        session = get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        if session.status == GameStatus.finished:
            raise HTTPException(status_code=409, detail="Cannot modify score in finished session")

        team = get_team(db, team_id)
        if not team or team.session_id != session_id:
            raise HTTPException(status_code=404, detail="Team not found in this session")

        if score is not None:
            team.score = score
        else:
            team.score += delta

        db.add(team)
        db.commit()
        db.refresh(team)
        return team

    @staticmethod
    def board_state(db: Session, session_id: int) -> tuple[GameSession, list[BoardCategoryState]]:
        session = get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        template = db.scalar(
            select(GameSession)
            .where(GameSession.id == session_id)
            .options(
                joinedload(GameSession.template)
                .joinedload(Category.questions),
                joinedload(GameSession.question_states),
            )
        )
        if template is None:
            raise HTTPException(status_code=404, detail="Session not found")

        state_map = {st.question_id: st for st in template.question_states}
        categories: list[BoardCategoryState] = []
        for category in sorted(template.template.categories, key=lambda c: c.order):
            question_states: list[BoardQuestionState] = []
            for question in sorted(category.questions, key=lambda q: q.order):
                st = state_map[question.id]
                question_states.append(
                    BoardQuestionState(
                        question_id=question.id,
                        category_id=category.id,
                        value=question.value,
                        order=question.order,
                        is_opened=st.is_opened,
                        is_played=st.is_played,
                        answer_revealed=st.answer_revealed,
                    )
                )
            categories.append(
                BoardCategoryState(
                    category_id=category.id,
                    title=category.title,
                    order=category.order,
                    questions=question_states,
                )
            )

        return session, categories

    @staticmethod
    def get_winner(db: Session, session_id: int) -> GameResult:
        session = get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        if session.status != GameStatus.finished or not session.result:
            raise HTTPException(status_code=409, detail="Winner is available only for finished sessions")
        return session.result
