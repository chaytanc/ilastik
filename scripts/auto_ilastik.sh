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
    # Print the given error message to stderr and then exit
    echo >&2 "$@"
    exit 1
}

# Parse arguments and options (flags)

# Checks we have the proper number of arguments passed in
[ "$#" -ge 1 ] || die "1 arguments required, $# provided, auto_ilastik.sh"

noclean=false
while getopts :n: flag
do
    case "${flag}" in
        n) noclean=true; shift;;
        *) echo "Unknown parameter passed: $1"; die "Unknown param" ;;
    esac
done

imagesDir=$1

#XXX This should be redundant because we do a find rename in start.sh that robustly removes spaces
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
# NOTE: check_file_structure.sh enforces up to the project name dir, and under that will be created when
# we run ilastik if those dirs do not already exist
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
echo "Done renaming raw data"


# PIXEL SEGMENTATION
#NOTE: Put your model name under --project="your_model.ilp"
# (and make sure to put your model in the models directory)

#XXX need to install ilastik in freedman and chaytan directories
#XXX using scrubbed temporarily while we potentially buy disk space
# ** Replace project="..." **
#XXX locally debugging and testing to see if issue only arises on Hyak
#~/Applications/ilastik-1.4.0b15-OSX.app/Contents/ilastik-release/run_ilastik.sh \
/gscratch/scrubbed/freedman/ilastik/ilastik-1.3.3post3-Linux/run_ilastik.sh \
   	--headless \
    --project="../models/cyst_pixel_seg.ilp" \
    --table_filename=$outputDir/exported_object_features.csv \
    --output_filename_format="$outputDir/{nickname}_seg.tif" \
    --output_format="tif" \
    --export_source="probabilities" \
    --raw_data $noSpacesImages

# OBJECT DETECTION
#NOTE: Put your model name under --project=".../models/your_model.ilp"

# Looping through output files from segmentation and creating the segmentation-images variable we will pass
# to object detection
noSpacesSegImages=""
# Determines field separators (ie spaces in file names should not separate fields)
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
outputImages=$(ls $outputDir) || die "can't find outputDir $outputDir"
for file in $outputImages
do
  echo "seg file: ${file}"
  # Check that it is a segmentation image / not some prior object detection
  # (by checking that it contains the substring "seg" which we append to the file name in segmentation)
  if [[ "${file}" =~ .*"seg".* ]]
  then
      echo "Image: $file"
      newImage=$(echo $file | sed -e "s/ /_/g")
      cp "$outputDir/$file" "$outputDir/$newImage"
      echo "New file name: $newImage"
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
echo "No Spaces Seg Images ${noSpacesSegImages}"

# CAUTION: when constructing these commands, make sure there is no equal sign after the raw_data or prediction_maps
    # arguments -- if there is that means it expects only one string argument instead of many images!
# ** Replace project="..." **
#~/Applications/ilastik-1.4.0b15-OSX.app/Contents/ilastik-release/run_ilastik.sh \
/gscratch/scrubbed/freedman/ilastik/ilastik-1.3.3post3-Linux/run_ilastik.sh \
  --headless \
	--project="../models/cyst_object_det3.ilp" \
	--output_filename_format="$outputDir/{nickname}_obj.tif" \
  --output_format="tif" \
	--table_filename="$outputDir/{nickname}.csv" \
  --prediction_maps $noSpacesSegImages \
  --raw_data $noSpacesImages

# Check error status of run
if [ $(echo $?) == "0" ] 
then
	echo "auto_ilastik.sh ran on the images successfully!"
else
	echo "auto_ilastik.sh failure! check the log files in home directory (~/ilastik_log.txt)??"
fi
