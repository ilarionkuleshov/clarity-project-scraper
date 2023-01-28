"""add finances table

Revision ID: 597fbeef4f1c
Revises: 
Create Date: 2023-01-28 03:01:26.091416

"""
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import VARCHAR, FLOAT, DATE, BIGINT, TEXT, MEDIUMINT, TIMESTAMP

from alembic import op



# revision identifiers, used by Alembic.
revision = '597fbeef4f1c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "finances",
        Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        Column("edr", VARCHAR(100), unique=True, nullable=False),
        Column("url", VARCHAR(768), default=None, nullable=True),
        Column("row_1012_start", FLOAT(), default=None, nullable=True),
        Column("row_1012_end", FLOAT(), default=None, nullable=True),
        Column("row_1195_start", FLOAT(), default=None, nullable=True),
        Column("row_1195_end", FLOAT(), default=None, nullable=True),
        Column("row_1495_start", FLOAT(), default=None, nullable=True),
        Column("row_1495_end", FLOAT(), default=None, nullable=True),
        Column("row_1595_start", FLOAT(), default=None, nullable=True),
        Column("row_1595_end", FLOAT(), default=None, nullable=True),
        Column("row_1621_start", FLOAT(), default=None, nullable=True),
        Column("row_1621_end", FLOAT(), default=None, nullable=True),
        Column("row_1695_start", FLOAT(), default=None, nullable=True),
        Column("row_1695_end", FLOAT(), default=None, nullable=True),
        Column("row_1900_start", FLOAT(), default=None, nullable=True),
        Column("row_1900_end", FLOAT(), default=None, nullable=True),
        Column("row_2000_start", FLOAT(), default=None, nullable=True),
        Column("row_2000_end", FLOAT(), default=None, nullable=True),
        Column("row_2280_start", FLOAT(), default=None, nullable=True),
        Column("row_2280_end", FLOAT(), default=None, nullable=True),
        Column("row_2350_start", FLOAT(), default=None, nullable=True),
        Column("row_2350_end", FLOAT(), default=None, nullable=True),
        Column("exception", TEXT(), default=None, nullable=True, unique=False),
        Column(
            "status", MEDIUMINT(unsigned=True), index=True, unique=False,
            nullable=False, server_default=text("0")
        ),
        Column("created_at", TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
        Column(
            "updated_at", TIMESTAMP, nullable=False, index=True, unique=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP")
        ),
        Column("sent_to_customer", DATE(), default=None, nullable=True)
    )


def downgrade():
    op.drop_table("finances")
