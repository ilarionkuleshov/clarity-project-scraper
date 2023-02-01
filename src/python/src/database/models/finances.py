from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, FLOAT, DATE

from .base import Base
from .mixins import (
    MysqlPrimaryKeyMixin, MysqlExceptionMixin,
    MysqlStatusMixin, MysqlTimestampsMixin
)


class Finances(
    Base, MysqlPrimaryKeyMixin, MysqlExceptionMixin,
    MysqlStatusMixin, MysqlTimestampsMixin
):
    __tablename__ = "clarity_finances"

    edr = Column("edr", VARCHAR(100), unique=True, nullable=False)
    url = Column("url", VARCHAR(768), default=None, nullable=True)
    units = Column("units", VARCHAR(100), default=None, nullable=True)

    row_1012_start = Column("row_1012_start", FLOAT(), default=None, nullable=True)
    row_1012_end = Column("row_1012_end", FLOAT(), default=None, nullable=True)

    row_1195_start = Column("row_1195_start", FLOAT(), default=None, nullable=True)
    row_1195_end = Column("row_1195_end", FLOAT(), default=None, nullable=True)

    row_1495_start = Column("row_1495_start", FLOAT(), default=None, nullable=True)
    row_1495_end = Column("row_1495_end", FLOAT(), default=None, nullable=True)

    row_1595_start = Column("row_1595_start", FLOAT(), default=None, nullable=True)
    row_1595_end = Column("row_1595_end", FLOAT(), default=None, nullable=True)

    row_1621_start = Column("row_1621_start", FLOAT(), default=None, nullable=True)
    row_1621_end = Column("row_1621_end", FLOAT(), default=None, nullable=True)

    row_1695_start = Column("row_1695_start", FLOAT(), default=None, nullable=True)
    row_1695_end = Column("row_1695_end", FLOAT(), default=None, nullable=True)

    row_1900_start = Column("row_1900_start", FLOAT(), default=None, nullable=True)
    row_1900_end = Column("row_1900_end", FLOAT(), default=None, nullable=True)

    row_2000_start = Column("row_2000_start", FLOAT(), default=None, nullable=True)
    row_2000_end = Column("row_2000_end", FLOAT(), default=None, nullable=True)

    row_2280_start = Column("row_2280_start", FLOAT(), default=None, nullable=True)
    row_2280_end = Column("row_2280_end", FLOAT(), default=None, nullable=True)

    row_2350_start = Column("row_2350_start", FLOAT(), default=None, nullable=True)
    row_2350_end = Column("row_2350_end", FLOAT(), default=None, nullable=True)

    sent_to_customer = Column("sent_to_customer", DATE(), default=None, nullable=True)
