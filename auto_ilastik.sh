#!/bin/bash

# First arg from calling this script
imagesDir=$1

#~/Desktop/lab/Freedman\ Lab/cysts/b2_images
#~/Desktop/lab/freedman/cysts/b2_images
# runs from ilastik folder in home where Hello_World is located
images=$(ls "$imagesDir")
echo "Dir: "
echo $imagesDir
echo "IMAGES: "
echo $(ls "$imagesDir")
#NOTE: ilastik has an error which requires NO SPACES in files, 
# even if in quotes
noSpacesImages=""
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

~/Applications/ilastik-1.3.3post3-OSX.app/Contents/ilastik-release/run_ilastik.sh \
   	--headless \
	--project=Hello_World.ilp \
	--table_filename=/$imagesDir/exported_object_features.csv \
	--export_source="Object Predictions" \
	--raw_data $noSpacesImages
#Shouldn't need segmentation image since we're doing both at once
#   --segmentation_image my_unclassified_objects_1.h5/binary_segmentation_volume

# Check error status of run
if [ $(echo $?) == "0" ] 
then
	echo "Ilastik ran on the images successfully!"
else
	echo "Failure! check the log files in home directory (~/ilastik_log.txt)??"
fi
