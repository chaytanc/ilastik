#!/bin/bash

# This script takes all images from a given folder and runs a batch of pixel segmentation and
# object detection headlessly on the Hyak server.
# PARAMETERS:
#     imagesDir: This is the path to the folder titled "day X" relative to where this script is being run.
#        It should contain only raw images that you intend to process with ilastik.
# PRECONDITIONS:
#     the root dir of the project input should be under XXX change later /gscratch/scrubbed/freedman/ilastik/uwID/in
#     the imagesDir passed in should have a corresponding dir in .../uwID/out/imagesDir
# EFFECTS:
#     Output will go to ./../out/rootdir/day_X.
#     It will consist of probability images from pixel segmentation, detected object images
#     from object detection, and csv measurement and analysis from object detection,
#     as well as one output excel file summarizing the findings.
# REFERENCES:
#     https://www.ilastik.org/documentation/basics/headless.html
#XXX This output may get cleaned up later using cleanup.sh, leaving only the excel file output.

# A func to kill the script and direct errors to stderr
die () {
    echo >&2 "$@"
    exit 1
}

# Parse arguments and options (flags)

# Checks we have the proper number of arguments passed in
[ "$#" -ge 1 ] || die "1 arguments required, $# provided"

noclean=false
while getopts :n: flag
do
    case "${flag}" in
        n) noclean=true; shift;;
        *) echo "Unknown parameter passed: $1"; die "Unknown param" ;;
    esac
done

imagesDir=$1

# Rename imagesDir passed to have no underscores
echo $imagesDir
newDir=$(echo $imagesDir | sed -e "s/ /_/g")
echo $newDir
if [ $imagesDir != $newDir ]
then
    mv "$imagesDir" $newDir
    imagesDir=$newDir
fi

day=$(basename $imagesDir)
projectName=$(basename $(echo $imagesDir | sed -e "s/$day//"))
# A path to where we want to put all output images and csvs relative to the working directory
# We go up three dirs (one for day, another for projectName, another for "in/", then we're in uwID)
#XXX CHECK THIS -- enforce file structure invariant
# up out of day X, rootdir, in, then into out, rootdir, day
outputDir="$imagesDir/../../../out/$projectName/$day/"
echo "outputDir: $outputDir"

# Stores a list of all the images we're processing
images=$(ls "$imagesDir")
echo "Dir: "
echo $imagesDir
echo "IMAGES: "
echo $(ls "$imagesDir")
echo "day: "
echo $day
echo "projectName: "
echo $projectName

#NOTE: ilastik has an error which requires NO SPACES in files,
# even if in quotes
noSpacesImages=""
# Determines field separators (ie spaces in file names should not separate fields)
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
for image in $images
do
	echo "Image: $image"
	newImage=$(echo $image | sed -e "s/ /_/g")
	cp "$imagesDir/$image" "$imagesDir/$newImage"
	echo "New file name: $newImage"
	noSpacesImages="$noSpacesImages $imagesDir/$newImage "
done
IFS=$SAVEIFS
echo "Done renaming"


# PIXEL SEGMENTATION
#NOTE: Put your model name under --project="your_model.ilp"
# (and make sure to put your model in the models directory)

#XXX need to install ilastik in freedman and chaytan directories
#XXX not sure --raw_data $noSpacesImages works -- will have to test once disk quota is fixed
#XXX using scrubbed temporarily while we potentially buy disk space
# ** Replace project="..." **
#/gscratch/iscrm/freedman/ilastik/ilastik-1.3.3-Linux ./run_ilastik.sh \
#./gscratch/scrubbed/freedman/ilastik/ilastik-1.3.3post3-Linux/run_ilastik.sh \
/gscratch/scrubbed/freedman/ilastik/ilastik-1.3.3post3-Linux/run_ilastik.sh \
  --headless \
	--project="../models/cyst_pixel_seg.ilp" \
	--output_format="tif" \
	--output_filename_format="$outputDir/{nickname}.tif" \
	--export_source="Probabilities" \
	--raw_data=$noSpacesImages

# OBJECT DETECTION
#NOTE: Put your model name under --project="../models/your_model.ilp"

# Looping through output files from segmentation and creating the segmentation-images variable we will pass
# to object detection
noSpacesSegImages=""
# Determines field separators (ie spaces in file names should not separate fields)
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
outputImages=$(ls outputDir)
for file in $outputImages
do
	echo "Image: $file"
	newImage=$(echo $file | sed -e "s/ /_/g")
	cp "$outputDir/$file" "$outputDir/$newImage"
	echo "New file name: $newImage"
	# Appends the renamed image to the list of images
	noSpacesSegImages="$noSpacesSegImages $outputDir/$newImage "
done
IFS=$SAVEIFS
echo "Done renaming"

echo "No Spaces Images ${noSpacesImages}"
echo "No Spaces Seg Images ${noSpacesSegImages}"

# If you are processing more than one volume in a single command, provide all inputs of a given type in sequence:
#--raw_data "my_grayscale_stack_1/*.png" "my_grayscale_stack_2/*.png" "my_grayscale_stack_3/*.png" \
#--segmentation_image my_unclassified_objects_1.h5/binary_segmentation_volume my_unclassified_objects_2.h5/binary_segmentation_volume my_unclassified_objects_3.h5/binary_segmentation_volume
# ** Replace project="..." **
#/gscratch/iscrm/freedman/ilastik/ilastik-1.3.3-Linux ./run_ilastik.sh \
#./gscratch/scrubbed/freedman/ilastik/ilastik-1.3.3post3-Linux/run_ilastik.sh \
/gscratch/scrubbed/freedman/ilastik/ilastik-1.3.3post3-Linux/run_ilastik.sh \
  --headless \
	--project="../models/cyst_object_det3.ilp" \
	--output_format="tif" \
	--output_filename_format="$outputDir/{nickname}.tif" \
	--export_source="Probabilities" \
  --raw_data=$noSpacesImages \
  --segmentation_image=$noSpacesSegImages \

#XXX run consolidate_csvs.py
#XXX run format_data.py
# Transfer excel output back to local computer??
#XXX run cleanup script (base on flag parameter passed in)

# Check error status of run
if [ $(echo $?) == "0" ] 
then
	echo "Ilastik ran on the images successfully!"
else
	echo "Failure! check the log files in home directory (~/ilastik_log.txt)??"
fi
