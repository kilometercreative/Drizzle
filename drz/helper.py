import os
import json
from .errors import DrizzleException


class DrizzleWrapper:

    def __init__(self, file_name, path):
        self._file_name = file_name
        with open(path, 'r') as file:
            self._contents = json.load(file)

    def __getitem__(self, item):
        if item in self._contents:
            return self._contents[item]
        raise DrizzleException("Malformed %s, could not find property '%s'" % (self._file_name, item))


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
    """When include is specified, only top-level files that
    pass the include will be bundled."""

    wd = os.getcwd()

    if include:
        os.chdir(path)
        path = "."

    def add_to_bundle(r, f):
        bundle.write(os.path.relpath(os.path.join(r, f)))

    for root, dirs, files in os.walk(path):
        if include is not None and path is root:
            for file in files:
                for rule in include:
                    if _pattern_matcher(file, rule):
                        add_to_bundle(root, file)  # doesn't respect excludes
                        break

            bad_dirs = []
            for directory in dirs:
                for rule in include:
                    if _pattern_matcher(directory, rule):
                        break
                else:
                    bad_dirs.append(directory)
            dirs[:] = [d for d in dirs if d not in bad_dirs]
            continue

        for file in files:
            for ex in exclude:
                if _pattern_matcher(file, ex):
                    break
            else:
                add_to_bundle(root, file)

    os.chdir(wd)


def _pattern_matcher(filename, pattern):
    if not pattern:  # don't match the empty string
        return False

    def recursive(remaining, parts):
        if not parts:
            return True

        if parts[0]:
            return remaining.startswith(parts[0]) and recursive(remaining[len(parts[0]):], parts[1:])
        elif len(parts) == 1:
            return True
        elif not parts[1]:
            return recursive(remaining, parts[1:])
        else:
            if parts[1] in remaining:
                return recursive(remaining[remaining.index(parts[1])+len(parts[1]):], parts[2:])
            return False

    return recursive(filename, pattern.split('*'))


def get_drizzle_json():
    p_drizzle = path_to("drizzle.json")

    if not os.path.exists(p_drizzle):
        raise DrizzleException("Couldn't find drizzle.json at "+os.getcwd())

    return DrizzleWrapper("drizzle.json", p_drizzle)
