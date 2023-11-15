"""comments

Revision ID: 70b0d2960163
Revises: 317483585d07
Create Date: 2023-11-15 03:44:30.504227

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70b0d2960163'
down_revision: Union[str, None] = '317483585d07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment_association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('article_slug', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['article_slug'], ['articles.slug'], ),
    sa.PrimaryKeyConstraint('id', 'article_slug')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_association')
    # ### end Alembic commands ###
