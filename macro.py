import os
import re
import shutil
import sys
from argument import argparse, Arguments

MACRO      = ".macro."
MACRO_FILE = "Macro.h"
INCLUDE    = '#include "../' + MACRO_FILE + '"\n'
OUTPUT_DIR = "__macro__/"
PREPROCESSOR = "gcc -E"

whitespace = r"[\s\n\r\t]+"

def macro_file(path: str):
    # get the name of the file regardless of its location
    if "/" in path:
        filename = OUTPUT_DIR + path[path.rfind("/") + 1:]
        tempfile = OUTPUT_DIR + MACRO + path[path.rfind("/") + 1:]
    else:
        filename = OUTPUT_DIR + path
        tempfile = OUTPUT_DIR + MACRO + path

    # the path for the generated file to include the macro definitions
    includepath = ""
    for letter in path:
        if letter == "/":
            includepath += ".."
            includepath += "/"
    includepath += OUTPUT_DIR

    # add the include to the file, record first non-blank line
    with open(path, 'r') as original:
        contents = original.read()
        lines = contents.splitlines(True)
        i = 0
        while re.match(whitespace, lines[i]):
            i += 1
        firstline = lines[i]
    with open(tempfile, 'w') as temp:
        temp.write(INCLUDE + contents)

    # preprocess
    os.system(f"{PREPROCESSOR} {tempfile} 1> {filename}")
    os.remove(tempfile)

    # remove extaneous preprocessor output
    with open(filename, 'r') as modified:
        contents = modified.read().splitlines(True)
    with open(filename, 'w') as modified:
        i = 0
        while not contents[i] == firstline:
            i += 1
        modified.writelines(contents[i:])
    
def macro_dir(path: str, extension: str):
    for filename in os.listdir(path):
        if filename.endswith(extension):
            macro_file(path + filename)

def macro(arguments: Arguments):
    
    # remove (with all files) the output directory, then make an empty one
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    if os.path.isdir(arguments.path):
        macro_dir(arguments.path, arguments.extension)
    elif os.path.isfile(arguments.path):
        macro_file(arguments.path)
    else:
        print("Error: Invalid path", file=sys.stderr)
        exit(-1)

if __name__ == '__main__':
    arguments = argparse()
    macro(arguments)
