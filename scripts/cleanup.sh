#!/bin/bash

# This script will scp the segmentation images, object detection images, and formatted excel file back to the local
# directory from whence they came (relative to where start.sh was called). It then deletes the image files and csvs,
# leaving behind only the analysis csv in the Hyak directory. This script is not called if --noclean was passed to
# start.sh
# PARAMETERS:
#     outputDir: the directory where output was stored on the Hyak relative to the location of this script
#     outputFile: the consolidated csv file representing the output measurements of object detection as
#         formatted by format_data.py
#     destDir: the destination directory where the output images and excel file will be copied to
#     uwid: the UW NetID that you sshed into Hyak with
# EFFECTS:
#     copies all .tif files to the
#     deletes all csvs (that do not contain "out") and .tif images from the given outputDir

outputDir=$1
outputFile=$2
destDir=$3

# delete all csvs that aren't the output file since we consolidated them into the output file
for file in $outputDir
do
    if [[ $file == *.csv && $file -ne $outputFile ]]
    then
        rm $file
    fi
done

# scp the rest (anything with .tif and .csv or .excel)
#XXX problem: either need to close connection, scp remote files from local environment to local env
# or run the copy at the end after we're done with connection, or somehow start a task at the local env that does scp
# would need to know address to local machine from remote, need to know user running ssh
#scp -r $outputDir
# delete all .tif files
