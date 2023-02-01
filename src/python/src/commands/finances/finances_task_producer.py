from sqlalchemy import select, update

from rmq.commands import Producer
from rmq.utils import TaskStatusCodes

from database.models import Finances


class FinancesTaskProducer(Producer):
    def __init__(self):
        super().__init__()
        self.task_queue_name = self.project_settings.get("FINANCES_TASKS")
        self.reply_to_queue_name = self.project_settings.get("FINANCES_REPLIES")

    def build_task_query_stmt(self, chunk_size):
        stmt = select([Finances.id, Finances.edr]).where(
            Finances.status == TaskStatusCodes.NOT_PROCESSED.value
        ).order_by(Finances.id.asc()).limit(chunk_size)
        return stmt

    def build_task_update_stmt(self, db_task, status):
        return (
            update(Finances)
            .where(Finances.id == db_task["id"])
            .values({"status": status})
        )
