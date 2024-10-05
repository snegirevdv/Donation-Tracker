"""Initial

Revision ID: e361dc7a3eee
Revises:
Create Date: 2024-10-05 13:39:47.904953

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'e361dc7a3eee'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'charityproject',
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('desciption', sa.String(), nullable=False),
        sa.Column('full_amount', sa.Integer(), nullable=False),
        sa.Column('invested_amount', sa.Integer(), nullable=False),
        sa.Column('fully_invested', sa.Boolean(), nullable=False),
        sa.Column('create_data', sa.DateTime(), nullable=False),
        sa.Column('close_date', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'donation',
        sa.Column('comment', sa.String(), nullable=False),
        sa.Column('full_amount', sa.Integer(), nullable=False),
        sa.Column('invested_amount', sa.Integer(), nullable=False),
        sa.Column('fully_invested', sa.Boolean(), nullable=False),
        sa.Column('create_data', sa.DateTime(), nullable=False),
        sa.Column('close_date', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('donation')
    op.drop_table('charityproject')
