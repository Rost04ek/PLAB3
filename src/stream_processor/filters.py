from collections.abc import Iterable, Iterator
from stream_processor.models import TaskRecord

def validate_tasks(rows: Iterable[dict[str, str]]) -> Iterator[TaskRecord]:
    """Відкидає пошкодженні записи (validation) та віддає NamedTuple."""
    valid_priorities = {"Low", "Medium", "High", "Critical"}
    valid_statuses = {"Open", "In Progress", "Review", "Done"}

    for row in rows:
        try:
            task_id = int(row["task_id"])
            title = row["title"].strip()
            desc = row["description"].strip()
            priority = row["priority"].strip()
            status = row["status"].strip()
        except (ValueError, KeyError):
            continue  # Пропускаємо рядки з помилками парсингу

        if not title or priority not in valid_priorities or status not in valid_statuses:
            continue  # Пропускаємо невалідні значення

        yield TaskRecord(task_id, title, desc, priority, status)

def filter_undone(tasks: Iterable[TaskRecord]) -> Iterator[TaskRecord]:
    """Lazy-фільтр: пропускає лише невиконані завдання."""
    for task in tasks:
        if task.status != "Done":
            yield task