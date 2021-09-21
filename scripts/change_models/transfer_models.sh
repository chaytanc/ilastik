#!/bin/bash

# This script will take in any number of arguments, with at least two. The first is the location on the Hyak where
# you want to transfer the files. The second, and potentially third, fourth, etc... arguments are the paths (relative to
# your working directory) to the models you would like to transfer to that location on the Hyak. Technically, despite
# being named use_new_models.py, you can transfer any type of file to any location on the Hyak. You
# could also specify a directory instead of a file. You will need to separately ssh for each different file to
# transfer it.
# PARAMETERS:
#     transferdir: the location on the Hyak where you want to transfer the files.
#     uwid: your UW NetID which must have an account on the Hyak
#     files*: local path(s) to files you want to transfer. If you have multiple files, use the form where the whole
#       files argument is surrounded by quotes, but each file within the quotes is separated by a space.
# USAGE:
#  Ex: ./transfer_models.sh ~/ chaytan "../../models/cyst_pixel_seg.ilp ../../models/cyst_object_det3.ilp"
#     This example copies the two files cyst_pixel_seg.ilp and cyst_object_det3.ilp to my home directory at ~/
#     on the Hyak.

# A func to kill the script and direct errors to stderr
die () {
    echo >&2 "$@"
    exit 1
}

transfer_files() {

    # Read params
    # Shift to get the rest of args after the first
    transfer_path=$1; shift
    files=$*
    # Iterate over possible files
#    xargs -n 1 -J % transfer_file % <$files
    for file in ${files}
    do
      transfer_file "${file}"
    done
}

transfer_file() {
    echo "file: " $file
    if [[ -d $file ]]
    then
        scp -r $file $transfer_path || die "Couldn't scp directory ${file}"
    else
        scp $file $transfer_path || die "Couldn't scp ${file}"
    fi
}

main() {
      transferdir=$1
      uwid=$2
      shift; shift
      transfer_path="${uwid}@klone.hyak.uw.edu:${transferdir}"
      files="$*"
      echo "FILES: " "${files}"
      transfer_files $transfer_path $files
}

# Checks we have the proper number of arguments passed in
[ "$#" -ge 3 ] || die "3 arguments required, $# provided, start.sh"
main $1 $2 $3


