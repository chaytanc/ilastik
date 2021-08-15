# This script is run on the Hyak periodically to check if the correct file structure is being used.
# If directories that are presumed to exist do not, it creates them.
# PARAMETERS:
#     rootdir: path (on Hyak) to the dir containing raw images in "day X" folders
#     hyakDir: The directory to the freedman lab files under which your user files are located
#         Ex: hyakDir = /gscratch/freedman/ilastik/, should contain /gscratch/freedman/ilastik/user


#XXX todo test this script
# Checks we have the proper number of arguments passed in
[ "$#" -ge 2 ] || die "2 arguments required, $# provided"

#XXX copy this to auto_ilastik to parse noclean arg if it works here
noclean=false
while getopts :n: flag
do
    case "${flag}" in
        n) noclean=true; shift;;
        *) echo "Unknown parameter passed: $1"; die "Unknown param" ;;
    esac
done
rootdir=$1
rootdir=$(basename rootdir)
hyakDir=$2

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