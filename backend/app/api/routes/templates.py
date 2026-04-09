from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import template as template_crud
from app.db.session import get_db
from app.schemas.common import MessageResponse
from app.schemas.template import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    GameTemplateCreate,
    GameTemplateDetail,
    GameTemplateRead,
    GameTemplateUpdate,
    QuestionCreate,
    QuestionRead,
    QuestionUpdate,
)

router = APIRouter(prefix="/templates", tags=["templates"])


@router.post("", response_model=GameTemplateRead, status_code=status.HTTP_201_CREATED)
def create_template(payload: GameTemplateCreate, db: Session = Depends(get_db)) -> GameTemplateRead:
    return template_crud.create_template(db, payload)


@router.get("", response_model=list[GameTemplateRead])
def list_templates(db: Session = Depends(get_db)) -> list[GameTemplateRead]:
    return template_crud.list_templates(db)


@router.get("/{template_id}", response_model=GameTemplateDetail)
def get_template(template_id: int, db: Session = Depends(get_db)) -> GameTemplateDetail:
    template = template_crud.get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.patch("/{template_id}", response_model=GameTemplateRead)
def update_template(
    template_id: int,
    payload: GameTemplateUpdate,
    db: Session = Depends(get_db),
) -> GameTemplateRead:
    template = template_crud.get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template_crud.update_template(db, template, payload)


@router.delete("/{template_id}", response_model=MessageResponse)
def delete_template(template_id: int, db: Session = Depends(get_db)) -> MessageResponse:
    template = template_crud.get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    template_crud.delete_template(db, template)
    return MessageResponse(message="Template deleted")


@router.post("/{template_id}/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def add_category(template_id: int, payload: CategoryCreate, db: Session = Depends(get_db)) -> CategoryRead:
    template = template_crud.get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template_crud.add_category(db, template_id, payload)


@router.patch("/categories/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)) -> CategoryRead:
    category = template_crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return template_crud.update_category(db, category, payload)


@router.delete("/categories/{category_id}", response_model=MessageResponse)
def delete_category(category_id: int, db: Session = Depends(get_db)) -> MessageResponse:
    category = template_crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    template_crud.delete_category(db, category)
    return MessageResponse(message="Category deleted")


@router.post("/categories/{category_id}/questions", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
def add_question(category_id: int, payload: QuestionCreate, db: Session = Depends(get_db)) -> QuestionRead:
    category = template_crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return template_crud.add_question(db, category_id, payload)


@router.patch("/questions/{question_id}", response_model=QuestionRead)
def update_question(question_id: int, payload: QuestionUpdate, db: Session = Depends(get_db)) -> QuestionRead:
    question = template_crud.get_question(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return template_crud.update_question(db, question, payload)


@router.delete("/questions/{question_id}", response_model=MessageResponse)
def delete_question(question_id: int, db: Session = Depends(get_db)) -> MessageResponse:
    question = template_crud.get_question(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    template_crud.delete_question(db, question)
    return MessageResponse(message="Question deleted")
