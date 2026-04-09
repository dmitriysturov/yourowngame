from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class QuestionBase(BaseModel):
    text: str = Field(min_length=1)
    answer: str = Field(min_length=1)
    value: int = Field(gt=0)
    order: int = Field(ge=0, default=0)
    has_media: bool = False
    media_url: str | None = None


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    text: str | None = None
    answer: str | None = None
    value: int | None = Field(default=None, gt=0)
    order: int | None = Field(default=None, ge=0)
    has_media: bool | None = None
    media_url: str | None = None


class QuestionRead(ORMModel, QuestionBase):
    id: int
    category_id: int


class CategoryBase(BaseModel):
    title: str = Field(min_length=1)
    order: int = Field(default=0, ge=0)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: str | None = None
    order: int | None = Field(default=None, ge=0)


class CategoryRead(ORMModel, CategoryBase):
    id: int
    template_id: int
    questions: list[QuestionRead] = Field(default_factory=list)


class GameTemplateBase(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None


class GameTemplateCreate(GameTemplateBase):
    pass


class GameTemplateUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class GameTemplateRead(ORMModel, GameTemplateBase):
    id: int
    created_at: datetime


class GameTemplateDetail(GameTemplateRead):
    categories: list[CategoryRead] = Field(default_factory=list)
