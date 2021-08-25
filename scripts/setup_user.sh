#!/bin/bash

# This script sets up a user on the Hyak with the necessary files and structure to run start.sh automatically.
# It only needs to be run once per user; only before the first time they ever want to run start.sh
# PRECONDITIONS:
#     Run this from your local scripts directory (where start.sh is kept)
# PARAMETERS:
#XXX todo swap these params so hyakdir comes first and do the same for check_file_structure
#     rootname: the dir name (not path) which contains raw images in "day X" folders, ie "experiment1"
#     hyakDir: The directory to the freedman lab files under which your user files are located
#         Ex: hyakDir = /gscratch/freedman/ilastik/, should contain /gscratch/freedman/ilastik/user
#     uwid: UW NetID that was used to log in to the Hyak (no @uw.edu)
# EFFECTS:
# Copies over remote_hyak_start.sh, check_file_structure.sh, and cleanup.sh, then sshes and runs check_file_structure.sh

# A func to kill the script and direct errors to stderr
die () {
    echo >&2 "$@"
    exit 1
}

rootname=$1
rootname=$(basename $rootname)
hyakDir=$2
uwid=$3

# Transfer hyak bootstrap script
#XXX todo make duo mobile remember user so less 2FA
# Can use  ssh keygen, would need script to do it automatically and not sure if this eliminates need for 2fa
#https://duo.com/docs/remembered-devices
scp "./remote_hyak_start.sh" "${uwid}@klone.hyak.uw.edu:~/"
scp "./check_file_structure.sh" "${uwid}@klone.hyak.uw.edu:~/"
scp "./cleanup.sh" "${uwid}@klone.hyak.uw.edu:~/"
# ssh in so we can check the Hyak file structure
ssh "${uwid}@klone.hyak.uw.edu" "./check_file_structure.sh ${rootname} ${hyakDir} ${uwid}" || die "couldn't ssh in to Hyak, setup_user.sh"
