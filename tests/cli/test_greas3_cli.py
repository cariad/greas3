from typing import List, Type

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
                destination="s3://my-bucket/bar.txt",
                source="foo.txt",
            ),
        ),
        (
            ["foo.txt", "s3://my-bucket/bar.txt", "--dry-run"],
            Greas3Task,
            PathsArgs(
                destination="s3://my-bucket/bar.txt",
                dry_run=True,
                source="foo.txt",
            ),
        ),
        (
            ["foo.txt", "s3://my-bucket/bar.txt", "--debug"],
            Greas3Task,
            PathsArgs(
                debug=True,
                destination="s3://my-bucket/bar.txt",
                source="foo.txt",
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
