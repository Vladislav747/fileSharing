"""add connections between messages and users

Revision ID: acd1d3c390d7
Revises: 64894401f9c2
Create Date: 2022-06-21 00:30:17.681018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acd1d3c390d7'
down_revision = '64894401f9c2'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""INSERT INTO chats_messages (chat_id, message_id)
                  VALUES (1, 1)
               """)

    op.execute("""INSERT INTO chats_messages (chat_id, message_id)
                  VALUES (2, 2)
               """)

    op.execute("""INSERT INTO users_messages (user_id, message_id)
                    VALUES (1, 1)
                 """)

    op.execute("""INSERT INTO users_messages (user_id, message_id)
                    VALUES (2, 2)
                 """)


def downgrade():
    pass
