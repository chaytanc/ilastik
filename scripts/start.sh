#!/bin/bash

# This script detects organoids from batches of images that are placed in folders based on the day of imaging.
# It measures and analyzes the detected organoids, outputting the results in an excel file. Run this from your
# local computer, it will copy your local files to the Hyak and ssh automatically, though it will still prompt
# you for the password and 2FA.
# It will also scp the segmentation images, object detection images, and formatted excel file back to the local
# output directory (assumes the file structure is enforced locally).
#
# INPUT / PARAMETERS:
#   -n: a flag that determines whether or not the script will automatically clean up (remove) the files
#       intermediate files like .tif probability maps from the Hyak. By default, the only file remaining is the
#       excel analysis from object detection. If you set -n, make sure to clean up Hyak manually so it does
#       not run out of space.
#   -t: a flag that determines whether to copy input files over to the Hyak. Saves time debugging when you
#       have already transferred before mostly.
#   -p: Your phone number on which you would like to receive a text when the pipeline finishes
#   rootdir: This is the local PATH to the folder containing "day X" folders which contain the raw images of organoids.
#       It should be relative to the location this start.sh script is being run.
#       It should contain only raw images that you intend to process with ilastik.
#   uwid: Your Hyak-authorized UW netID. Do not include "@uw.edu" in this argument.
#
# PRECONDITIONS:
#     1) Have a UW NetID that is authorized to login to the Hyak.(If this is not the case, contact
#         benof@uw.edu to request to gain access).
#     2) .../freedmanlab/ilastik/uwid directory is set up / have been added as a freedman user
#     3) Current working directory is /gscratch/freedmanlab/ilastik
#
# OUTPUT / EFFECTS:
# All files and folders at or below the given rootdir will be renamed to use underscores instead of spaces.
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

# Sends a message when the Hyak is done, but only get one free per day...
phone_text() {
    phone=$1
    # Checks if phone param is null
    if [ ! -z "${phone}" ]
    then
        curl -X POST https://textbelt.com/text \
           --data-urlencode phone="$phone" \
           --data-urlencode message='The Hyak pipeline has finished running!' \
           -d key=textbelt
    fi
}

# Checks if the slurm job had an error file
check_logs() {
    outdir="$1"
    errfile=$(ls $outdir | grep .*err) || errfile="none"
    errpath="${outdir}/${errfile}"
    if [ $errfile != "none" ]
    then
        echo "ERROR in file $errpath"
        cat $errpath
    fi
}

# Go to the directory from which this script is being run so paths relative to it work
MY_PATH="`dirname \"$0\"`"
cd $MY_PATH || die "Couldn't change dirs to where the script is"

# Parse arguments and options (flags)

noclean=false
# Checks we have the proper number of arguments passed in
[ "$#" -ge 2 ] || die "2 arguments required, $# provided, start.sh"

while getopts :ntp: flag
do
    case "${flag}" in
        n) noclean=true;;
        t) notransfer=true;;
        p) phone=${OPTARG};;
        *) echo "Unknown parameter passed: $1"; die "Unknown param" ;;
    esac
done
shift $((OPTIND-1))

rootdir="$1"
noSpacesDir=$(echo "$rootdir" | sed -e "s/ /_/g")
uwid=$2

# ** Replace with different path to freedman node on Hyak once we buy 1 TB storage **
#hyakDir="/gscratch/scrubbed/freedman/ilastik/"
hyakDir="/gscratch/freedmanlab/ilastik/"

remove_path_underscores () {
    # Rename all directories to have underscores instead of spaces, starting at rootdir
    workingDir=$(pwd)
    cd "${rootdir}" || die "couldn't cd to rootdir"
    # Recursively finds all spaces in directories and replaces them with underscores
    find . -depth -name '* *' \
    | while IFS= read -r f ;
    do
      echo "Old dir with underscores: $f"
      new="$(dirname "$f")/$(basename "$f"|tr ' ' _)"
      mv -i "$f" $new;
      echo "New dir without underscores: $new"
    done

    cd $workingDir || die "Couldn't change dirs to ${workingDir}"
}
remove_path_underscores
# The rootname of the root directory (contains "day X" folders) without spaces
noSpacesName=$(basename "$noSpacesDir")

# Transfer scp local files to Hyak
  # Login
# If the -t flag is not set, transfer files over
if [[ $notransfer == "" ]]
then
    echo "Transferring your local ${noSpacesDir} directory..."
    scp -r "${noSpacesDir}" "${uwid}@klone.hyak.uw.edu:${hyakDir}/${uwid}/in/"
else
    echo "Skipping file transfer..."
fi

# Login and run hyak bootstrap script
echo "Starting the pipeline on the Hyak..."
say "Starting the pipeline on the Hyak..."
hyakOutDir="${hyakDir}/scripts/${noSpacesDir}/../../out/${noSpacesName}"
localOutDir="${noSpacesDir}/../../out/${noSpacesName}"

# Check local directory invariant before proceeding
./bootstrap/check_file_structure.sh $noSpacesName "../" $uwid

#NOTE: sbatch currently works but is very slow and hides stdout so not using. Also
# it does not fix the obj detection issue
ssh "${uwid}@klone.hyak.uw.edu" "rm ${hyakOutDir}/slurm.out ${hyakOutDir}/slurm.err; sbatch --output='${hyakOutDir}/slurm.out' --error='${hyakOutDir}/slurm.err' --wait ./bootstrap/remote_hyak_start.sh ${noSpacesDir} ${hyakDir} ${uwid}" || die "couldn't ssh in to Hyak for remote_hyak_start, start.sh"
#ssh "${uwid}@klone.hyak.uw.edu" "./bootstrap/remote_hyak_start.sh ${noSpacesDir} ${hyakDir} ${uwid}" || die "couldn't ssh in to Hyak, start.sh"

say "Hyak analysis is done" || say "There was an error"

# Transfer output files back to local
scp -r "${uwid}@klone.hyak.uw.edu:/${hyakOutDir}/*" "${localOutDir}" \
|| die "could not transfer Hyak output to local computer, start.sh"

# Check if there was a slurm.err file
check_logs ${localOutDir}

phone_text $phone
# ssh to Hyak, run cleanup script
# If noclean is null, clean up the Hyak (otherwise do nothing / complete)
if [ -z "${noclean}" ]
then
    echo "Cleaning up Hyak files..."
    ssh "${uwid}@klone.hyak.uw.edu" "python3 bootstrap/cleanup.py ${hyakOutDir}" || die "couldn't ssh in to Hyak to cleanup files, start.sh"
fi
say "The Hyak pipeline run completed!" || say "The Hyak pipeline experienced an error"

