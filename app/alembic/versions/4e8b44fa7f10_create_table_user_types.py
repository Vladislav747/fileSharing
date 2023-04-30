"""create table user_types

Revision ID: 4e8b44fa7f10
Revises: ef4ff93a10b1
Create Date: 2023-04-30 23:55:34.471282

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4e8b44fa7f10'
down_revision = 'ef4ff93a10b1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users_types',
                    sa.Column('type_id', sa.Integer(), nullable=False),
                    sa.Column('type_name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('type_id')
                    )


def downgrade():
    op.drop_table('users_types')
