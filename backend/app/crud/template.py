from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Category, GameTemplate, Question
from app.schemas.template import (
    CategoryCreate,
    CategoryUpdate,
    GameTemplateCreate,
    GameTemplateUpdate,
    QuestionCreate,
    QuestionUpdate,
)


def create_template(db: Session, payload: GameTemplateCreate) -> GameTemplate:
    template = GameTemplate(**payload.model_dump())
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


def list_templates(db: Session) -> list[GameTemplate]:
    stmt = select(GameTemplate).order_by(GameTemplate.created_at.desc())
    return list(db.scalars(stmt).all())


def get_template(db: Session, template_id: int) -> GameTemplate | None:
    stmt = (
        select(GameTemplate)
        .where(GameTemplate.id == template_id)
        .options(joinedload(GameTemplate.categories).joinedload(Category.questions))
    )
    return db.scalars(stmt).unique().first()


def update_template(db: Session, template: GameTemplate, payload: GameTemplateUpdate) -> GameTemplate:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(template, field, value)
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


def delete_template(db: Session, template: GameTemplate) -> None:
    db.delete(template)
    db.commit()


def add_category(db: Session, template_id: int, payload: CategoryCreate) -> Category:
    category = Category(template_id=template_id, **payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category(db: Session, category_id: int) -> Category | None:
    stmt = select(Category).where(Category.id == category_id).options(joinedload(Category.questions))
    return db.scalars(stmt).unique().first()


def update_category(db: Session, category: Category, payload: CategoryUpdate) -> Category:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category: Category) -> None:
    db.delete(category)
    db.commit()


def add_question(db: Session, category_id: int, payload: QuestionCreate) -> Question:
    question = Question(category_id=category_id, **payload.model_dump())
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_question(db: Session, question_id: int) -> Question | None:
    return db.get(Question, question_id)


def update_question(db: Session, question: Question, payload: QuestionUpdate) -> Question:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(question, field, value)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def delete_question(db: Session, question: Question) -> None:
    db.delete(question)
    db.commit()
