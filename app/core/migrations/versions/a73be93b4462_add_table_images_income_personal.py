"""add table images income personal

Revision ID: a73be93b4462
Revises: 7ddfce2b31a8
Create Date: 2024-09-16 01:26:29.908277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = 'a73be93b4462'
down_revision: Union[str, None] = '7ddfce2b31a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images_income_personal',
    sa.Column('images', sa.LargeBinary(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('income_id', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['income_id'], ['income_personal.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images_income_personal')
    # ### end Alembic commands ###
