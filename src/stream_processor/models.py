from typing import NamedTuple

class TaskRecord(NamedTuple):
    task_id: int
    title: str
    description: str
    priority: str
    status: str

class TaskIDIterator:
    """Власний ітератор (вимога методички)."""
    def __init__(self, start: int, stop: int):
        self.current = start
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value