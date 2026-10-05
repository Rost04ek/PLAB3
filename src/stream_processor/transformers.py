from collections.abc import Iterable, Iterator
from stream_processor.models import TaskRecord

def to_short_representation(tasks: Iterable[TaskRecord]) -> Iterator[str]:
    """Перетворює об'єкт завдання на короткий текстовий рядок 'на льоту'."""
    for task in tasks:
        yield f"[{task.priority.upper()}] #{task.task_id} {task.title}"