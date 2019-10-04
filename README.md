# Program Preprocessor
This Python utility utilizes the C preprocessor for use in languages other than C and C++.
## Format
To use the preprocessor, you must define all of your C style macros in a file called `macro.h`. This file must be placed in a location similar to that of a Makefile. Once all of the macros are defined, you can run the program with the proper command line arguments. For convenience of use, it is recommended that you create an alias for calling Preprocess: `alias preprocess='python3 <path to repo>/preprocess.py'`.
## Usage
Below are the use cases for Preprocess (assuming the prementioned alias).
```
# preprocess a single file
$ preprocess -path test.py

# preprocess all *.py files in a directory
$ preprocess -path test/ -ext .py
```
When the preprocessing is complete, all files will be placed under `__preprocessed__/`
## Dependencies
* gcc
* Python 3
## Portability
Preprocess runs on Windows Powershell, Windows Subsystem for Linux, and Debian based Linux distros (other distros have not been tested).