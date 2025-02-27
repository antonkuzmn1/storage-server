"""column name changed

Revision ID: f6ec87d31286
Revises: 5ce9c529bdb4
Create Date: 2025-02-20 01:17:26.422077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f6ec87d31286'
down_revision: Union[str, None] = '5ce9c529bdb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('user_id', sa.Integer(), nullable=False))
    op.drop_column('files', 'user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('user', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_column('files', 'user_id')
    # ### end Alembic commands ###
