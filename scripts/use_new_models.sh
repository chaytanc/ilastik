#!/bin/bash
#This script will take in any number of arguments, with at least two. The first is the location on the Hyak where
#you want to transfer the files. The second, and potentially third, fourth, etc... arguments are the paths (relative to
#your working directory) to the models you would like to transfer to that location on the Hyak. Technically, despite
#being named use_new_models.py, you can transfer any type of file to any location on the Hyak. You
#could also specify a directory instead of a file. You will need to separately ssh for each different file to
#transfer it.
#PARAMETERS:
#    hyakdir: the root on the Hyak of the pipeline, for example, /gscratch/scrubbed/freedman/ilastik, which contains
#        scripts, models... and other folders
#    localauto: the local path of the auto_ilastik.sh file to replace the ilastik models in,
#       for example, "./auto_ilastik.sh"
#    uwid: your UW NetID which must have an account on the Hyak
#    pixel_model: local path to your pixel segmentation model, for example, "../models/cyst_pixel_seg.ilp"
#    object_model: local path to your object detection model
#
#EFFECTS:
##XXX todo

main() {
      hyakdir=$1
      localauto=$2
      uwid=$3
      pixel_model=$4
      object_model=$5
}


#XXX todo add support for editing the auto_ilastik.sh file with given models (also add flag that controls whether to do that)
#XXX todo turn in to a bash script because ffs python needs a module in order to


# Tries to find scripts dir around where the model files were transferred to and if it does, looks for auto_ilastik.sh
# If auto_ilastik.sh is found, replaces --project "previous_pixel.ilp" lines to use --project "current_pixel.ilp" and
# --project "previous_object.ilp"
replace_auto_models() {
      hyakdir=$1
      localauto=$2
      uwid=$3
      transfer_path="${uwid}@klone.hyak.uw.edu:${hyakdir}/scripts/"
      pixel_model=$4
      object_model=$5

    # locally edit auto_ilastik.sh
    #XXX todo test and then use -i flag once it works (backslashses are iffy)
    #XXX todo replace first occurrence w pixel model https://stackoverflow.com/questions/148451/how-to-use-sed-to-replace-only-the-first-occurrence-in-a-file
    sed "0,/--project.*/{s/--project.*/--project='..\/models\/test_pix.ilp'\\\ //}" ./data/mock_auto_ilastik.sh > temp.txt
    # replace second occurrence with obj model:
    # replace --project lines
    sed "s/--project.*/--project='..\/models\/test.ilp'\\\ /" auto_ilastik.sh  > temp.txt
    # save file / scp over to hyak
    scp $localauto $transfer_path
}