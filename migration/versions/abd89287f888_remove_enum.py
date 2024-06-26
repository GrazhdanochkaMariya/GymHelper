"""remove enum

Revision ID: abd89287f888
Revises: 546cd4dc1bb0
Create Date: 2024-04-16 14:41:24.606106

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'abd89287f888'
down_revision = '546cd4dc1bb0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'score_level',
               existing_type=postgresql.ENUM('USER_LIKED', 'TOP_CHART', 'USER_CREATED', 'ADMIN_CREATED', 'NEW_RELEASES', 'RECENTLY_PLAYED', 'EXCLUSIVE_RELEASES', 'RECOMMENDED', 'COLLECTIONS', name='typeenum'),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'score_level',
               existing_type=sa.String(),
               type_=postgresql.ENUM('USER_LIKED', 'TOP_CHART', 'USER_CREATED', 'ADMIN_CREATED', 'NEW_RELEASES', 'RECENTLY_PLAYED', 'EXCLUSIVE_RELEASES', 'RECOMMENDED', 'COLLECTIONS', name='typeenum'),
               existing_nullable=True)
    # ### end Alembic commands ###
