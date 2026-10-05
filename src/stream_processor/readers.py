from pathlib import Path
from collections.abc import Iterator

def read_lines(path: Path) -> Iterator[str]:
    """Генератор для потокового читання файлу рядок за рядком."""
    with path.open("r", encoding="utf-8") as file:
        # yield from делегує ітерацію самому об'єкту файлу
        yield from file