#!/bin/bash

# This script has all the commands that are needed to bootstrap the object detection and analysis on the Hyak.
# It should be piped to an ssh command such that these commands are run on the Hyak.
# PARAMETERS:
#     rootdir:
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
hyakDir=$2

# A func to kill the script and direct errors to stderr
die () {
    echo >&2 "$@"
    exit 1
}

cd $hyakDir || die "Couldn't find $hyakDir"
echo $(pwd)

#XXX move this to setup_user.sh file that only runs once when user first joins
# Also makes no sense to make these directories after doing scp -- should make before and then scp, so do prior approach
# Make expected file structure on the Hyak (ssh must have succeeded)
userdir="$hyakDir/$uwid"
outdir="$userdir/out/"
project_outdir="$outdir/$rootdir/"
indir="$userdir/in/"
project_indir="$indir/$rootdir/"

#dirtree=( $userdir $outdir $project_outdir $indir $project_indir )
dirtree=( $project_outdir $project_indir )
for path in $dirtree
do
    # -p flag makes it so it also makes intermediate nonexisting directories so we don't have to directly
    # make indir and outdir anymore
    mkdir -p "$path" || die "failed to uphold Hyak file structure invariant"
    echo "made dir ${path}"
done

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