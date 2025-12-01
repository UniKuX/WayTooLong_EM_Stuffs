import numpy as np
import matplotlib.pyplot as plt

# Load your array
arr = np.load("J190_particles_selected_exported.cs", allow_pickle=True)

# Extract the field
curvature = arr["filament/curvature"]

# Plot histogram
plt.hist(curvature, bins=50)  # adjust number of bins if needed
plt.xlabel("Filament curvature")
plt.ylabel("Count")
plt.title("Histogram of filament curvature")
plt.show()