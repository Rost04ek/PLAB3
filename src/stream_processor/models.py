from typing import NamedTuple

class TaskRecord(NamedTuple):
    task_id: int
    title: str
    description: str
    priority: str
    status: str