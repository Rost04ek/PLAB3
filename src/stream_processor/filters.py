from collections.abc import Iterable, Iterator
from stream_processor.models import TaskRecord

def validate_tasks(rows: Iterable[dict[str, str]]) -> Iterator[TaskRecord]:
    """Validation stage: відкидає пошкоджені записи."""
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
            continue

        if not title or priority not in valid_priorities or status not in valid_statuses:
            continue

        yield TaskRecord(task_id, title, desc, priority, status)

def filter_by_status(tasks: Iterable[TaskRecord], target_status: str) -> Iterator[TaskRecord]:
    """Фільтрація за статусом."""
    for task in tasks:
        if task.status == target_status:
            yield task

def filter_by_priority(tasks: Iterable[TaskRecord], target_priority: str) -> Iterator[TaskRecord]:
    """Фільтрація за пріоритетом (вимога варіанту 14)."""
    for task in tasks:
        if task.priority == target_priority:
            yield task

def lazy_search(tasks: Iterable[TaskRecord], search_id: int = None, search_title: str = None) -> Iterator[TaskRecord]:
    """Lazy пошук завдань за ID або назвою з early termination."""
    for task in tasks:
        if search_id and task.task_id == search_id:
            yield task
            break  # Early termination: знайшли унікальний ID і припинили пошук
        elif search_title and search_title.lower() in task.title.lower():
            yield task