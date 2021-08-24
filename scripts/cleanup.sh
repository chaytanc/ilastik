#!/bin/bash

# This script ssh then deletes the image files and csvs,
# leaving behind only the analysis csv in the Hyak directory. This script is not called if --noclean was passed to
# start.sh
# PARAMETERS:
#     hyakDir: The directory to the freedman lab files under which your user files are located
#         Ex: hyakDir = /gscratch/freedman/ilastik/, if file invariant is followed,
#             this directory will also contain /gscratch/freedman/ilastik/user
#     rootname: the dir name (not path) which contains raw images in "day X" folders, ie "experiment1"
#     uwid: UW NetID that was used to log in to the Hyak (no @uw.edu)
# EFFECTS:
#     deletes all Hyak csvs (that do not contain "out") and .tif images from the given outputDir

# Parse arguments
hyakDir=$1
rootname=$2
uwid=$3
outputDir="${hyakDir}/${uwid}/out/${rootname}/"
# This filename was set by run_batches.py and we're assuming it's static for now
outputFile="${outputDir}/out.xlsx"

# delete all csvs that aren't the output file since we consolidated them into the output file
delete_hyak_files() {
    for file in $outputDir
    do
       if [[ $file == *.csv && $file -ne $outputFile ]]
       then
           rm $file
       fi
    done
}

# Ask the user for confirmation before deleting Hyak files
#XXX not sure this works while we're sshed?
echo "Proceed to delete output images on the Hyak in ${outputDir}? (y/n)"
read proceed
if [[ $proceed == "y" || $proceed == "Y" || $proceed == "yes" || $proceed == "Yes" ]]
then
    delete_hyak_files
fi


