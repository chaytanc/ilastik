#!/usr/bin/env python3
import os
import re
import argparse


'''
This script will run Ilastik object detection using auto_ilastik.sh on all sub dirs in the given directory.
USAGE: python3 run_batches.py /gscratch/iscrm/freedman/my_images
    ARGS: 
        imagesdir: path (on Hyak) to the dir containing raw images in "day X" folders
        uwid: UW NetID that was used to log in to the Hyak (no @uw.edu)
    FLAGS: 
        --noclean will run auto_ilastik.sh without deleting the intermediate files made.
        Ex: python3 run_batches.py --no-clean "../in/my_cyst_images/"
        
XXX MOVED file structure building TO START.SH
EFFECTS:
    This script makes the file structure where input and output are stored on the Hyak, ie making 
    a directory for the UW NetID given under the .../freedman/ilastik directory on the Hyak, as well as 
    ...uwid/in and ...uwid/out directories and copying imagesdir to ...uwid/in/imagesdir
PRECONDITIONS:
    This script must be run on the Hyak.
'''

global ARGS
ARGS = None

global BASEDIR
BASEDIR = "/gscratch/scrubbed/freedman/ilastik/"


# Gets the command line arguments and returns them
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--noclean", action="store_true", help="does not automatically remove excess files from Ilastik output")
    parser.add_argument("imagesdir", help="path to the directory containing 'day X' folders of raw images")
    # parser.add_argument("uwid", help="the UW NetID of the Hyak user for these batches")
    return parser.parse_args()


# Gets all directories under imagesdir that contain "day" or "Day"
def get_subdirs(imagesdir):
    subdirs = []
    # Excludes strings matching out.*\.csv regex pattern
    excluded_pattern = re.compile(r'out.*')
    # Recurse through subdirs and get those that match day or Day pattern
    pattern = r'[(day)(Day)]'
    for root, foundSubdirs, files in os.walk(imagesdir):
        # Get subdirs that match day X pattern
        for subdir in filter(lambda x: re.match(pattern, x), foundSubdirs):
            bad_dir = re.match(excluded_pattern, subdir)
            if bad_dir:
                print("Skipping analysis on directory ", subdir)
            else:
                # Adds root so we get the full relative path
                subdirs.append(root + "/" + subdir + "/")

    # Check that there was at least one directory found
    try:
        dir1 = subdirs[0]
    except IndexError as e:
        print(e)
        raise FileNotFoundError("Could not find any 'day' or 'Day' subdirectory " + str(imagesdir))
    return subdirs


def run_batches(subdirs):
    exit_val = 0
    for subdir in subdirs:
        if ARGS.noclean:
            call = "./auto_ilastik.sh '%s'" % str(subdir)
        else:
            call = "./auto_ilastik.sh '%s' '%s'" % ("-n", str(subdir))
        print("\n CALLING ", call, "\n")
        temp_val = os.system(call)
        if temp_val != 0:
            exit_val = 1
    return exit_val


def run_analysis(imagesdir):
    #XXX copied from auto_ilastik.sh -- need to make globals file or something
    projectName = os.path.basename(imagesdir)

    # Want to output above the "day_X" output folders, so goes up above and imagesdir and in, and down into out/
    outputDir = imagesdir + "/../../out/" + projectName
    outputCSVPath = outputDir + "/out.csv"
    outputFormattedPath = outputDir + "/out.xlsx"
    # NOTE: multiple calls to consolidate_csvs.py without deleting out.csv will continually append
    call = "python3 consolidate_csvs.py " + outputDir + " " + outputCSVPath
    os.system(call)
    call = "python3 format_data.py " + outputCSVPath + " " + outputFormattedPath
    os.system(call)
    #XXX cleanup script


if __name__ == "__main__":
    ARGS = parse_args()
    # print("args: ", ARGS)
    # print("root: ", ARGS.imagesdir)
    subdirs = get_subdirs(ARGS.imagesdir)
    exit_val = run_batches(subdirs)
    if exit_val == 0:
        print("Success! Ran ilastik on all directories ", subdirs, " found.")
        print("Running analysis...")
        run_analysis(ARGS.imagesdir)
        print("Analysis done!")
