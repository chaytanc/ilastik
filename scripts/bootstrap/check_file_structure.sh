#!/bin/bash

# This script is run on the Hyak periodically to check if the correct file structure is being used.
# (See File Strucutre Invariant Documentation or the README for more information)
# If directories that are presumed to exist do not, it creates them. For example,
# if there is no "/out/rootname" directory under the hyakDir/uwid path, then it is created.
# PARAMETERS:
#     rootname: name of the dir containing raw images in "day X" folders -- should have no spaces
#     hyakDir: The directory to the freedman lab files under which your user files are located
#         Ex: hyakDir = /gscratch/freedman/ilastik/, should contain /gscratch/freedman/ilastik/user
#         If using this script for testing, perhaps on a local machine, pass in the
#         the uwid directory which itself contains the project name dir
#     uwid: UW NetID that was used to log in to the Hyak (no @uw.edu)
# EFFECTS:
#    This script makes the file structure where input and output are stored on the Hyak, ie making
#    a directory for the uwid given under the hyakDir directory on the Hyak, as well as
#    ...uwid/in and ...uwid/out directories

# A func to kill the script and direct errors to stderr
die () {
    echo >&2 "$@"
    exit 1
}

# Checks we have the proper number of arguments passed in
[ "$#" -ge 2 ] || die "2 arguments required, $# provided, check_file_structure.sh"

rootname="$1"
rootname=$(basename $rootname)
hyakDir=$2
uwid=$3

userdir="$hyakDir/$uwid"
outdir="$userdir/out/"
project_outdir="$outdir/$rootname/"
indir="$userdir/in/"
project_indir="$indir/$rootname/"

#dirtree=( $userdir $outdir $project_outdir $indir $project_indir )
dirtree=( $project_outdir $project_indir )
for path in $dirtree
do
    if [[ -d "$path" ]]
    then
        echo "$DIRECTORY exists on your filesystem."
    # Make the dir if it didn't exist
    else
        # -p flag makes it so it also makes intermediate nonexisting directories so we don't have to directly
        # make indir and outdir anymore
        mkdir -p "$path" || die "failed to uphold Hyak file structure invariant"
        echo "made dir ${path}"
    fi
done
echo "File structure invariant is good, working dir: $(pwd)"

