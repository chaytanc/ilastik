#!/bin/bash
# This script will replace the paths to the pixel and object detection models called headlessly in the given file with
# given parameters for replacement pixel and object detection models. It will then transfer the replaced script to
# to the Hyak scripts directory. The paths to the models given should be relative to the Hyak scripts directory.

# PRECONDITIONS:
# Assumes that the modified file should go to hyakdir/scripts
# Assumes that the paths to the models given are relative to the Hyak and that the models exist there.
# (if you give a path to a model that isn't actually on the Hyak / hasn't been transferred, this script fails)
#
# PARAMETERS:
#    hyakdir: the root on the Hyak of the pipeline, for example, /gscratch/freedmanlab/ilastik, which contains
#        scripts, models... and other folders
#    localauto: the local path of the auto_ilastik.sh file to replace the ilastik models in,
#       for example, "./auto_ilastik.sh"
#    uwid: your UW NetID which must have an account on the Hyak
#    pixel_model: path to the pixel segmentation model on the Hyak relative to the scripts directory,
#       for example, "../models/cyst_pixel_seg.ilp"
#    object_model: path to the object detection model on the Hyak relative to the scripts directory
#
# EFFECTS:
# Replaces the models called headlessly by Ilastik in the given localauto file with the pixel and object models
# supplied, then transfers this file to the scripts directory on the Hyak.
# NOTE: if your localauto path is not in a local scripts directory like auto_ilastik.sh
# is on the Hyak, the paths to the model files will break locally
# (but will work on the Hyak)

# Calls python to replace --project "previous_pixel.ilp" lines to use --project "current_pixel.ilp" and
# --project "previous_object.ilp" then scps replaced file to the scripts directory of the hyak
replace_auto_models() {
      hyakdir=$1
      localauto=$2
      uwid=$3
      transfer_path="${uwid}@klone.hyak.uw.edu:${hyakdir}/scripts/"
      pixel_model=$4
      object_model=$5

#    sed "0,/--project.*/{s/--project.*/--project='..\/models\/test_pix.ilp'\\\ //}" ./data/mock_auto_ilastik.sh > temp.txt
#    sed "s/--project.*/--project='..\/models\/test.ilp'\\\ /" auto_ilastik.sh  > temp.txt
#    sed "s/--project.*/--project='..\/models\/test.ilp'\\\ /" ./tests/data/mock_auto_ilastik.sh  > temp.txt
    python3 use_new_models.py $localauto $pixel_model $object_model
    # save file / scp over to hyak
    scp $localauto $transfer_path
}
replace_auto_models $1 $2 $3 $4 $5