import seaborn as sns
import matplotlib.pyplot as plt
import starfile
from matplotlib.colors import LogNorm


input_file = input("Enter STAR filename (e.g., HisCC_job100_run_data.star): ").strip()
df = starfile.read(input_file)

# --- If it's a dictionary (multiple data blocks), access 'data_particles' ---
if isinstance(df, dict):
    df = df['particles']

plt.figure(figsize=(10, 6))
ax = sns.histplot(
    x=df['rlnAngleRot'], 
    y=df['rlnAngleTilt'], 
    bins=120,         # You can adjust this for resolution
    cmap='plasma', 
    cbar=True
)
ax.set_xlim(-180, 180)
ax.set_ylim(0, 180)
ax.set_xlabel('Rotation Angle (°)')
ax.set_ylabel('Tilt Angle (°)')
ax.set_title('Particle Angular Distribution (Count Plot)')


plt.tight_layout()
# --- Save figure ---
output_file = input_file.replace('.star', '_AngularPlot.png')
plt.savefig(output_file, dpi=300)
print(f"Plot saved as: {output_file}")

plt.show()
