#Make sure to run this script in cryolo conda enviroment!!!!

import os
import subprocess

# Same shit as Making_shit_ton_of_star_files_from_Cryolo.sh, but in python
# Use relative path only to your micrograph directory for relion
micrograph_dir = "../MC_MRC_S28D_from_Cs_J39/"
# Use relative path only to your star file directory made by Cryolo        
star_dir = "output_boxes_4/STAR"
# Specify your output directory here
output_dir = "box4_test/"  

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get list of .mrc files in the micrograph directory
mrc_files = [f for f in os.listdir(micrograph_dir) if f.endswith('.mrc')]

# Iterate over each .mrc file
for mrc_file in mrc_files:
    # Get the base filename without the extension
    base_filename = os.path.splitext(mrc_file)[0]

    # Construct the corresponding .star file path
    star_file = os.path.join(star_dir, f"{base_filename}.star")

    # Construct the full path to the .mrc file
    mrc_file_path = os.path.join(micrograph_dir, mrc_file)

    # Construct the output file path
    output_file = os.path.join(output_dir, f"{base_filename}")  # Adjust the output file name as needed

    # Check if the corresponding .star file exists
    if os.path.isfile(star_file):
        # Run the cryolo_boxmanager_tools.py command with the matched files and output file
        subprocess.run([
            "cryolo_boxmanager_tools.py", "createAutopick",
            "-m", mrc_file_path,
            "-c", star_file,
            "-o", output_file
        ])

        # Print the processed files
        print(f"Processed: {mrc_file_path} and {star_file}, output saved to {output_file}")
    else:
        print(f"Corresponding .star file not found for {mrc_file_path}")
