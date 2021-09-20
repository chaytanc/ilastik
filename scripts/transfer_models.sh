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
#  Ex: ./transfer_models.sh ~/ chaytan "../models/cyst_pixel_seg.ilp ../models/cyst_object_det3.ilp"
#
# EFFECTS:
#XXX todo

# A func to kill the script and direct errors to stderr
die () {
    echo >&2 "$@"
    exit 1
}

transfer_files() {
  # Read params
  transfer_path=$1
  files=$2
  # Iterate over possible files
  for file in $files
  do
      if [[ -d $file ]]
      then
          scp -r $file $transfer_path || die "Couldn't scp directory ${file}"
      else
          scp $file $transfer_path || die "Couldn't scp ${file}"
      fi
  done
}

main() {
      transferdir=$1
      uwid=$2
      transfer_path="${uwid}@klone.hyak.uw.edu:${transferdir}"
      files=$3
      transfer_files $transfer_path $files
}

# Checks we have the proper number of arguments passed in
[ "$#" -ge 3 ] || die "3 arguments required, $# provided, start.sh"
main $1 $2 $3

#XXX todo add support for editing the start.sh file with given models (also add flag that controls whether to do that)
# getopts for flag

# Tries to find scripts dir around where the model files were transferred to and if it does, looks for start.sh
# If start.sh is found, replaces --project "previous_pixel.ilp" lines to use --project "current_pixel.ilp" and
# --project "previous_object.ilp"
#replace_start_models() {
#}


