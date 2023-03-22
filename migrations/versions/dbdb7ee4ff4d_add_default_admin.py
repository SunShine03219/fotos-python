"""add default admin

Revision ID: dbdb7ee4ff4d
Revises: be7d7b145ac3
Create Date: 2023-03-22 10:51:51.801287

"""
from os import getenv

from alembic import op
from dotenv import load_dotenv

from utils.providers.hash_provider import generate_hash

# revision identifiers, used by Alembic.
revision = "dbdb7ee4ff4d"
down_revision = "be7d7b145ac3"
branch_labels = None
depends_on = None
load_dotenv()

name = getenv("NAME")
email = getenv("EMAIL")
password = getenv("PASSWORD")


def upgrade() -> None:
    op.execute(
        f"""
        INSERT INTO "user" (name, email, password, role)
        VALUES ('{name}', '{email}', '{generate_hash(password)}', 'admin')
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM "user" WHERE email = email;
        """
    )
