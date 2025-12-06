from pathlib import Path
import numpy as np
import pandas as pd

# Reproducible randomness
rng = np.random.default_rng(42)

N = 100  # number of parcels

# Dimensions in millimeters (rough, realistic ranges)
L = rng.integers(100, 600, size=N)   # length
W = rng.integers(80, 400, size=N)    # width
H = rng.integers(20, 300, size=N)    # height

# Basic attributes
stackable = rng.random(N) < 0.7       # 70% stackable
fragile   = rng.random(N) < 0.2       # 20% fragile

# Weight: derive from simple density model
# Convert mm^3 -> cm^3: 1 cm^3 = 1000 mm^3
volume_cm3 = (L * W * H) / 1000.0
# Choose densities (g/cm^3) across light -> medium items
density = rng.uniform(0.2, 0.9, size=N)
weight_g = np.clip(volume_cm3 * density, 50, 20000).round(0)  # clamp 50g–20kg

df = pd.DataFrame({
    "parcel_id": [f"P{i:03d}" for i in range(1, N + 1)],
    "length_mm": L,
    "width_mm":  W,
    "height_mm": H,
    "weight_g":  weight_g.astype(int),
    "stackable": stackable,
    "fragile":   fragile,
    # handy computed features
    "volume_cm3": volume_cm3.round(1),
    "dim_cm": (L/10 * W/10 * H/10).round(1)  # same as volume_cm3, explicit name if you like
})

# --- Output section (robust, path-safe version) ---
from pathlib import Path

# Base directory = location of this script (ai_cases)
base_dir = Path(__file__).parent

# data folder inside ai_cases
out_dir = base_dir / "data"
out_dir.mkdir(parents=True, exist_ok=True)

# CSV file inside that folder
out_path = out_dir / "parcels_sample.csv"

# Save and confirm
df.to_csv(out_path, index=False, encoding="utf-8")
print(f"Saved {len(df)} rows to {out_path.resolve()}")
