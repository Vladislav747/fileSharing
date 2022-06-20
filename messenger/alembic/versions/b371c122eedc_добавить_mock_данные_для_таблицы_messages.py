"""Добавить mock данные для таблицы messages

Revision ID: b371c122eedc
Revises: 31d30e219413
Create Date: 2022-06-20 15:28:59.113943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b371c122eedc'
down_revision = '31d30e219413'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""INSERT INTO messages (message)
          VALUES ('Hello')
       """)

    op.execute("""INSERT INTO messages (message)
          VALUES ('Hello Man')
       """)


def downgrade():
    op.execute("""DELETE FROM chats WHERE message = 'Hello'""")
    op.execute("""DELETE FROM chats WHERE message = 'Hello Man'""")
