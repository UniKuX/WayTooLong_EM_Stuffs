#!/bin/bash

#Make sure to run this script in cryolo conda enviroment!!!!

#Use relative path only to your micrograph directory for relion
micrograph_dir="../MC_MRC_S28D_from_Cs_J39/"
#Use relative path only to your star file directory made by Cryolo        
star_dir="output_boxes_4/STAR/"                     

###########################################
#Also need the output directory for 
#cryolo_boxmanager_tools.py createAutopick,
#change that in the line 25
###########################################

# Iterate over each .mrc file in the micrograph directory
for mrc_file in "$micrograph_dir"*.mrc; do
    # Get the base filename without the extension
    base_filename=$(basename "$mrc_file" .mrc)

    # Construct the corresponding .cbox file path
    star_file="$star_dir${base_filename}.star"

    # Check if the corresponding .cbox file exists
    if [ -f "$star_file" ]; then
        # Run the cryolo_boxmanager_tools.py command with the matched files
        cryolo_boxmanager_tools.py createAutopick -m "$mrc_file" -c "$star_file" -o box4_test/${base_filename}.star
        
        # Print the processed files
        echo "Processed: $mrc_file and $star_file"
    else
        echo "Corresponding .star file not found for $mrc_file"
    fi
done
