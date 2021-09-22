#!/bin/bash

# This script takes all images from a given folder and runs a batch of pixel segmentation and
# object detection headlessly on the Hyak server.
# PARAMETERS:
#     imagesDir: This is the path to the folder of input images which is titled "day X".
#       It is relative to where this script is being run.
#       It should contain only raw images that you intend to process with ilastik.
# PRECONDITIONS:
#     the root dir of the project input should be under /gscratch/freedmanlab/ilastik/uwID/in
#     the imagesDir passed in should have a corresponding dir in /uwID/out/imagesDirName
#     assumes this script is run as "./auto_ilastik.sh ...params" (in other words, that this script is run while in
#         the scripts directory, and not called from a higher dir)
# EFFECTS:
#     Output will go to your local ./../out/projectName/day_X.
#     It will consist of probability images from pixel segmentation, detected object images
#     from object detection, and csv measurement and analysis from object detection,
#     as well as one output excel file summarizing the findings.
# REFERENCES:
#     https://www.ilastik.org/documentation/basics/headless.html

# A func to kill the script and direct errors to stderr
die () {
    # Print the given error message to stderr and then exit
    echo >&2 "$@"
    exit 1
}

# Parse arguments and options (flags)

# Checks we have the proper number of arguments passed in
[ "$#" -ge 1 ] || die "1 arguments required, $# provided, auto_ilastik.sh"

while getopts :n:t: flag
do
    case "${flag}" in
        n) noclean=true; shift;;
        t) test=true; shift;;
        *) echo "Unknown parameter passed: $1"; die "Unknown param" ;;
    esac
done

imagesDir=$1

day=$(basename $imagesDir)
projectName=$(basename $(echo $imagesDir | sed -e "s/$day//"))
# A path to where we want to put all output images and csvs relative to the working directory
# We go up three dirs (one for day, another for projectName, another for "in/", then we're in uwID)
# NOTE: check_file_structure.sh enforces up to the project name dir, and under that will be created when
# we run ilastik if those dirs do not already exist
outputDir="$imagesDir/../../../out/$projectName/$day/"
echo "Outputting to $outputDir"

# Stores a list of all the images we're processing
images=$(ls "$imagesDir")
echo "Input from $imagesDir"
echo "day: $day"
echo "Project name: $projectName"

#NOTE: ilastik has an error which requires NO SPACES in files,
# even if in quotes
noSpacesImages=""
# Determines field separators (ie spaces in file names should not separate fields)
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
for image in $images
do
  newImage=$(echo $image | sed -e "s/ /_/g")
  cp "$imagesDir/$image" "$imagesDir/$newImage"
  echo "New file name: $newImage"
  noSpacesImages="$noSpacesImages $imagesDir/$newImage "
done
IFS=$SAVEIFS
echo "Done renaming raw data to $noSpacesImages"


# PIXEL SEGMENTATION
#NOTE: Put your model name under project="your_model.ilp"
# (and make sure to put your model in the models directory)

# ** Replace project="..." **
if [[ $test == "" ]]
then
#    ilastikStart="/gscratch/scrubbed/freedman/ilastik/ilastik-1.4.0b15-Linux/run_ilastik.sh "
    ilastikStart="/gscratch/freedmanlab/ilastik-1.4.0b15-Linux/run_ilastik.sh "
else
    #NOTE: for debugging off the Hyak, insert your local path to ilastik here and use the -t flag
    ilastikStart="$HOME/Applications/ilastik-1.4.0b15-OSX.app/Contents/ilastik-release/run_ilastik.sh"
fi
$ilastikStart \
   	--headless \
    --project="../models/cyst_pixel_seg.ilp" \
    --table_filename=$outputDir/exported_object_features.csv \
    --output_filename_format="$outputDir/{nickname}_seg.tif" \
    --output_format="tif" \
    --export_source="probabilities" \
    --raw_data $noSpacesImages

# OBJECT DETECTION
#NOTE: Put your model name under project=".../models/your_model.ilp"

# Looping through output files from segmentation and creating the segmentation-images variable we will pass
# to object detection
noSpacesSegImages=""
# Determines field separators (ie spaces in file names should not separate fields)
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
outputImages=$(ls $outputDir) || die "can't find outputDir $outputDir"
for file in $outputImages
do
  # Check that it is a segmentation image / not some prior object detection
  # (by checking that it contains the substring "seg" which we append to the file name in segmentation)
  if [[ "${file}" =~ .*"seg".* ]]
  then
      newImage=$(echo $file | sed -e "s/ /_/g")
      cp "$outputDir/$file" "$outputDir/$newImage"
      echo "New segmentation file name: $newImage"
      # Appends the renamed image to the list of images
      noSpacesSegImages="$noSpacesSegImages $outputDir/$newImage "
  fi
done
IFS=$SAVEIFS

# Check that the files were found where we expected them and we were able to parse them
if [[ $noSpacesSegImages == "" ]]
then
  die "Cannot find output segmentation images in auto_ilastik.sh"
fi
echo "Done renaming segmentation images"

echo "No Spaces Images ${noSpacesImages}"
echo "" # line break
echo "No Spaces Seg Images for object detection input ${noSpacesSegImages}"

# CAUTION: when constructing these commands, make sure there is no equal sign after the raw_data or prediction_maps
    # arguments -- if there is that means it expects only one string argument instead of many images!
# ** Replace project="..." **
$ilastikStart \
  --headless \
	--project="../models/cyst_object_det3.ilp" \
	--output_filename_format="$outputDir/{nickname}_obj.tif" \
  --output_format="tif" \
	--table_filename="$outputDir/{nickname}.csv" \
  --raw_data $noSpacesImages \
	--prediction_maps $noSpacesSegImages

# Check error status of run
if [ $(echo $?) == "0" ] 
then
	echo "auto_ilastik.sh ran on the images successfully!"
else
	echo "auto_ilastik.sh failure! check the log files in home directory (~/ilastik_log.txt)??"
fi
