from pathlib import Path
from collections.abc import Iterator
from stream_processor.models import TaskRecord
from stream_processor.readers import read_lines
from stream_processor.parsers import parse_csv_rows
from stream_processor.filters import validate_tasks

def build_base_pipeline(path: Path) -> Iterator[TaskRecord]:
    """Будує базовий лінивий конвеєр (читання -> парсинг -> валідація)."""
    lines = read_lines(path)
    rows = parse_csv_rows(lines)
    valid_tasks = validate_tasks(rows)
    return valid_tasks