import os
import re
import shutil
import sys
from argument import argparse, Arguments

PREPROCESS_TEMP  = ".preprocess."
PREPROCESS_FILE  = "macros.h"
INCLUDE          = '#include "../' + PREPROCESS_FILE + '"\n'
OUTPUT_DIR       = "__preprocessed__/"
PREPROCESSOR     = "gcc -E"
PREPROCESSOR_EXT = ".c"

EXTRA_OUTPUT = r"#\s[\d]+"

def preprocess_file(path: str):
    # get the name of the file regardless of its location
    filename = OUTPUT_DIR
    tempfile = OUTPUT_DIR + PREPROCESS_TEMP
    if os.sep in path:
        filename += path[path.rfind(os.sep) + 1:]
        tempfile += path[path.rfind(os.sep) + 1:]
    else:
        filename += path
        tempfile += path
    # tempfile to a .c file
    tempfile = os.path.splitext(tempfile)[0] + PREPROCESSOR_EXT

    # the path for the generated file to include the preprocess definitions
    includepath = ""
    for letter in path:
        if letter == os.sep:
            includepath += ".."
            includepath += os.sep
    includepath += OUTPUT_DIR

    # add the include to the file, record first non-blank line
    with open(path, 'r') as original:
        contents = original.read()
    with open(tempfile, 'w') as temp:
        temp.write(INCLUDE + contents)

    # preprocess
    os.system(f"{PREPROCESSOR} {tempfile} 1> {filename}")
    os.remove(tempfile)

    # remove extaneous preprocessor output
    with open(filename, 'r') as modified:
        contents = modified.read().splitlines(True)
        index = 0
        for line in contents:
            if re.match(EXTRA_OUTPUT, line):
                index += 1
            else:
                break
    with open(filename, 'w') as modified:
        modified.writelines(contents[index:])
    
def preprocess_dir(path: str, extension: str):

    for filename in os.listdir(path):
        if filename.endswith(extension):
            preprocess_file(path + filename)

def preprocess(arguments: Arguments):
    
    # remove (with all files) the output directory, then make an empty one
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    if os.path.isdir(arguments.path):
        preprocess_dir(arguments.path, arguments.extension)
    elif os.path.isfile(arguments.path):
        preprocess_file(arguments.path)
    else:
        print(f"Error: Invalid path {arguments.path}", file=sys.stderr)
        exit(-1)

if __name__ == '__main__':
    arguments = argparse()
    preprocess(arguments)
