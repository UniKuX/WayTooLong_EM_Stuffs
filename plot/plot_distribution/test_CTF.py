import starfile
import matplotlib.pyplot as plt
import numpy as np

input_file = input("Enter STAR filename (e.g., Postprocess.star): ").strip()
df = starfile.read(input_file)

# Handle multi-block STAR files
if isinstance(df, dict):
    for key in df:
        if 'fsc' in key.lower() or 'ctf' in key.lower():
            df = df[key]
            break

x = df['rlnAngstromResolution'].to_numpy()

# Sort by resolution ascending (important for interpolation)
sort_idx = np.argsort(x)
x = x[sort_idx]

# List of FSC columns to plot and annotate
fsc_columns = [
    'rlnFourierShellCorrelationCorrected',
    'rlnFourierShellCorrelationParticleMaskFraction',
    'rlnFourierShellCorrelationUnmaskedMaps',
    'rlnFourierShellCorrelationMaskedMaps',
    'rlnCorrectedFourierShellCorrelationPhaseRandomizedMaskedMaps'
]

plt.figure(figsize=(10, 6))

colors = plt.cm.tab10.colors  # Up to 10 distinct colors

# Sort by resolution ascending
sort_idx = np.argsort(x)
x = x[sort_idx]

# Keep only points with resolution >= 16 Å
mask = x >= 16
x = x[mask]

for i, col in enumerate(fsc_columns):
    y = df[col].to_numpy()[sort_idx]

    plt.plot(x, y, label=col.split('_rln')[-1], lw=2, color=colors[i % len(colors)])

    # Find crossing resolution at FSC=0.143 by linear interpolation
    res_143 = None
    for j in range(1, len(y)):
        if y[j-1] > 0.143 >= y[j]:
            x1, x2 = x[j-1], x[j]
            y1, y2 = y[j-1], y[j]
            res_143 = x1 + (0.143 - y1) * (x2 - x1) / (y2 - y1)
            break

    if res_143 is not None:
        plt.axvline(res_143, color=colors[i % len(colors)], linestyle='--', lw=1)
        plt.text(res_143, 0.15, f"{res_143:.2f} Å", color=colors[i % len(colors)],
                 rotation=90, va='bottom', ha='right', fontsize=8)

# Draw horizontal reference lines
plt.axhline(0.143, color='gray', linestyle='--', lw=1)
plt.axhline(0.5, color='gray', linestyle='--', lw=1)

plt.xlabel('Resolution (Å)')
plt.ylabel('FSC')
plt.title('FSC Curves with 0.143 Cutoff Annotations')
plt.legend()
plt.grid(True)
plt.gca().invert_xaxis()
plt.tight_layout()

output_file = input_file.replace('.star', '_CTF_annotated_all.png')
plt.savefig(output_file, dpi=300)
print(f"Plot saved as: {output_file}")

plt.show()
