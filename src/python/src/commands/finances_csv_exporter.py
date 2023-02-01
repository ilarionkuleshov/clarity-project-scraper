from sqlalchemy import select, and_

from .base import BaseCSVExporter
from database.models import Finances


class FinancesCsvExporter(BaseCSVExporter):
    table = Finances
    excluded_statuses = [0, 1, 4]
    excluded_columns = [
        "exception", "status", "created_at", "updated_at", "sent_to_customer"
    ]
    filename_prefix = "export"

    def build_select_query_stmt(self, chunk_size):
        where_clause = and_(
            self.table.sent_to_customer == None,
            *[self.table.status != status for status in self.excluded_statuses]
        )
        if columns := self.specify_columns():
            return select(*columns).limit(chunk_size).where(where_clause)
        else:
            return select(self.table).limit(chunk_size).where(where_clause)
