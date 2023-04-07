from io import StringIO
from pathlib import Path
from unittest.mock import patch

from cline import CommandLineArguments
from slash3 import S3Uri

from greas3.cli.greas3_task import Greas3Task
from greas3.cli.paths_args import PathsArgs


def test_make_args() -> None:
    cli_args = CommandLineArguments(
        {
            "source": "foo.txt",
            "destination": "s3://my-bucket/bar.txt",
        }
    )

    args = Greas3Task.make_args(cli_args)

    assert args == PathsArgs(
        destination="s3://my-bucket/bar.txt",
        source="foo.txt",
    )


def test_invoke() -> None:
    args = PathsArgs(
        debug=True,
        destination="s3://my-bucket/bar.txt",
        source="foo.txt",
    )

    out = StringIO()
    task = Greas3Task(args, out)

    with patch("greas3.cli.greas3_task.put") as put:
        exit_code = task.invoke()

    put.assert_called_once_with(
        Path("foo.txt"),
        S3Uri("s3://my-bucket/bar.txt"),
        dry_run=False,
        session=None,
    )

    assert exit_code == 0
    assert out.getvalue() == ""


def test_invoke__dry_run() -> None:
    args = PathsArgs(
        source="foo.txt",
        destination="s3://my-bucket/bar.txt",
        dry_run=True,
    )

    out = StringIO()
    task = Greas3Task(args, out)

    with patch("greas3.cli.greas3_task.put") as put:
        exit_code = task.invoke()

    put.assert_called_once_with(
        Path("foo.txt"),
        S3Uri("s3://my-bucket/bar.txt"),
        dry_run=True,
        session=None,
    )

    assert exit_code == 0
    assert out.getvalue() == ""
