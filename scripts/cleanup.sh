#!/bin/bash

# This script deletes the image files and csvs from the directory they are stored (based on hyakDir, uwid, and rootname)
# leaving behind only the analysis csv in the Hyak directory. This script is not called if -n was passed to
# start.sh
# PARAMETERS:
#     outputDir: Path to the output directory for this specific run on the Hyak (includes rootname)
# EFFECTS:
#     deletes all Hyak csvs (that do not contain "out") and .tif images from the given outputDir

# Parse arguments
#hyakDir=$1
#rootname=$2
#uwid=$3
outputDir=$1
#outputDir="${hyakDir}/${uwid}/out/${rootname}/"
# This filename was set by run_batches.py and we're assuming it's static for now
outputFile="${outputDir}/out.xlsx"

# delete all csvs that aren't the output file since we consolidated them into the output file
#XXX Need to do recursively for all day X directories and write a test for local
delete_hyak_files() {
  # for each level
  # remove files (tifs and non output csvs)
  # for all directories, go in and call this func
  # stop when no more subdirs
    for file in $outputDir
    do
       if [[ $file == *.csv && $file -ne $outputFile ]]
       then
          echo "Removing $file..."
          rm $file
       elif [[ $file == *.tif ]]
       then
          echo "Removing $file..."
          rm $file
       fi
    done
}

#XXX user input doesn't work with ssh -- could probably use flags instead
# Ask the user for confirmation before deleting Hyak files
#echo "Proceed to delete output images on the Hyak in ${outputDir}? (y/n)"
#read proceed
#if [[ $proceed == "y" || $proceed == "Y" || $proceed == "yes" || $proceed == "Yes" ]]
#then
echo "Cleaning up Hyak output in ${outputDir}..."
delete_hyak_files
#fi


