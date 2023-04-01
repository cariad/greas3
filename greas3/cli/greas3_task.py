from pathlib import Path

from boto3.session import Session
from cline import CommandLineArguments, Task
from slash3 import S3Uri

from greas3.cli.paths_args import PathsArgs
from greas3.operations import put


class Greas3Task(Task[PathsArgs]):
    @classmethod
    def make_args(cls, args: CommandLineArguments) -> PathsArgs:
        return PathsArgs(
            source=args.get_string("source"),
            destination=args.get_string("destination"),
            session=Session(),
        )

    def invoke(self) -> int:
        source = Path(self.args.source)
        destination = S3Uri(self.args.destination)

        put(source, destination, session=self.args.session)

        return 0
