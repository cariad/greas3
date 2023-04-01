from logging import Formatter, StreamHandler, root

from greas3.cli import Greas3Cli
from greas3.logging import logger


def entry() -> None:
    sh = StreamHandler()
    sh.setFormatter(Formatter("%(message)s"))
    root.addHandler(sh)
    logger.setLevel("INFO")

    Greas3Cli.invoke_and_exit()


if __name__ == "__main__":
    entry()
