from typing import List, Type
from unittest.mock import ANY

from cline import AnyTask
from pytest import mark

from greas3.cli import Greas3Cli
from greas3.cli.greas3_task import Greas3Task
from greas3.cli.paths_args import PathsArgs


@mark.parametrize(
    "args, expect_task, expect_args",
    [
        (
            ["foo.txt", "s3://my-bucket/bar.txt"],
            Greas3Task,
            PathsArgs(
                source="foo.txt",
                destination="s3://my-bucket/bar.txt",
                session=ANY,
            ),
        ),
    ],
)
def test(
    args: List[str],
    expect_task: Type[AnyTask],
    expect_args: PathsArgs,
) -> None:
    cli = Greas3Cli(args=args)
    assert isinstance(cli.task, expect_task)
    assert cli.task.args == expect_args
