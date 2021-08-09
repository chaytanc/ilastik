#!/usr/bin/env python3
import sys
import os
from pathlib import Path
import re
import argparse


'''
This script will run Ilastik object detection using auto_ilastik.sh on all sub dirs in the given directory.
USAGE: python3 run_batches.py /gscratch/iscrm/freedman/my_images
    ARGS: rootdir: path (on Hyak) to the dir containing raw images in "day X" folders
    FLAGS: --noclean will run auto_ilastik.sh without deleting the intermediate files made.
        Ex: python3 run_batches.py --no-clean "../in/my_cyst_images/"
'''

global ARGS
ARGS = None


# Gets the command line arguments and returns them
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("rootdir", help="path to the directory containing 'day X' folders of raw images")
    parser.add_argument("--noclean", action="store_true", help="does not automatically remove excess files from Ilastik output")
    return parser.parse_args()


# Gets all directories under root_dir that contain "day" or "Day"
def get_subdirs(root_dir):
    subdirs = []
    # Excludes strings matching out.*\.csv regex pattern
    excluded_pattern = re.compile(r'out.*')
    # csv_files = [csv for csv in Path(csv_dir).rglob('*.csv')]
    #XXX not sure this Path thing works w regex, nor that it shows subdirs or is specifically for files
    # Recurse through subdirs and get those that match day or Day pattern
    pattern = r'[(day)(Day)]'
    # subs = Path(root_dir).rglob()
    # for subdir in subs:
    for root, foundSubdirs, files in os.walk(root_dir):
        for subdir in filter(lambda x: re.match(pattern, x), foundSubdirs):
            bad_dir = re.match(excluded_pattern, subdir)
            if bad_dir:
                print("skipping dir: ", subdir)
            else:
                print("good dir: ", subdir)
                #XXX need to make sure we append full path from root_dir to subdir
                # Adds root so we get the full relative path
                subdirs.append(root + subdir)

    # Check that there was at least one directory found
    try:
        dir1 = subdirs[0]
        print("First subdir:  " + str(dir1))
    except IndexError as e:
        print(e)
        raise FileNotFoundError("Could not find any 'day' or 'Day' subdirectory " + str(root_dir))
    return subdirs


def run_batches(subdirs):
    for subdir in subdirs:
        if ARGS.noclean:
            call = "./auto_ilastik.sh '%s'" % str(subdir)
        else:
            call = "./auto_ilastik.sh '%s' '%s'" % ("--noclean", str(subdir))
        os.system(call)


if __name__ == "__main__":
    ARGS = parse_args()
    print("args: ", ARGS)
    print("root: ", ARGS.rootdir)
    subdirs = get_subdirs(ARGS.rootdir)
    run_batches(subdirs)
    print("Success! Ran ilastik on all directories ", subdirs, " found.")
