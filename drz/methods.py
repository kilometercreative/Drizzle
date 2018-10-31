import os
import json
from shutil import copyfile
from functools import reduce

from .helper import path_to, conflicting_exists, write_replacing


class Command:

    def __init__(self, func, name, docs):
        self.func = func
        self.name = name
        self._docs = docs

    def docs(self):
        return json.load(open(path_to(self._docs, loc='docs'), 'r'))


def drizzle_help(cmd):
    if cmd:
        print("Retrieving help for %s" % cmd)
    else:
        print("Commands: ")
        for C in COMMANDS:
            print("%s - %s" % (C.name, C.docs()['description']))


def setup():
    p_deploy = path_to(".deploy")
    p_lib = path_to("lib")
    p_shared = path_to("shared")

    if conflicting_exists(p_deploy, p_lib, p_shared):
        return

    os.makedirs(p_deploy)
    os.makedirs(p_lib)
    os.makedirs(p_shared)


def add(args):
    if len(args) != 1:
        return print("Usage: drz add <name>")

    name = args[0]
    p_fun = path_to(name)

    if conflicting_exists(p_fun):
        return

    os.makedirs(p_fun)
    write_replacing(
        path_to("config.json", loc="templates"),
        path_to(name, "config.json"),
        replacements={
            "$1": name
        }
    )


def deploy():
    print("DEPLOYING NOW!")


# Compile commands into dictionary
COMMANDS = [
    Command(drizzle_help, "help", "help.json"),
    Command(setup, "setup", "setup.json"),
    Command(add, "add", "add.json"),
    Command(deploy, "deploy", "deploy.json"),
]

COMMAND_MAP = reduce(lambda acc, c: {**acc, c.name: c}, COMMANDS, {})
