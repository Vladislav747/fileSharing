"""add connections between chat and users

Revision ID: 64894401f9c2
Revises: b47bb5879972
Create Date: 2022-06-21 00:30:02.070965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64894401f9c2'
down_revision = 'b47bb5879972'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""INSERT INTO users_chats (user_id, chat_id)
                VALUES (1, 1)
             """)

    op.execute("""INSERT INTO users_chats (user_id, chat_id)
                VALUES (2, 2)
             """)




def downgrade():
    pass
