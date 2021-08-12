#!/usr/bin/env python3
import sys
import os
from pathlib import Path
import re
import argparse


'''
This script will run Ilastik object detection using auto_ilastik.sh on all sub dirs in the given directory.
USAGE: python3 run_batches.py /gscratch/iscrm/freedman/my_images
    ARGS: 
        rootdir: path (on Hyak) to the dir containing raw images in "day X" folders
        uwid: UW NetID that was used to log in to the Hyak (no @uw.edu)
    FLAGS: 
        --noclean will run auto_ilastik.sh without deleting the intermediate files made.
        Ex: python3 run_batches.py --no-clean "../in/my_cyst_images/"
        
XXX MOVED file structure building TO START.SH
EFFECTS:
    This script makes the file structure where input and output are stored on the Hyak, ie making 
    a directory for the UW NetID given under the .../freedman/ilastik directory on the Hyak, as well as 
    ...uwid/in and ...uwid/out directories and copying rootdir to ...uwid/in/rootdir
PRECONDITIONS:
    This script must be run on the Hyak.
'''

global ARGS
ARGS = None

global BASEDIR
BASEDIR = "/gscratch/scrubbed/freedman/ilastik"

# Gets the command line arguments and returns them
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("rootdir", help="path to the directory containing 'day X' folders of raw images")
    # parser.add_argument("uwid", help="the UW NetID of the Hyak user for these batches")
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
#MOVED THIS TO START.SH instead
# def make_file_structure(rootdir, uwid):
#     #XXX working here to make file structure if it doesn't already exist, assuming this is run on Hyak
#     userdir = os.path.join(BASEDIR, uwid)
#     outdir = os.path.join(userdir, "out")
#     project_outdir = os.path.join(outdir, rootdir)
#     # NOTE: these two should already exist from the scp
#     #projectroot = os.path.join(indir, rootdir)
#     #indir = os.path.join(userdir, "in")
#
#     dirtree = [userdir, outdir, project_outdir]
#     for path in dirtree:
#         os.mkdir(path)

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
