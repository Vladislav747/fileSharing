"""fill table user_types

Revision ID: 912e58f15a73
Revises: 4e8b44fa7f10
Create Date: 2023-05-01 00:20:09.317319

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '912e58f15a73'
down_revision = '4e8b44fa7f10'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """INSERT INTO users_types (type_id, type_name)
           VALUES (1, 'Авторизован')
        """
    )
    op.execute(
        """INSERT INTO users_types (type_id, type_name)
           VALUES (2, 'Premium')
        """
    )


def downgrade():
    op.execute("""TRUNCATE TABLE public.users_types CASCADE""")
