import sys

from .methods import COMMAND_MAP
from .errors import no_args, unknown_command


def entrypoint():
    if len(sys.argv) < 2:
        return no_args()

    command = sys.argv[1]
    if command in COMMAND_MAP:
        COMMAND_MAP[command].func(sys.argv[2:])
    else:
        unknown_command(command)
