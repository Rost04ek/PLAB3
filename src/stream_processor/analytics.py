from collections.abc import Iterable, Iterator
from itertools import islice, groupby, filterfalse

def batched_tasks(tasks: Iterable, batch_size: int) -> Iterator[list]:
    """Batch processing за допомогою itertools.islice (Засіб 1)."""
    iterator = iter(tasks)
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            return
        yield batch

def groupby_priority(tasks: Iterable) -> dict:
    """Групування за пріоритетом за допомогою itertools.groupby (Засіб 2)."""
    sorted_tasks = sorted(tasks, key=lambda t: t.priority)
    result = {}
    for priority, group in groupby(sorted_tasks, key=lambda t: t.priority):
        result[priority] = len(list(group))
    return result

def get_undone_tasks_lazy(tasks: Iterable) -> Iterator:
    """Використання itertools.filterfalse (Засіб 3)."""
    return filterfalse(lambda t: t.status == "Done", tasks)

def count_task_statuses(tasks: Iterable) -> dict:
    """Підрахунок статусів із застосуванням generator expression."""
    counts = {"Done": 0, "Undone": 0}
    for task in tasks:
        if task.status == "Done":
            counts["Done"] += 1
        else:
            counts["Undone"] += 1
    return counts

def extract_titles_gen_expr(tasks: Iterable) -> Iterator[str]:
    """Обов'язкове використання generator expression за методичкою."""
    # Це generator expression (у дужках)
    return (task.title for task in tasks)