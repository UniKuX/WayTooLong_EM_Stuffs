#!/bin/csh

# Set the source and destination directories
set source_dir = "The directory of your big ass data set"
set dest_dir = "Where you want to put the symbolic links"

# Check if source directory exists
if (! -d $source_dir) then
    echo "Source directory does not exist!"
    exit 1
endif

# Check if destination directory exists, if not, create it
if (! -d $dest_dir) then
    mkdir -p $dest_dir
endif

# Use find to locate files with the desired pattern and create symbolic links
foreach file (`find $source_dir -name "*_fractions_patch_aligned_doseweighted.mrc"`)
    # Extract only the filename from the full path
    set filename = `basename $file`
    # Create symbolic link in the destination directory
    ln -s $file $dest_dir/$filename
end
