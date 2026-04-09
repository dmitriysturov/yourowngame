"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-04-09
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "game_templates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_index(op.f("ix_game_templates_id"), "game_templates", ["id"], unique=False)

    op.create_table(
        "game_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("template_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.Enum("new", "in_progress", "finished", name="gamestatus"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("is_finished", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["template_id"], ["game_templates.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_game_sessions_id"), "game_sessions", ["id"], unique=False)

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("template_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["template_id"], ["game_templates.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_categories_id"), "categories", ["id"], unique=False)

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["game_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_teams_id"), "teams", ["id"], unique=False)

    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("has_media", sa.Boolean(), nullable=False),
        sa.Column("media_url", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_questions_id"), "questions", ["id"], unique=False)

    op.create_table(
        "game_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("winner_team_id", sa.Integer(), nullable=True),
        sa.Column("winner_score", sa.Integer(), nullable=True),
        sa.Column("final_scores", sa.JSON(), nullable=False),
        sa.Column("stats", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["game_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["winner_team_id"], ["teams.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_id"),
    )
    op.create_index(op.f("ix_game_results_id"), "game_results", ["id"], unique=False)

    op.create_table(
        "session_question_states",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("is_opened", sa.Boolean(), nullable=False),
        sa.Column("is_played", sa.Boolean(), nullable=False),
        sa.Column("answer_revealed", sa.Boolean(), nullable=False),
        sa.Column("selected_by_team_id", sa.Integer(), nullable=True),
        sa.Column("opened_at", sa.DateTime(), nullable=True),
        sa.Column("played_at", sa.DateTime(), nullable=True),
        sa.Column("answer_revealed_at", sa.DateTime(), nullable=True),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["selected_by_team_id"], ["teams.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["session_id"], ["game_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_id", "question_id", name="uq_session_question"),
    )
    op.create_index(op.f("ix_session_question_states_id"), "session_question_states", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_session_question_states_id"), table_name="session_question_states")
    op.drop_table("session_question_states")
    op.drop_index(op.f("ix_game_results_id"), table_name="game_results")
    op.drop_table("game_results")
    op.drop_index(op.f("ix_questions_id"), table_name="questions")
    op.drop_table("questions")
    op.drop_index(op.f("ix_teams_id"), table_name="teams")
    op.drop_table("teams")
    op.drop_index(op.f("ix_categories_id"), table_name="categories")
    op.drop_table("categories")
    op.drop_index(op.f("ix_game_sessions_id"), table_name="game_sessions")
    op.drop_table("game_sessions")
    op.drop_index(op.f("ix_game_templates_id"), table_name="game_templates")
    op.drop_table("game_templates")
