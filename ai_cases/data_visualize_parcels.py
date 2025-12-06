import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# --- Load dataset (robust path) ---
data_path = Path(__file__).parent / "data" / "parcels_sample.csv"
df = pd.read_csv(data_path)

# Pick a parcel to visualize (change the index to try others)
parcel = df.iloc[0]
L, W, H = float(parcel["length_mm"]), float(parcel["width_mm"]), float(parcel["height_mm"])

# Define the 8 corner points of the box
x = [0, L, L, 0, 0, L, L, 0]
y = [0, 0, W, W, 0, 0, W, W]
z = [0, 0, 0, 0, H, H, H, H]

# Triangles to form faces (Plotly Mesh3d uses indices i, j, k)
i = [0, 0, 0, 4, 4, 5, 6, 2, 1, 5, 6, 7]
j = [1, 2, 3, 5, 6, 6, 7, 3, 5, 1, 2, 3]
k = [2, 3, 0, 6, 7, 7, 4, 0, 0, 4, 5, 6]

fig = go.Figure(
    data=[go.Mesh3d(x=x, y=y, z=z, color="lightblue", opacity=0.5, flatshading=True)]
)

fig.update_layout(
    title=f"3D Parcel Visualization — ID: {parcel['parcel_id']}  "
          f"({int(L)}×{int(W)}×{int(H)} mm)",
    scene=dict(
        xaxis_title="Length (mm)",
        yaxis_title="Width (mm)",
        zaxis_title="Height (mm)",
        aspectmode="data"  # true-to-scale axes
    ),
    margin=dict(l=0, r=0, t=50, b=0)
)

fig.show()
