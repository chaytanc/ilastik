#!/bin/bash

# This script detects organoids from batches of images that are placed in folders based on the day of imaging.
# It measures and analyzes the detected organoids, outputting the results in an excel file. Run this from your
# local computer, it will copy your local files to the Hyak and ssh automatically, though it will still prompt
# you for the password and 2FA.
# It will also scp the segmentation images, object detection images, and formatted excel file back to the local
# output directory (assumes the file structure is enforced locally).
#
# INPUT / PARAMETERS:
#XXX todo fix noclean / test (also getopts doesn't support long options...
#   --noclean: a flag that determines whether or not the script will automatically clean up (remove) the files
#       intermediate files like .tif probability maps from the Hyak. By default, the only file remaining is the
#       excel analysis from object detection. If you set --noclean, make sure to clean up Hyak manually so it does
#       not run out of space.
#   --notransfer: a flag that determines whether to copy input files over to the Hyak. Saves time debugging when you
#       have already transferred before mostly.
#   rootdir: This is the local PATH to the folder containing "day X" folders which contain the raw images of organoids.
#       It should be relative to the location this start.sh script is being run.
#       It should contain only raw images that you intend to process with ilastik.
#   uwid: Your Hyak-authorized UW netID. Do not include "@uw.edu" in this argument.
#
# PRECONDITIONS:
#     1) Have a UW NetID that is authorized to login to the Hyak.(If this is not the case, contact
#         benof@uw.edu to request to gain access).
#     2) getopts is downloaded on the Hyak
#     3) .../freedman/ilastik/uwid directory is set up / have been added as a freedman user
#     4) Current working directory is /gscratch/scrubbed/freedman/ilastik
#
# OUTPUT / EFFECTS:
# All files in the given directory will be renamed to use underscores instead of spaces.
# It's better this way, trust me.
# Output will be copied back to the local path ./../{uwid}/out/{rootname} (assuming file invariant is locally upheld)
# Cleanup:
# Output on the Hyak is automatically deleted except for the formatted excel file (only after this output has been
# copied back over)

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
[ "$#" -ge 2 ] || die "2 arguments required, $# provided, start.sh"

while getopts :n:t: flag
do
    case "${flag}" in
        n) noclean=true; shift;;
        t) notransfer=true; shift;;
        *) echo "Unknown parameter passed: $1"; die "Unknown param" ;;
    esac
done

# Set up useful references
rootdir=$1
noSpacesDir=$(echo "$rootdir" | sed -e "s/ /_/g")
uwid=$2
#XXX switch to not be in scrubbed once lab gets its own storage
# ** Replace with different path to freedman node on Hyak once we buy 1 TB storage **
hyakDir="/gscratch/scrubbed/freedman/ilastik/"
#hyakDir="/gscratch/iscrm/freedman/ilastik/"

remove_path_underscores () {
    # Rename all directories to have underscores instead of spaces, starting at rootdir
    workingDir=$(pwd)
    cd $rootdir || die "couldn't cd to rootdir"
    cd ".."
    for d in $(find . -name '*_*' -type d) ; do
        new=$(echo "${d}" | sed -e 's/ /_/g')
        mv "${d}" $new
        echo "New dir without underscores: $new"
    done
    cd $workingDir || die "Couldn't change dirs to ${workingDir}"
}
remove_path_underscores

# Transfer scp local files to Hyak
  # Login
# If the -t flag is not set, transfer
if [[ $notransfer == "" ]]
then
    echo "Transferring your local files..."
    scp -r $noSpacesDir "${uwid}@klone.hyak.uw.edu:${hyakDir}/${uwid}/in/"
else
    echo "Skipping file transfer..."
fi

# ssh into Hyak
  # Login and run hyak bootstrap script
echo "Starting the pipeline on the Hyak..."
#XXX working here to get sbatch running instead of directly calling
ssh "${uwid}@klone.hyak.uw.edu" "sbatch --wait ./remote_hyak_start.sh ${noSpacesDir} ${hyakDir} ${uwid}" || die "couldn't ssh in to Hyak, start.sh"
# Transfer output files back to local
#XXX may need to mkdir first since file structure invariant is only enforced on hyak, not locally
noSpacesName=$(basename $noSpacesDir)
hyakOutDir="${hyakDir}/scripts/${noSpacesDir}/../../out/"
localOutDir="${noSpacesDir}/../../out/"
scp -r "${uwid}@klone.hyak.uw.edu:/${hyakOutDir}/*" "${localOutDir}" || die "could not transfer Hyak output to local computer, start.sh"
# ssh to Hyak, run cleanup script
echo "Cleaning up Hyak files..."
ssh "${uwid}@klone.hyak.uw.edu" "python3 cleanup.py ${hyakOutDir}" || die "couldn't ssh in to Hyak to cleanup files, start.sh"


# Check error status of run
if [ $(echo $?) == "0" ] 
then
	echo "Ilastik ran on the images successfully!"
else
	echo "Failure! check the log files in home directory (~/ilastik_log.txt)??"
fi
