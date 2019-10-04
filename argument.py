from sys import argv

PATH = "-path"
EXTENSION = "-ext"

class Arguments:
    def __init__(self):
        pass

def find(item):
    if item in argv:
        return argv[argv.index(item) + 1]
    else:
        return None

def argparse():
    args = Arguments()
    args.path = find(PATH)
    args.extension = find(EXTENSION)
    return args
