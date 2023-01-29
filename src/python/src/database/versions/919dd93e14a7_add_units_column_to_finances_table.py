"""add units column to finances table

Revision ID: 919dd93e14a7
Revises: 597fbeef4f1c
Create Date: 2023-01-29 19:14:25.357769

"""
import sqlalchemy as sa
from alembic import op



# revision identifiers, used by Alembic.
revision = '919dd93e14a7'
down_revision = '597fbeef4f1c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE finances ADD units VARCHAR(100) DEFAULT NULL AFTER url")


def downgrade():
    op.drop_column("finances", "units")
