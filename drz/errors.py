def no_args():
    print("""usage: drz <command> [parameters]
To see help, run:

drz help
drz <command> help
""")


def unknown_command(command):
    no_args()
    print("error: unknown command '%s'" % command)
