#!/bin/bash

# This script sets up a user on the Hyak with the necessary files and structure to run start.sh automatically.
# It only needs to be run once per user; only before the first time they ever want to run start.sh
# PARAMETERS: XXX
# EFFECTS:

rootdir=$1
hyakDir=$2

#XXX todo test this
# Transfer hyak bootstrap script
scp "./remote_hyak_start.sh" "${uwid}@klone.hyak.uw.edu:~/"
scp "./check_file_structure.sh" "${uwid}@klone.hyak.uw.edu:~/"
# ssh in so we can check the Hyak file structure
ssh "${uwid}@klone.hyak.uw.edu" "./check_file_structure.sh ${rootdir} ${hyakDir}" || die "couldn't ssh in to Hyak"
