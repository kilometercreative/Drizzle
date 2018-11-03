import os
import json
from .errors import DrizzleException


def path_to(*file, loc=""):
    file = map(os.path.expanduser, file)

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
    src_data = contents_of(src)

    for original in replacements:
        src_data = src_data.replace(original, replacements[original])

    dst = open(dst, 'w')
    dst.write(src_data)
    dst.close()


# Not safe, will throw error if file_name isn't a valid path
def contents_of(path):
    f = open(path, 'r')
    contents = f.read()
    f.close()

    return contents


def zip_into(bundle, path, exclude, include=None):
    for root, dirs, files in os.walk(path):
        for file in files:
            if include:
                should_include = False
                # todo do it on paths and pass it down?
            else:
                should_include = True

            if should_include:
                for ex in exclude:
                    if _pattern_matcher(file, ex):
                        should_include = False
                        break

            if not should_include:
                continue

            bundle.write(os.path.relpath(os.path.join(root, file)))


def _pattern_matcher(filename, pattern):
    if not pattern:  # don't match the empty string
        return False

    def recursive(remaining, parts):
        if not parts:
            return True

        if parts[0]:
            return (not remaining.startswith(parts[0])) and recursive(remaining[len(parts[0]):], parts[1:])
        elif len(parts) == 1:
            return True
        elif not parts[1]:
            return recursive(remaining, parts[1:])
        else:
            if parts[1] in remaining:
                return recursive(remaining[remaining.index(parts[1])+len(parts[1]):], parts[2:])
            return False

    return recursive(filename, pattern.split('*'))


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

    return DrizzleWrapper(json.loads(contents_of(p_drizzle)))
