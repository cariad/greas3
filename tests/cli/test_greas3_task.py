from io import StringIO
from pathlib import Path
from unittest.mock import ANY, Mock, patch

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
        source="foo.txt",
        destination="s3://my-bucket/bar.txt",
        session=ANY,
    )


def test_invoke(session: Mock) -> None:
    args = PathsArgs(
        source="foo.txt",
        destination="s3://my-bucket/bar.txt",
        session=session,
    )

    out = StringIO()
    task = Greas3Task(args, out)

    with patch("greas3.cli.greas3_task.put") as put:
        exit_code = task.invoke()

    put.assert_called_once_with(
        Path("foo.txt"),
        S3Uri("s3://my-bucket/bar.txt"),
        session=session,
    )

    assert exit_code == 0
    assert out.getvalue() == ""
