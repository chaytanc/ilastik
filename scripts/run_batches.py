#!/usr/bin/env python3
import os
import re
import argparse

'''
This script will run Ilastik object detection using auto_ilastik.sh on all sub dirs in the given directory.
USAGE: python3 run_batches.py /gscratch/freedmanlab/ilastik/my_images
    ARGS: 
        imagesdir: path (on Hyak) to the dir containing raw images in "day X" folders
        
EFFECTS:
    Pixel segmentation and object detection run by auto_ilastik.sh will be run on all "day X" folders in the
    given imagesdir. The result are tifs and csvs representing object detection output in the
    hyakDir/uwid/out/rootname/ folder on the Hyak.
    Moves any existing files at the specified output csv or xlsx to a .copy extension and saves 
    the new analysis files as out.csv or .xlsx
    
PRECONDITIONS:
    This script must be run on the Hyak.
'''

global ARGS
ARGS = None

# Gets the command line arguments and returns them
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("imagesdir", help="path to the directory containing 'day X' folders of raw images")
    return parser.parse_args()


# Gets all directories under imagesdir that contain "day" or "Day"
def get_subdirs(imagesdir):
    subdirs = []
    # Excludes strings matching out.* regex pattern so we don't analyze the output directory (hopefully...)
    excluded_pattern = re.compile(r'.*out.*')
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
        subdirs[0]
        print("Will run analysis on ", subdirs)
    except IndexError as e:
        print(e)
        raise FileNotFoundError("Could not find any 'day' or 'Day' subdirectory " + str(imagesdir))
    return subdirs


def run_batches(subdirs):
    exit_val = 0
    for subdir in subdirs:
        call = "./auto_ilastik.sh '%s'" % str(subdir)
        # Queue auto_ilastik.sh for a batch, need to then wait for it to finish before continuing
        #XXX working here
        # call = "sbatch auto_ilastik.sh '%s'" % str(subdir)
        print("\n CALLING ", call, "\n")
        temp_val = os.system(call)
        if temp_val != 0:
            exit_val = 1
    return exit_val


def run_analysis(imagesdir):
    project_name = os.path.basename(imagesdir)
    if project_name == "":
        project_name = os.path.basename(os.path.normpath(imagesdir))

    # Want to output in the output dir for the given project,
    # so we go up above project_name and "in", and down into "out" and project_name
    outputdir = imagesdir + "/../../out/" + project_name
    print("Analysis output dir: ", outputdir)
    #NOTE: this is where we set output file names??
    output_csv_path = outputdir + "/out.csv"
    output_formatted_path = outputdir + "/out.xlsx"
    move_existing_output_files(output_csv_path, output_formatted_path)
    # NOTE: multiple calls to consolidate_csvs.py without deleting out.csv will continually append
    call = "python3 consolidate_csvs.py " + outputdir + " " + output_csv_path
    os.system(call)
    call = "python3 format_data.py " + output_csv_path + " " + output_formatted_path
    os.system(call)


# Moves any existing files at the specified output csv or xlsx to a .copy extension and saves
# the new analysis files as out.csv or .xlsx
def move_existing_output_files(*paths_to_check):
    for path in paths_to_check:
        if os.path.exists(path):
            new = path + ".copy"
            os.rename(path, new)


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
