import os
import json
from .errors import DrizzleException


def path_to(*file, loc=""):
    if not loc:
        return os.path.join(os.getcwd(), *file)
    else:
        return os.path.join(os.path.dirname(__file__), loc, *file)


def conflicting_exists(*paths):
    conflicts = [p for p in paths if os.path.exists(p)]
    if len(conflicts) > 0:
        print("Conflicting folder exists. "
              "Please delete or move the following folders:\n%s" %
              '\n'.join(map(lambda p: '\t%s' % p, conflicts)))
        return True
    return False


# Not safe, doesn't check if file exists--will overwrite
def write_replacing(src, dst, replacements):
    src = open(src, 'r')
    src_data = src.read()
    src.close()

    for original in replacements:
        src_data = src_data.replace(original, replacements[original])

    dst = open(dst, 'w')
    dst.write(src_data)
    dst.close()


class DrizzleWrapper:
    def __init__(self, contents):
        self._contents = contents

    def __getitem__(self, item):
        if item in self._contents:
            return self._contents[item]
        raise DrizzleException("Malformed drizzle.json, could not find property '%s'" % item)


def get_drizzle_json():
    p_drizzle = path_to("drizzle.json")

    if not os.path.exists(p_drizzle):
        raise DrizzleException("Couldn't find drizzle.json")

    drizzle_file = open(p_drizzle, 'r')
    contents = json.load(drizzle_file)
    drizzle_file.close()

    return DrizzleWrapper(contents)
