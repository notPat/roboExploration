import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

INPUT_FILE = "SectorDensityMap.csv"
OUTPUT_DIR = "heatmap_output"

os.makedirs(OUTPUT_DIR, exist_ok=True)


rows = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    header = next(f, None)  

    for line in f:
        line = line.strip()
        if not line:
            continue

        try:
            sector_part, value_part = line.rsplit(",", 1)
        except ValueError:
            continue

        match = re.match(r"X=(-?\d+)\s+Y=(-?\d+)\s+Z=(-?\d+)", sector_part)
        if not match:
            continue

        x, y, z = map(int, match.groups())

        try:
            value = float(value_part)
        except ValueError:
            continue

        rows.append((x, y, z, value))

df = pd.DataFrame(rows, columns=["X", "Y", "Z", "Value"])

if df.empty:
    raise ValueError("Keine gültigen Daten gefunden.")

print("Anzahl Sektoren:", len(df))
print("Z-Ebenen:", sorted(df["Z"].unique()))


topdown = df.groupby(["Y", "X"], as_index=False)["Value"].sum()
pivot_top = topdown.pivot(index="Y", columns="X", values="Value").fillna(0)

plt.figure(figsize=(10, 8))
plt.imshow(
    np.log1p(pivot_top.values),   
    origin="lower",
    aspect="auto",
    cmap="viridis"
)
plt.colorbar(label="log(1 + Anzahl Punkte)")
plt.xlabel("Sektor X")
plt.ylabel("Sektor Y")
plt.title("Heatmap der SectorDensityMap (Top-Down, über Z aufsummiert)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "heatmap_topdown.png"), dpi=300)
plt.close()


for z_value in sorted(df["Z"].unique()):
    layer = df[df["Z"] == z_value]
    grouped = layer.groupby(["Y", "X"], as_index=False)["Value"].sum()
    pivot_layer = grouped.pivot(index="Y", columns="X", values="Value").fillna(0)

    plt.figure(figsize=(10, 8))
    plt.imshow(
        np.log1p(pivot_layer.values),
        origin="lower",
        aspect="auto",
        cmap="viridis"
    )
    plt.colorbar(label="log(1 + Anzahl Punkte)")
    plt.xlabel("Sektor X")
    plt.ylabel("Sektor Y")
    plt.title(f"Heatmap der SectorDensityMap für Z={z_value}")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"heatmap_z_{z_value}.png"), dpi=300)
    plt.close()

print("Fertig. Dateien gespeichert in:", OUTPUT_DIR)