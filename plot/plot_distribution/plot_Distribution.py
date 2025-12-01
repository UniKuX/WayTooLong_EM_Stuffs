import matplotlib.pyplot as plt
import starfile
import numpy as np

input_file = input("Enter STAR filename (e.g., HisCC_job100_run_data.star): ").strip()
df = starfile.read(input_file)

if isinstance(df, dict):
    df = df.get('particles', df)

x = df['rlnAngleRot'].values
y = df['rlnAngleTilt'].values

plt.figure(figsize=(10, 6))

hb = plt.hexbin(
    x, y,
    gridsize=80,           # number of hexagons along x-axis (adjust as needed)
    cmap='plasma',  # colormap for the hexagons
    mincnt=1,              # ignore empty bins
    bins='log'             # log scale for color bar counts
)

plt.colorbar(hb, label='log10(Counts)')
plt.xlim(-180, 180)
plt.ylim(0, 180)
plt.xlabel('Rotation Angle (°)')
plt.ylabel('Tilt Angle (°)')
plt.title('Particle Angular Distribution (Hexbin, log counts)')

plt.tight_layout()

output_file = input_file.replace('.star', '_AngularHexbin.png')
plt.savefig(output_file, dpi=300)
print(f"Hexbin plot saved as: {output_file}")

plt.show()