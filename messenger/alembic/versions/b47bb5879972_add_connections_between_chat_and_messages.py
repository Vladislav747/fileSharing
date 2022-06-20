"""add connections between chat and messages

Revision ID: b47bb5879972
Revises: b371c122eedc
Create Date: 2022-06-21 00:19:41.165372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b47bb5879972'
down_revision = 'b371c122eedc'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""INSERT INTO chats_messages (chat_id, message_id)
             VALUES (1, 1)
          """)

    op.execute("""INSERT INTO chats_messages (chat_id, message_id)
             VALUES (1, 2)
          """)


def downgrade():
    pass
