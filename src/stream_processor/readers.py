from pathlib import Path
from collections.abc import Iterator
from collections.abc import Iterable, Iterator


def read_lines(path: Path) -> Iterator[str]:
    """Генератор для потокового читання файлу рядок за рядком."""
    with path.open("r", encoding="utf-8") as file:
        # yield from делегує ітерацію самому об'єкту файлу
        yield from file

def clean_lines(lines: Iterable[str]) -> Iterator[str]:
    """Generator для очищення потоку (видалення порожніх рядків)."""
    for line in lines:
        cleaned = line.strip()
        if cleaned:
            yield cleaned