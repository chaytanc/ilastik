#!/bin/bash

# This script sets up a user on the Hyak with the necessary files and structure to run start.sh automatically.
# It only needs to be run once per user; only before the first time they ever want to run start.sh
# PRECONDITIONS:
#     Run this from your local scripts directory (where start.sh is kept)
# PARAMETERS:
#XXX todo swap these params so hyakdir comes first and do the same for check_file_structure
#     rootname: the dir name (not path) which contains raw images in "day X" folders, ie "experiment1"
#     hyakDir: The directory to the freedman lab files under which your user files are located
#         Ex: hyakDir = /gscratch/freedmanlab/ilastik/, should contain /gscratch/freedmanlab/ilastik/user
#     uwid: UW NetID that was used to log in to the Hyak (no @uw.edu)
# EFFECTS:
# Copies over remote_hyak_start.sh, check_file_structure.sh, and cleanup.py, then sshes and runs check_file_structure.sh

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
#https://duo.com/docs/remembered-devices
# Can use  ssh keygen, would need script to do it automatically and not sure if this eliminates need for 2fa
scp -r "./bootstrap" "${uwid}@klone.hyak.uw.edu:~/"
# ssh in so we can check the Hyak file structure and check that anaconda is setup
#ssh "${uwid}@klone.hyak.uw.edu" "./bootstrap/check_file_structure.sh ${rootname} ${hyakDir} ${uwid}; \
#bash /gscratch/freedmanlab/Miniconda3-latest-Linux-x86_64.sh -b -u -p /gscratch/freedmanlab/miniconda3; \
#conda init bash; conda activate /gscratch/freedmanlab; echo setup done" || die "couldn't ssh in to Hyak, setup_user.sh"
#XXX removed sourcing Miniconda.sh file so that it doesn't reinstall conda for randy, just need to see if appending to
# his bashrc file will work
ssh "${uwid}@klone.hyak.uw.edu" "./bootstrap/check_file_structure.sh ${rootname} ${hyakDir} ${uwid}; \
echo ' \
# >>> conda initialize >>> \
# !! Contents within this block are managed by 'conda init' !! \
__conda_setup="$('/gscratch/freedmanlab/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)" \
if [ $? -eq 0 ]; then \
    eval "$__conda_setup" \
else \
    if [ -f "/gscratch/freedmanlab/miniconda3/etc/profile.d/conda.sh" ]; then \
        . "/gscratch/freedmanlab/miniconda3/etc/profile.d/conda.sh" \
    else \
        export PATH="/gscratch/freedmanlab/miniconda3/bin:$PATH" \
    fi \
fi \
unset __conda_setup \
# <<< conda initialize <<< \
# Setting base of conda to use freedman env, not default base \
export PATH="/gscratch/freedmanlab/miniconda3/condabin:$PATH" \
' >> ~/.bashrc \
conda init bash; conda activate /gscratch/freedmanlab; echo setup done" || die "couldn't ssh in to Hyak, setup_user.sh"
