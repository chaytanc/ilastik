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

#XXX should move this up the chain / enforce earlier in pipeline
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
#XXX using scrubbed temporarily while we potentially buy disk space
# ** Replace project="..." **
#XXX locally debugging and testing to see if issue only arises on Hyak
#/gscratch/scrubbed/freedman/ilastik/ilastik-1.3.3post3-Linux/run_ilastik.sh \
~/Applications/ilastik-1.4.0b15-OSX.app/Contents/ilastik-release/run_ilastik.sh \
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
  # Check that it is a segmentation image / not some prior object detection
  if [[ $image =~ "seg" ]]
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
echo "Done renaming"

echo "No Spaces Images ${noSpacesImages}"
echo "No Spaces Seg Images ${noSpacesSegImages}"

# CAUTION: when constructing these commands, make sure there is no equal sign after the raw_data or prediction_maps
    # arguments -- if there is that means it expects only one string argument instead of many images!
# ** Replace project="..." **
#/gscratch/scrubbed/freedman/ilastik/ilastik-1.3.3post3-Linux/run_ilastik.sh \
~/Applications/ilastik-1.4.0b15-OSX.app/Contents/ilastik-release/run_ilastik.sh \
  --headless \
	--project="../models/cyst_object_det3.ilp" \
	--output_filename_format="$outputDir/{nickname}_obj.tif" \
  --output_format="tif" \
	--table_filename="$outputDir/{nickname}.csv" \
  --prediction_maps $noSpacesSegImages \
  --raw_data $noSpacesImages

python3 consolidate_csvs.py $outputDir "${outputDir}/"
python3 format_data.py
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
