import numpy as np
import matplotlib.pyplot as plt

# List your files
files = ["HisCC","HelHis","CC_Hel","actin_only"]

sampled_data = []

# Sample 10,000 rows from each file
for f in files:
    arr = np.load(f, allow_pickle=True)
    curvature = arr["filament/curvature"]
    n = min(10000, len(curvature))
    sampled_curvature = np.random.choice(curvature, size=n, replace=False)
    sampled_data.append(sampled_curvature)

# Global X range
global_min = min(d.min() for d in sampled_data)
global_max = max(d.max() for d in sampled_data)

# Plot side-by-side histograms with % on Y axis
plt.figure(figsize=(12,5))
for i, (f, data) in enumerate(zip(files, sampled_data), 1):
    plt.subplot(4, 1, i)
    
    # density=True makes histogram area = 1, multiply by 100 for percentage
    counts, bins, patches = plt.hist(
        data, bins=50, range=(global_min, global_max),
        color='skyblue', edgecolor='black', density=True
    )
    
    plt.xlabel("Filament curvature")
    plt.ylabel("Percentage (%)")
    plt.title(f"Histogram: {f}")
    plt.xlim(global_min, global_max)
    
    # Rescale Y ticks to percentages
    yticks = plt.gca().get_yticks()
    plt.gca().set_yticklabels([f"{y*100:.0f}%" for y in yticks])

plt.tight_layout()
plt.show()