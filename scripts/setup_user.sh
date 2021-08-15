#!/bin/bash

# This script sets up a user on the Hyak with the necessary files and structure to run start.sh automatically.
# It only needs to be run once per user; only before the first time they ever want to run start.sh
# PARAMETERS:
#     XXX fix rootdir definition in all other sh files
#     rootdir: the dir name which contains raw images in "day X" folders, ie "experiment1"
#     hyakDir: The directory to the freedman lab files under which your user files are located
#         Ex: hyakDir = /gscratch/freedman/ilastik/, should contain /gscratch/freedman/ilastik/user
# EFFECTS:

rootdir=$1
rootdir=$(basename rootdir)
hyakDir=$2

#XXX todo test this
# Transfer hyak bootstrap script
scp "./remote_hyak_start.sh" "${uwid}@klone.hyak.uw.edu:~/"
scp "./check_file_structure.sh" "${uwid}@klone.hyak.uw.edu:~/"
# ssh in so we can check the Hyak file structure
ssh "${uwid}@klone.hyak.uw.edu" "./check_file_structure.sh ${rootdir} ${hyakDir}" || die "couldn't ssh in to Hyak"
