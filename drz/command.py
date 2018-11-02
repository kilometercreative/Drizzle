import json
from functools import reduce

from .helper import path_to, contents_of
from .errors import DrizzleException


class Command:

    def __init__(self, func, name, docs, args=None, flags=None):
        self.func = func
        self.name = name
        self._docs = docs
        self._args = args or []
        self._flags = flags or []

    def parse_args(self, arguments):
        current_arg = None

        positional_args = []
        named_args = dict()
        flags = reduce(lambda acc, f: {**acc, f: False}, self._flags, {})

        for arg in arguments:
            if arg.startswith("--"):
                arg = arg[2:]
                if arg[2:] in self._args:
                    current_arg = arg[2:]
                else:
                    raise DrizzleException("Unknown argument '%s'" % arg)
            elif arg.startswith("-"):
                for fl in arg[1:]:
                    if fl in self._flags:
                        flags[fl] = True
                    else:
                        raise DrizzleException("Unknown flag '%s'" % arg)
            else:
                if current_arg:
                    named_args[current_arg] = arg
                else:
                    positional_args.append(arg)

        return {"pos": positional_args, "named": named_args, "flags": flags}

    def docs(self):
        return json.load(contents_of(path_to(self._docs, loc='docs')))
