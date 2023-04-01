from os.path import sep
from pathlib import Path
from typing import List

from slash3 import S3Uri

from greas3.put_operation import PutOperation
from greas3.put_operations import PutOperations


def test_from_dir(data_dir: Path) -> None:
    uri = S3Uri("s3://stuff/")
    operations = PutOperations.from_dir(data_dir, uri)

    expect: List[PutOperation] = [
        PutOperation(
            data_dir / "lorum.txt",
            "lorum.txt",
            uri / "lorum.txt",
            "lorum.txt",
        ),
        PutOperation(
            data_dir / "movies" / "star-wars.txt",
            f"movies{sep}star-wars.txt",
            uri / "movies/star-wars.txt",
            "movies/star-wars.txt",
        ),
    ]

    assert operations.operations == expect


def test_from_file__uri_slash(lorum: Path) -> None:
    uri = S3Uri("s3://stuff/inbox/")
    operations = PutOperations.from_file(lorum, uri)

    expect: List[PutOperation] = [
        PutOperation(
            lorum,
            "lorum.txt",
            uri / "lorum.txt",
            "lorum.txt",
        ),
    ]

    assert operations.operations == expect
