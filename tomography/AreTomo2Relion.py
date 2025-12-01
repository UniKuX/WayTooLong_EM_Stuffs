import os
import pandas as pd
import starfile

# Define the directories
tiltseries_dir = 'job034/tilt_series'
aln_dir = 'tomograms_from_create'
output_dir = 'job034/updated_tiltseries'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Helper function to read .aln files using pandas
def read_aln_file(filepath):
    try:
        df = pd.read_csv(filepath, delim_whitespace=True, comment='#', header=None, 
                         names=['SEC', 'ROT', 'GMAG', 'TX', 'TY', 'SMEAN', 'SFIT', 'SCALE', 'BASE', 'TILT'])
        return df['TX'].values, df['TY'].values
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None, None

# List all .star files in the tiltseries directory
star_files = [f for f in os.listdir(tiltseries_dir) if f.endswith('.star')]

# Traverse and process each .star file
for star_filename in star_files:
    base_name = star_filename.replace('.star', '')
    aln_filename = base_name.replace('_', '_') + '.st' + '.aln'  # Adjust the .aln filename
    
    aln_filepath = os.path.join(aln_dir, aln_filename)
    
    if os.path.exists(aln_filepath):
        tx_values, ty_values = read_aln_file(aln_filepath)
        
        if tx_values is not None and ty_values is not None:
            # Print the values of TX and TY read from the .aln file
            print(f"Values read from {aln_filepath}:")
            print("TX values:", tx_values)
            print("TY values:", ty_values)
            
            # Multiply by pixel size (assuming pixel size is 2.1)
            tx_values = [tx * 2.1 for tx in tx_values]
            ty_values = [ty * 2.1 for ty in ty_values]
            
            # Print the modified values of TX and TY
            print(f"Modified values for {aln_filepath}:")
            print("TX values:", tx_values)
            print("TY values:", ty_values)

            # Process corresponding .star file
            star_filepath = os.path.join(tiltseries_dir, star_filename)
            
            if os.path.exists(star_filepath):
                try:
                    star_data = starfile.read(star_filepath)
                    
                    # Update columns _rlnTomoXShiftAngst and _rlnTomoYShiftAngst if they exist
                    if 'rlnTomoXShiftAngst' in star_data.columns and 'rlnTomoYShiftAngst' in star_data.columns:
                        # Check if the lengths of tx_values and ty_values match the number of rows in the DataFrame
                        if len(tx_values) == len(star_data) and len(ty_values) == len(star_data):
                            # Update columns
                            star_data['rlnTomoXShiftAngst'] = tx_values
                            star_data['rlnTomoYShiftAngst'] = ty_values

                            # Update _rlnTomoZRot column to 87.01
                            star_data['rlnTomoZRot'] = 87.01

                            # Define the output file path
                            output_filepath = os.path.join(output_dir, star_filename)
                            
                            # Write the updated .star file
                            starfile.write(star_data, output_filepath)
                            print(f"Updated .star file written to {output_filepath}")
                        else:
                            print(f"Length of TX or TY values does not match the length of the DataFrame in {star_filepath}")
                    else:
                        print(f"Columns '_rlnTomoXShiftAngst' and '_rlnTomoYShiftAngst' not found in {star_filepath}")
                except Exception as e:
                    print(f"Error processing {star_filepath}: {e}")
            else:
                print(f"Star file {star_filepath} does not exist.")
        else:
            print(f"Skipping {aln_filepath} due to read error.")
    else:
        print(f"Alignment file {aln_filepath} does not exist.")
