#!/bin/bash

## SBATCH account and partition setup
#SBATCH --account=iscrm
#SBATCH --partition=compute-hugemem

## working directory for this job:
#SBATCH --chdir=/gscratch/freedmanlab/ilastik/scripts
## one way of saving output would be using job name, but I don't want unique log files to build up
##SBATCH --output="../logs/%x.%j.out"

## allocation:
## nodes: # of nodes
## ntasks-per-node: # cores per node
## mem: ram
## time: max running time
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --signal=USR2
#SBATCH --ntasks=28
#SBATCH --mem=120G

## email
#SBATCH --mail-type=ALL
#SBATCH --mail-user=chaytan@uw.edu

# This script has all the commands that are needed to bootstrap the object detection and analysis on the Hyak.
# It should be piped to an ssh command such that these commands are run on the Hyak.
# PARAMETERS:
#     rootdir: path (on Hyak) to the output dir containing raw images in "day X" folders
#     hyakDir: The directory to the freedman lab files under which your user files are located
#         Ex: hyakDir = /gscratch/freedman/ilastik/, if file invariant is followed,
#             this directory will also contain /gscratch/freedman/ilastik/user
#     uwid: UW NetID that was used to log in to the Hyak (no @uw.edu)

# A func to kill the script and direct errors to stderr
die () {
    echo >&2 "$@"
    exit 1
}

#XXX working here to remove previous slurm output files before running
remove_prev_logs() {
    outdir="$1"
    errfile=$(ls $outdir | grep .*err) || errfile="none"
    outfile=$(ls $outdir | grep slurm.out) || outfile="none"
    if [ errfile != "none" ]
    then
        errpath="${outdir}/${errfile}"
        echo "Removing ${errpath}"
        rm $errpath
    fi
    if [ outfile != "none" ]
    then
        outpath="${outdir}/${outfile}"
        echo "Removing ${outpath}"
        rm $outpath
    fi
}

# Parse arguments and options (flags)

# Checks we have the proper number of arguments passed in
[ "$#" -ge 3 ] || die "3 arguments required, $# provided, remote_hyak_start.sh"

rootdir=$1
hyakDir=$2
uwid=$3

#conda activate /gscratch/freedmanlab
remove_prev_logs $rootdir
./bootstrap/check_file_structure.sh $rootdir $hyakDir $uwid

# Go to working directory and check file structure invariant
cd $hyakDir || die "Error: Couldn't find $hyakDir"
# Start run_batches.py
cd ${hyakDir}/scripts/
echo "Working dir: $(pwd)"
echo "rootdir dir: ${rootdir}"

python3 run_batches.py "$rootdir"
