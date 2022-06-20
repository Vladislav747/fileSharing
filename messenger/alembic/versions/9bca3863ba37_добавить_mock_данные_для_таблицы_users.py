"""Добавить mock данные для таблицы users

Revision ID: 9bca3863ba37
Revises: 91f3829bf633
Create Date: 2022-06-20 15:28:39.417000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '9bca3863ba37'
down_revision = '91f3829bf633'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""INSERT INTO users (login, password, name)
       VALUES ('vladislavis', 'asdsadsad', 'vlad')
    """)

    op.execute("""INSERT INTO users (login, password, name)
           VALUES ('nikitios','aaaa', 'nikita')
        """)


def downgrade():
    op.execute("""DELETE FROM users WHERE  login = 'vladislavis'""")
    op.execute("""DELETE FROM users WHERE  login = 'nikitios'""")
