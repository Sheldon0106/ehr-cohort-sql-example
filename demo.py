"""Build the synthetic fixture in memory and print the visit-level cohort."""
from contextlib import closing
from pathlib import Path
import sqlite3


ROOT = Path(__file__).resolve().parent


def load_fixture(connection):
    connection.executescript((ROOT / "fixture.sql").read_text(encoding="utf-8"))


def cohort(connection):
    return connection.execute((ROOT / "cohort.sql").read_text(encoding="utf-8"))


def main():
    with closing(sqlite3.connect(":memory:")) as connection:
        load_fixture(connection)
        cursor = cohort(connection)
        header = [column[0] for column in cursor.description]
        rows = [header, *([str(value) for value in row] for row in cursor)]
    widths = [max(map(len, column)) for column in zip(*rows)]
    for row in rows:
        print("  ".join(value.ljust(width) for value, width in zip(row, widths)).rstrip())


if __name__ == "__main__":
    main()
