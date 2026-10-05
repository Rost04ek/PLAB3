from collections.abc import Iterable, Iterator
from itertools import islice, groupby

def batched_tasks(tasks: Iterable, batch_size: int) -> Iterator[list]:
    """Розбиває потік на батчі (batch processing)."""
    iterator = iter(tasks)
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            return
        yield batch

def count_task_statuses(tasks: Iterable) -> dict:
    """Підрахунок виконаних і невиконаних завдань потоково."""
    counts = {"Done": 0, "Undone": 0}
    for task in tasks:
        if task.status == "Done":
            counts["Done"] += 1
        else:
            counts["Undone"] += 1
    return counts

def groupby_priority(tasks: Iterable) -> dict:
    """Групування за пріоритетом (потребує попереднього сортування)."""
    # Сортуємо вхідні дані, оскільки itertools.groupby вимагає відсортованих даних
    sorted_tasks = sorted(tasks, key=lambda t: t.priority)
    result = {}
    for priority, group in groupby(sorted_tasks, key=lambda t: t.priority):
        result[priority] = len(list(group))
    return result