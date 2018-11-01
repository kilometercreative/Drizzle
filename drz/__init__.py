import sys

from .methods import COMMAND_MAP
from .errors import DrizzleException, no_args, unknown_command, generic_error


def entrypoint():
    if len(sys.argv) < 2:
        return no_args()

    command = sys.argv[1]
    if command in COMMAND_MAP:
        try:
            COMMAND_MAP[command].func(**COMMAND_MAP[command].parse_args(sys.argv[2:]))
        except DrizzleException as er:
            generic_error(er.message)
    else:
        unknown_command(command)

