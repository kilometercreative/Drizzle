import os
import json
from functools import reduce


class Command:

    def __init__(self, func, name, docs):
        self.func = func
        self.name = name
        self._docs = docs

    def docs(self):
        return json.load(open('%s/docs/%s' % (os.path.dirname(__file__), self._docs), 'r'))


def drizzle_help(cmd):
    if cmd:
        print("Retrieving help for %s" % cmd)
    else:
        print("Commands: ")
        for C in COMMANDS:
            print("%s - %s" % (C.name, C.docs()['description']))


def deploy():
    print("DEPLOYING NOW!")


# Compile commands into dictionary
COMMANDS = [
    Command(drizzle_help, "help", "help.json"),
    Command(deploy, "deploy", "deploy.json"),
]

COMMAND_MAP = reduce(lambda acc, c: {**acc, c.name: c}, COMMANDS, {})
