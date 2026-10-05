import sys
sys.path.append("src")

import tracemalloc
import time
import csv
from pathlib import Path
from itertools import islice

from stream_processor.pipeline import build_base_pipeline
from stream_processor.filters import filter_undone
from stream_processor.transformers import to_short_representation
from stream_processor.analytics import count_task_statuses, groupby_priority, batched_tasks

def eager_read_all(path: Path) -> list:
    """Eager processing: завантажує весь файл у пам'ять."""
    with path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

def measure_execution(func, *args):
    """Вимірює час виконання та пікове споживання пам'яті."""
    tracemalloc.start()
    start_time = time.perf_counter()
    
    result = func(*args)
    
    elapsed_time = time.perf_counter() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return result, elapsed_time, peak

def consume_lazy_pipeline(path: Path):
    """Споживає лінивий пайплайн для підрахунку статусів."""
    pipeline = build_base_pipeline(path)
    return count_task_statuses(pipeline)

def main():
    test_file = Path("data/tasks_100k.csv")
    
    if not test_file.exists():
        print(f"Файл {test_file} не знайдено! Запусти generate_data.py")
        return

    print(f"=== Аналіз файлу {test_file.name} ===\n")

    # 1. Демонстрація лінивих операцій (Варіант 14)
    print("--- Отримання перших 5 невиконаних завдань (islice) ---")
    pipeline = build_base_pipeline(test_file)
    undone = filter_undone(pipeline)
    short_repr = to_short_representation(undone)
    
    # Витягуємо рівно 5 елементів. Файл не читається до кінця!
    for task_str in islice(short_repr, 5):
        print(task_str)

    print("\n--- Демонстрація Batch Processing ---")
    pipeline_for_batch = build_base_pipeline(test_file)
    # Беремо тільки перший батч розміром 3 для прикладу
    for batch in islice(batched_tasks(pipeline_for_batch, 3), 1):
        print(f"Батч містить {len(batch)} записи: {[t.task_id for t in batch]}")

    print("\n--- Групування за пріоритетом (groupby) ---")
    pipeline_for_group = build_base_pipeline(test_file)
    # Для групування беремо лише 100 елементів (щоб не сортувати всі 100к у пам'яті)
    sample_tasks = list(islice(pipeline_for_group, 100))
    groups = groupby_priority(sample_tasks)
    print(f"Групи у вибірці 100 завдань: {groups}")

    # 2. Порівняння Eager vs Lazy
    print("\n=== Eager vs Lazy Experiment ===")
    
    print("Запуск Eager (завантаження всього CSV у пам'ять)...")
    eager_res, eager_time, eager_peak = measure_execution(eager_read_all, test_file)
    
    print("Запуск Lazy (потокове читання та підрахунок)...")
    lazy_res, lazy_time, lazy_peak = measure_execution(consume_lazy_pipeline, test_file)

    print(f"\nEager memory peak: {eager_peak / 1024 / 1024:.2f} MB")
    print(f"Lazy memory peak:  {lazy_peak / 1024 / 1024:.2f} MB")
    print(f"Eager time: {eager_time:.4f} sec")
    print(f"Lazy time:  {lazy_time:.4f} sec")
    print(f"Lazy memory is ~{eager_peak / lazy_peak:.0f}x more efficient!")

if __name__ == "__main__":
    main()