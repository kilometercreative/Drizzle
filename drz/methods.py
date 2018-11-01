import os
import boto3
from functools import reduce

from .command import Command
from .helper import path_to, conflicting_exists, write_replacing, get_drizzle_json


def drizzle_help(pos, named, flags):
    if pos[0]:
        print("Retrieving help for %s" % pos[0])
    else:
        print("Commands: ")
        for c in COMMANDS:
            print("%s - %s" % (c.name, c.docs()['description']))


def setup(pos, named, flags):
    p_deploy = path_to(".deploy")
    p_lib = path_to("lib")
    p_shared = path_to("shared")
    p_drizzle = path_to("drizzle.json")

    if conflicting_exists(p_deploy, p_lib, p_shared, p_drizzle):
        return

    os.makedirs(p_deploy)
    os.makedirs(p_lib)
    os.makedirs(p_shared)

    access = named.get("access")
    if not access:
        access = input("AWS Access Key ID: ")

    secret = named.get("secret")
    if not secret:
        secret = input("AWS Secret Access Key: ")

    write_replacing(path_to("drizzle.json", loc="templates"),
                    p_drizzle,
                    replacements={"$access": access, "$secret": secret})


def add(pos, named, flags):
    if len(pos) != 1:
        return print("Usage: drz add <name>")

    drizzle = get_drizzle_json()

    name = pos[0]
    role_name = '%s_drizzle' % name
    p_fun = path_to(name)

    if conflicting_exists(p_fun):
        return

    os.makedirs(p_fun)
    write_replacing(path_to("config.json", loc="templates"),
                    path_to(name, "config.json"),
                    replacements={"$1": name})
    write_replacing(path_to("starter.py", loc="templates"),
                    path_to(name, "__init__.py"),
                    replacements={"$1": name})

    iam = boto3.client('iam',
                       aws_access_key_id=drizzle["AWS Access Key"],
                       aws_secret_access_key=drizzle["AWS Secret Key"])
    iam.create_role(RoleName=role_name,
                    AssumeRolePolicyDocument=open(path_to("lambda_trust", loc="templates"), 'r').read())
    iam.put_role_policy(RoleName=role_name,
                        PolicyName='lambda_logs',
                        PolicyDocument=open(path_to("lambda_policy", loc="templates"), 'r').read())

    # boto3.client('lambda').create_function(
    # boto3.lambda.create_function()


def deploy():
    print("DEPLOYING NOW!")


# Compile commands into dictionary
COMMANDS = [
    Command(drizzle_help, "help", "help.json"),
    Command(setup, "setup", "setup.json", args=["access", "secret"]),
    Command(add, "add", "add.json"),
    Command(deploy, "deploy", "deploy.json"),
]

COMMAND_MAP = reduce(lambda acc, c: {**acc, c.name: c}, COMMANDS, {})
