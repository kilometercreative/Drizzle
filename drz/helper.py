import os


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
