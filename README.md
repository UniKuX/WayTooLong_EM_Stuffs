# WayTooLong_EM_Stuffs
'Useful' little scripts I used for Cryo-EM and Cryo-ET processing.

For the python scripts, please check the codes to see what dependencies are required, most of the time it just needs 'starfile' package.
## filament
Jupyter notebook is to only keep the last 4 digits in the helical tube ID colum in CryoSPARC metadata. Might be useful when coverting to RELION .star files and enbale helical processing
The other three scripts are for plotting the filament curvature from CryoSPARC filament tracer.

## plot
Scripts to plot RELION generated .star files to generate CryoSPARC style plots for FSC curves and particle distributions.

## singularity
Files for making singularity containers, especially for RELION and King's College London CREATE

## tomography
A small script to bypass RELION 5.0 bugger AreTomo2 wrapper. Run the AreTomo2 seperately and replace the alignment data in the .star files. Probably useless now.

## utils
Some scripts to copy many files or whatever.
