
class DrizzleException(Exception):

    def __init__(self, message):
        self.message = message


def no_args():
    print("""usage: drz <command> [parameters]
To see help, run:

drz help
drz <command> help
""")


def unknown_command(command):
    no_args()
    generic_error("unknown command '%s'" % command)


def generic_error(message):
    print("error: %s" % message)
