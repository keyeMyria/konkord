from rq.worker import SimpleWorker
from django.db import transaction


class AtomicTransactionWorker(SimpleWorker):
    def main_work_horse(self, *args, **kwargs):
        raise NotImplementedError("Worker does not implement this method")

    def execute_job(self, *args, **kwargs):
        with transaction.atomic():
            sid = transaction.savepoint()
            task_res = super(
                AtomicTransactionWorker, self).execute_job(*args, **kwargs)
            if not task_res:
                transaction.savepoint_rollback(sid)
            return task_res
