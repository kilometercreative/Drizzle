import os
import json
import zipfile
from functools import reduce

from .command import Command
from .aws import config_profile, aws
from .helper import DrizzleWrapper, path_to, conflicting_exists, write_replacing, contents_of, zip_into
from .errors import DrizzleException


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

    profile = named.get("profile")
    if not profile:
        profile = input("AWS Profile Name [default]: ") or "default"

    region = named.get("region")
    if not region:
        region = input("AWS Region [us-west-2]: ") or "us-west-2"

    config_profile(profile)

    write_replacing(path_to("drizzle.json", loc="templates"),
                    p_drizzle,
                    replacements={"$profile": profile,
                                  "$region": region})


def add(pos, named, flags):
    if len(pos) != 1:
        return print("Usage: drz add <name>")

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

    iam = aws('iam')
    role_arn = iam.create_role(RoleName=role_name,
                               AssumeRolePolicyDocument=contents_of(path_to("lambda_trust", loc="templates"))
                               )["Role"]["Arn"]
    iam.put_role_policy(RoleName=role_name,
                        PolicyName='lambda_logs',
                        PolicyDocument=contents_of(path_to("lambda_policy", loc="templates")))

    build([name])

    with open(path_to('.deploy/build/%s.zip' % name), 'rb') as bundle:
        aws('lambda').create_function(
            FunctionName=name,
            Runtime='python3.6',
            Role=role_arn,
            Handler='%s.lambda_handler' % name,
            Description='Created by drizzle',
            Code={'ZipFile': bundle.read()})


def build(pos=None, named=None, flags=None):
    # Able to run from:
    # - command line, within function (with or without pos[0] as name)
    # - project, supplying pos[0] as name of function
    # - another function

    # if drizzle function
    if len(pos) > 0:
        name = pos[0]
    else:
        name = os.path.basename(os.getcwd())
        os.chdir("..")

    p_config = path_to(name, "config.json")
    print(p_config)
    if not os.path.exists(p_config):
        raise DrizzleException("Couldn't find config.json for function '%s'" % name)
    config = DrizzleWrapper("config.json", p_config)

    # create build folder if it doesn't exist
    p_build = path_to('.deploy/build')
    if not os.path.exists(p_build):
        os.mkdir(p_build)

    # create build zip
    bundle = zipfile.ZipFile('.deploy/build/%s.zip' % name, 'w', zipfile.ZIP_DEFLATED)
    bundle.writestr("BUILD.md", contents_of(path_to("BUILD.md", loc="templates")))
    zip_into(bundle, path_to(name), config["exclude"])
    zip_into(bundle, path_to("shared"), config["exclude"])
    zip_into(bundle, path_to("lib"), config["exclude"], include=config["include"])
    bundle.close()


def deploy(pos, named, flags):
    print("DEPLOYING NOW!")


# Compile commands into dictionary
COMMANDS = [
    Command(drizzle_help, "help", "help.json"),
    Command(setup, "setup", "setup.json", args=["profile", "region"]),
    Command(add, "add", "add.json"),
    Command(build, "build", "add.json"),
    Command(deploy, "deploy", "deploy.json"),
]

COMMAND_MAP = reduce(lambda acc, c: {**acc, c.name: c}, COMMANDS, {})
