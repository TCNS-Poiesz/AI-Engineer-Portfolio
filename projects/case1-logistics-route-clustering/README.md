# Case 1 — Logistics Route Clustering

**Goal:** Cluster delivery points to design efficient unattended delivery zones.

## Steps
1. Load delivery points (lat/lon).
2. Run k-means for k ∈ {3,4,5}.
3. Visualize clusters on a map (Folium/Plotly).
4. Discuss operational implications.

## Data
- Place your CSV in `data/raw/` (gitignored). Example columns: `id,lat,lon`.
