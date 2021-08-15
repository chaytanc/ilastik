#!/bin/bash

# This script has all the commands that are needed to bootstrap the object detection and analysis on the Hyak.
# It should be piped to an ssh command such that these commands are run on the Hyak.
# PARAMETERS:
#     rootdir: path (on Hyak) to the dir containing raw images in "day X" folders
#     hyakDir: The directory to the freedman lab files under which your user files are located
#         Ex: hyakDir = /gscratch/freedman/ilastik/, should contain /gscratch/freedman/ilastik/user

# Parse arguments and options (flags)

# Checks we have the proper number of arguments passed in
[ "$#" -ge 1 ] || die "1 argument required, $# provided"

#XXX copy this to auto_ilastik to parse noclean arg if it works here
noclean=false
while getopts :n: flag
do
    case "${flag}" in
        n) noclean=true;;
        *) echo "Unknown parameter passed: $1"; die "Unknown param" ;;
    esac
done
rootdir=$1
rootdir=$(basename rootdir)
hyakDir=$2

# A func to kill the script and direct errors to stderr
die () {
    echo >&2 "$@"
    exit 1
}

cd $hyakDir || die "Couldn't find $hyakDir"
echo $(pwd)

./check_file_strucuture.sh $hyakDir $rootdir

# Start run_batches.py
cd ${hyakDir}/scripts/
if [ $noclean == true ]
then
#XXX how to do sbatch with python instead of shell?    sbatch run_batches.py
# sbatch runs computation on computation node
    ./run_batches.py --noclean "$project_indir"
else
    ./run_batches.py "$project_indir"
fi