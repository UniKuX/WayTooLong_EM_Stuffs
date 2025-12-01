import numpy as np
import matplotlib.pyplot as plt

# List your files
files = ["HisCC","HelHis","CC_Hel","actin_only"]


# Sample data
sampled_data = []

# First, randomly sample 10,000 rows from each file
for f in files:
    arr = np.load(f, allow_pickle=True)
    curvature = arr["filament/curvature"]
    n = min(15000, len(curvature))
    sampled_curvature = np.random.choice(curvature, size=n, replace=False)
    sampled_data.append(sampled_curvature)

# Determine global min and max for X axis
global_min = min([d.min() for d in sampled_data])
global_max = max([d.max() for d in sampled_data])

# Plot each histogram once to find max Y (counts)
counts = []
for data in sampled_data:
    hist, bin_edges = np.histogram(data, bins=50, range=(global_min, global_max))
    counts.append(hist.max())
global_ymax = max(counts)

# Plot side-by-side histograms
plt.figure(figsize=(12,7))
for i, (f, data) in enumerate(zip(files, sampled_data), 1):
    plt.subplot(4, 1, i)
    plt.hist(data, bins=50, range=(global_min, global_max), color='skyblue', edgecolor='black', log=False)
    plt.xlabel("Filament curvature")
    plt.ylabel("Count")
    plt.title(f"Histogram: {f}")
    plt.xlim(global_min, global_max)  # ensure same X-axis scale
    plt.ylim(0, global_ymax * 1.05)    # same Y (with 5% headroom)

plt.tight_layout()
plt.show()