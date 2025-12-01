import starfile
import matplotlib.pyplot as plt

# Load the STAR file
input_file = input("Enter STAR filename (e.g., Postporcess.star): ").strip()
df = starfile.read(input_file)


if isinstance(df, dict):
    df = df['fsc']

# Plot the FSC curves vs. resolution (Å)
plt.figure(figsize=(10, 6))

plt.plot(df['rlnResolution'], df['rlnFourierShellCorrelationCorrected'], label='Corrected FSC', lw=2)
plt.plot(df['rlnResolution'], df['rlnFourierShellCorrelationUnmaskedMaps'], label='Unmasked Maps FSC', lw=2)
plt.plot(df['rlnResolution'], df['rlnFourierShellCorrelationMaskedMaps'], label='Masked Maps FSC', lw=2)
plt.plot(df['rlnResolution'], df['rlnCorrectedFourierShellCorrelationPhaseRandomizedMaskedMaps'], label='Phase Rand. Masked Maps FSC', lw=2)

plt.axhline(0.143, color='gray', linestyle='--', lw=1)
plt.xlabel('Spacial Frequency (1/Å)')
plt.ylabel('FSC')
plt.title('FSC Curves')
plt.legend()
plt.grid(True)
plt.gca()  # Higher resolution on left
plt.tight_layout()
# --- Save figure ---
output_file = input_file.replace('.star', '_CTF.png')
plt.savefig(output_file, dpi=300)
print(f"Plot saved as: {output_file}")

plt.show()