"""Добавить mock данные для таблицы chats

Revision ID: 31d30e219413
Revises: 9bca3863ba37
Create Date: 2022-06-20 15:28:51.832732

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = '31d30e219413'
down_revision = '9bca3863ba37'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""INSERT INTO chats (name, type)
       VALUES ('First chat', 'public')
    """)

    op.execute("""INSERT INTO chats (name, type)
       VALUES ('Second chat', 'public')
    """)


def downgrade():
    op.execute("""DELETE FROM chats WHERE name = 'First chat'""")
    op.execute("""DELETE FROM chats WHERE name = 'Second chat'""")
