from argparse import ArgumentParser

from cline import ArgumentParserCli, RegisteredTasks

from greas3.cli.greas3_task import Greas3Task


class Greas3Cli(ArgumentParserCli):
    def make_parser(self) -> ArgumentParser:
        parser = ArgumentParser()

        parser.add_argument(
            "source",
            help="source",
        )

        parser.add_argument(
            "destination",
            help="destination",
        )

        return parser

    def register_tasks(self) -> RegisteredTasks:
        return [
            Greas3Task,
        ]
