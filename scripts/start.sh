#!/bin/bash

# This script detects organoids from batches of images that are placed in folders based on the day of imaging.
# It measures and analyzes the detected organoids, outputting the results in an excel file. Run this from your
# local computer, it will copy your local files to the Hyak and ssh automatically, though it will still prompt
# you for the password and 2FA.
#
# INPUT / PARAMETERS:
#   --noclean: a flag that determines whether or not the script will automatically clean up (remove) the files
#       intermediate files like .tif probability maps from the Hyak. By default, the only file remaining is the
#       excel analysis from object detection. If you set --noclean, make sure to clean up Hyak manually so it does
#       not run out of space.
#   rootdir: This is the local path to the folder containing "day X" folders which contain the raw images of organoids.
#       It should be relative to the location this start.sh script is being run.
#       It should contain only raw images that you intend to process with ilastik.
#   uwid: Your Hyak-authorized UW netID. Do not include "@uw.edu" in this argument.
#
# PRECONDITIONS:
#     1) Have a UW NetID that is authorized to login to the Hyak.(If this is not the case, contact
#         benof@uw.edu to request to gain access).
#     2) getopts, is downloaded on the Hyak
#     3) .../freedman/ilastik/uwid directory is set up / have been added as a freedman user
#
# OUTPUT / EFFECTS:
# All files in the given directory will be renamed to use underscores instead of spaces.
# It's better this way, trust me.
# XXX Output will go to ./../out/??
# It will consist of one output excel file summarizing the findings, unless --noclean is set.

#https://stackoverflow.com/questions/14447406/bash-shell-script-check-for-a-flag-and-grab-its-value
#cleanup

# A func to kill the script and direct errors to stderr
die () {
    echo >&2 "$@"
    exit 1
}

# Go to the directory from which this script is being run so paths relative to it work
MY_PATH="`dirname \"$0\"`"
cd $MY_PATH || die "Couldn't change dirs to where the script is"

# Parse arguments and options (flags)

noclean=false
# Checks we have the proper number of arguments passed in
[ "$#" -ge 2 ] || die "2 arguments required, $# provided"

while getopts :n: flag
do
    case "${flag}" in
        n) noclean=true; shift;;
        *) echo "Unknown parameter passed: $1"; die "Unknown param" ;;
    esac
done

# Set up useful references
noSpacesDir=$(echo $rootdir | sed -e "s/ /_/g")
rootdir=$1
uwid=$2
#XXX switch to not be in scrubbed once lab gets its own storage
# ** Replace with different path to freedman node on Hyak once we buy 1 TB storage **
hyakDir="/gscratch/scrubbed/freedman/ilastik/"

remove_path_underscores () {
    # Rename all directories to have underscores instead of spaces, starting at rootdir
    workingDir=$(pwd)
    cd $rootdir || die "couldn't cd to rootdir"
    cd ".."
    for d in $(find . -name '*_*' -type d) ; do
        new=$(echo $d | sed -e 's/_/ /g')
        mv $d $new
        echo "new dir: $new"
    done
    cd $workingDir
}
remove_path_underscores

# Transfer scp local files to Hyak
  # Login
scp -r $rootdir "${uwid}@klone.hyak.uw.edu:${hyakDir}/${uwid}/${noSpacesDir}/in/"

# ssh into Hyak
  # Login and run hyak bootstrap script
ssh "${uwid}@klone.hyak.uw.edu" "./remote_hyak_start.sh ${noSpacesDir} ${hyakDir}" || die "couldn't ssh in to Hyak"


# Check error status of run
if [ $(echo $?) == "0" ] 
then
	echo "Ilastik ran on the images successfully!"
else
	echo "Failure! check the log files in home directory (~/ilastik_log.txt)??"
fi
