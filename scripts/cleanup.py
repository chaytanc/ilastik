#!/bin/bash

# This script deletes the image files and csvs from the directory they are stored (based on hyakDir, uwid, and rootname)
# leaving behind only the analysis csv in the Hyak directory. This script is not called if -n was passed to
# start.sh
# PARAMETERS:
#     output_dir: Path to the output directory for this specific run on the Hyak (includes rootname)
# EFFECTS:
#     deletes all Hyak csvs (that do not contain "out") and .tif images from the given output_dir

import argparse
import os
import re


global ARGS
ARGS = None


# Gets the command line arguments and returns them
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="path to the directory containing output on the Hyak for this run")
    return parser.parse_args()


# delete all csvs and tifs that aren't the output files in the day X directories
def delete_hyak_files(output_dir):
    # Excludes strings matching out.* regex pattern so we don't remove output csv or xlsx files
    excluded_pattern = re.compile(r'.*out.*')
    # Recurse through subdirs and get those that match day or Day pattern
    # pattern = r'[(.*csv)(.*tif)]'
    pattern = r'(.*\.csv)|(.*\.tif)'
    # dir_pattern = r'[(Day.*)(day.*)]'
    dir_pattern = r'(Day.*)|(day.*)'
    for root, found_subdirs, files in os.walk(output_dir):
        # Get subdirs that match day X pattern and walk through them to get files
        for subdir in filter(lambda y: re.match(dir_pattern, y), found_subdirs):
            for subroot, _, subfiles in os.walk(os.path.join(root, subdir)):
                # Get files under day X dir that end in csv or tif and aren't output file
                to_delete = filter(lambda x: re.match(pattern, x), subfiles)
                for file in to_delete:
                    bad_file = re.match(excluded_pattern, file)
                    if bad_file:
                        print("Skipping cleanup on file ", file)
                    # The file found is a tif or csv that we want to delete from a 'day X' folder
                    else:
                        # remove the file
                        # add the day x part
                        path = os.path.join(subdir, file)
                        # add the root to the path
                        path = os.path.join(root, path)
                        print("Removing ", path, "...")
                        os.remove(path)


def main(output_dir):
    print("Cleaning up Hyak output in ", output_dir, "...")
    delete_hyak_files(output_dir)
    print("Cleaned up Hyak files.")


if __name__ == "__main__":
    ARGS = parse_args()
    output_dir = ARGS.output_dir
    main(output_dir)


