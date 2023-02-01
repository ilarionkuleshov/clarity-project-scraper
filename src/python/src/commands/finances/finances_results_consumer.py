from sqlalchemy import update

from rmq.commands import Consumer
from database.models import Finances


class FinancesResultsConsumer(Consumer):
    def __init__(self):
        super().__init__()
        self.queue_name = self.project_settings.get("FINANCES_RESULTS")

    def build_message_store_stmt(self, message_body):
        values = {k:v for k,v in message_body.items() if k not in ["id"]}
        return update(Finances).where(Finances.id == message_body["id"]).values(values)
