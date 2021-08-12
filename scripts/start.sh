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
#   rootdir: This is the path to the folder containing "day X" folders which contain the raw images of organoids.
#       It should contain only raw images that you intend to process with ilastik.
#   uwid: Your Hyak-authorized UW netID. Do not include "@uw.edu" in this argument.
#
# PRECONDITIONS:
#     1) Have a UW NetID that is authorized to login to the Hyak.(If this is not the case, contact
#         benof@uw.edu to request to gain access).
#     2) getopts,  is downloaded on the Hyak
#
# OUTPUT / EFFECTS:
# All files in the given directory will be renamed to use underscores instead of spaces.
# It's better this way, trust me.
# XXX Output will go to ./../out/??
# It will consist of one output excel file summarizing the findings, unless --noclean is set.

#https://stackoverflow.com/questions/14447406/bash-shell-script-check-for-a-flag-and-grab-its-value
#cleanup

# Parse arguments and options (flags)
rootdir=$1
#XXX need to store rootdir basename in case ./start.sh is called from diff dir
uwid=$2
noclean=false
#XXX switch to not be in scrubbed once lab gets its own storage
hyakDir="/gscratch/scrubbed/freedman/ilastik/"
# While number of parameters passed is greater than 0, parse them
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -n|--noclean) noclean=true;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Transfer scp local files to Hyak
  # Login
scp -r $rootdir "${uwid}@klone.hyak.uw.edu:${hyakDir}/"
# ssh into Hyak
  # Login
ssh "{$uwid}@klone.hyak.uw.edu"
mkdir $hyakDir
cd $hyakDir

# Make expected file structure on the Hyak (ssh must have succeeded XXX put an exit in above if it didnt')
#XXX working here to make file structure if it doesn't already exist, assuming this is run on Hyak
userdir="$hyakDir$uwid"
outdir="$userdir/out/"
project_outdir="$outdir/$rootdir/"
indir="$userdir/in/"
project_indir="$indir/$rootdir/"

dirtree=( $userdir $outdir $project_outdir $indir $project_indir )
for path in $dirtree
do
    mkdir "$path"
done

# Start run_batches.py
if [ $noclean == true ]
then
#XXX how to do sbatch with python instead of shell?    sbatch run_batches.py
    ./run_batches --noclean "$project_indir"
else
    ./run_batches "$project_indir"
fi


# Check error status of run
if [ $(echo $?) == "0" ] 
then
	echo "Ilastik ran on the images successfully!"
else
	echo "Failure! check the log files in home directory (~/ilastik_log.txt)??"
fi
