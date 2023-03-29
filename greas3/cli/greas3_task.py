from pathlib import Path

from boto3.session import Session
from cline import CommandLineArguments, Task

from greas3.cli.paths_args import PathsArgs
from greas3.operations import put
from greas3.s3 import unpack_s3_uri


class Greas3Task(Task[PathsArgs]):
    @classmethod
    def make_args(cls, args: CommandLineArguments) -> PathsArgs:
        return PathsArgs(
            source=args.get_string("source"),
            destination=args.get_string("destination"),
            session=Session(),
        )

    def invoke(self) -> int:
        unpacked_source = unpack_s3_uri(self.args.source)

        if unpacked_source is not None:
            self.out.write("Only local file uploads are supported")
            return 1

        unpacked_destination = unpack_s3_uri(self.args.destination)

        if unpacked_destination is None:
            self.out.write("Only uploads to S3 are supported")
            return 1

        source = Path(self.args.source)
        bucket_name = unpacked_destination[0]
        key = unpacked_destination[1]

        put(source, bucket_name, key, session=self.args.session)

        return 0
