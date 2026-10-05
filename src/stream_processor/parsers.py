import csv
from collections.abc import Iterable, Iterator

def parse_csv_rows(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    """Перетворює рядки CSV на словники (lazy parsing)."""
    reader = csv.DictReader(lines)
    yield from reader