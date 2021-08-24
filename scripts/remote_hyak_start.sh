#!/bin/bash

# This script has all the commands that are needed to bootstrap the object detection and analysis on the Hyak.
# It should be piped to an ssh command such that these commands are run on the Hyak.
# PARAMETERS:
#     rootdir: path (on Hyak) to the dir containing raw images in "day X" folders
#     hyakDir: The directory to the freedman lab files under which your user files are located
#         Ex: hyakDir = /gscratch/freedman/ilastik/, if file invariant is followed,
#             this directory will also contain /gscratch/freedman/ilastik/user
#     uwid: UW NetID that was used to log in to the Hyak (no @uw.edu)

# A func to kill the script and direct errors to stderr
die () {
    echo >&2 "$@"
    exit 1
}

# Parse arguments and options (flags)

# Checks we have the proper number of arguments passed in
[ "$#" -ge 3 ] || die "3 arguments required, $# provided, remote_hyak_start.sh"

noclean=false
while getopts :n: flag
do
    case "${flag}" in
        n) noclean=true; shift;;
        *) echo "Unknown parameter passed: $1"; die "Unknown param" ;;
    esac
done
rootdir=$1
hyakDir=$2
uwid=$3

# Go to working directory and check file structure invariant
cd $hyakDir || die "Couldn't find $hyakDir"
pwd
./check_file_structure.sh $hyakDir $rootdir $uwid

# Start run_batches.py
cd ${hyakDir}/scripts/
if [ $noclean == true ]
then
#XXX how to do sbatch with python instead of shell?    sbatch run_batches.py
# sbatch runs computation on computation node
    ./run_batches.py --noclean "$rootdir"
else
    ./run_batches.py "$rootdir"
fi