"""Update models

Revision ID: 94d077477562
Revises: d40a0bb8bc43
Create Date: 2024-10-09 16:08:13.020255

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = '94d077477562'
down_revision: str | None = 'd40a0bb8bc43'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'project',
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('full_amount', sa.Integer(), nullable=False),
        sa.Column('invested_amount', sa.Integer(), nullable=False),
        sa.Column('create_date', sa.DateTime(), nullable=False),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.drop_table('charityproject')
    op.drop_column('donation', 'fully_invested')


def downgrade() -> None:
    op.add_column('donation', sa.Column('fully_invested', sa.BOOLEAN(), nullable=False))
    op.create_table(
        'charityproject',
        sa.Column('name', sa.VARCHAR(length=100), nullable=False),
        sa.Column('description', sa.VARCHAR(), nullable=False),
        sa.Column('full_amount', sa.INTEGER(), nullable=False),
        sa.Column('invested_amount', sa.INTEGER(), nullable=False),
        sa.Column('fully_invested', sa.BOOLEAN(), nullable=False),
        sa.Column('create_date', sa.DATETIME(), nullable=False),
        sa.Column('close_date', sa.DATETIME(), nullable=True),
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.drop_table('project')
