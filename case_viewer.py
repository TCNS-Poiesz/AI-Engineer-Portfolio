import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
from ai_cases.ud_embeddings_analyzer import UDEmbeddingsAnalyzer

# --- Config ---
st.set_page_config(page_title="AI Case Viewer", layout="wide")
page = st.sidebar.radio(
    "Choose AI Case",
    ["Case 1 – Space Optimization & UD", "Case 2 – UD Incident Embeddings"]
)
# ============================================================
# AI Case Viewer — TODO (next session)
# 1) Confirm columns AFTER rename include w/d/h
# 2) Ensure rename happens BEFORE any r["w"]/r["d"]/r["h"] access
# 3) Verify Plotly 3D boxes render (green + red)
# 4) Remove debug prints (st.write columns)
# 5) Optional: Add locker boundary wireframe / toggle
# ============================================================

def case1_page():
    st.title("AI Case 1 – Space Optimization & Unattended Delivery")

    # --- Load and Display Markdown ---
    case_path = Path("ai_cases/case1_space_optimization_unattended_delivery.md")
    if case_path.exists():
        st.markdown(case_path.read_text(encoding="utf-8"), unsafe_allow_html=True)
    else:
        st.error("Case file not found. Please check your folder path.")
        st.stop()

    # --- Load parcels CSV ---
    data_path = Path("ai_cases/data/parcels_sample.csv")
    if not data_path.exists():
        st.error(f"Missing data file: {data_path}")
        st.stop()

    df = pd.read_csv(data_path)

    # ---------- Locker size sliders FIRST ----------
    st.sidebar.header("Locker Dimensions (meters)")
    locker_w = st.sidebar.slider("Locker width (W)", 0.2, 2.0, 1.0, 0.05)
    locker_d = st.sidebar.slider("Locker depth (D)", 0.2, 2.0, 1.0, 0.05)
    locker_h = st.sidebar.slider("Locker height (H)", 0.2, 2.5, 1.5, 0.05)

    # ---------- Normalize parcel dataset ----------
    if {"length_mm", "width_mm", "height_mm"}.issubset(df.columns):
        df = df.rename(
            columns={
                "width_mm": "width",
                "length_mm": "depth",
                "height_mm": "height",
            }
        )
        df[["width", "depth", "height"]] = df[["width", "depth", "height"]] / 1000.0

    # If positions are missing, generate placeholder positions
    if not {"x", "y", "z"}.issubset(df.columns):
        rng = np.random.default_rng(0)
        df["x"] = rng.uniform(0, locker_w, size=len(df))
        df["y"] = rng.uniform(0, locker_d, size=len(df))
        df["z"] = rng.uniform(0, locker_h, size=len(df))

    # ---------- Sanity check ----------
    required_cols = {"width", "depth", "height", "x", "y", "z"}
    missing = required_cols - set(df.columns)
    if missing:
        st.error(f"Still missing required columns after normalization: {missing}")
        st.stop()

    # Clamp parcel dimensions so they never exceed locker bounds
    df["width"] = df["width"].clip(upper=locker_w)
    df["depth"] = df["depth"].clip(upper=locker_d)
    df["height"] = df["height"].clip(upper=locker_h)
    # ---------- Physical properties (demo, but data-aware) ----------
    # In real logistics data, weight and stackability normally come from
    # the carrier/shipper manifest. Here we:
    # 1) Use existing columns if present.
    # 2) Otherwise, derive demo values so the prototype remains usable.

    # Volume in cubic meters (always safe to compute).
    df["volume_m3"] = df["width"] * df["depth"] * df["height"]

    if {"weight_kg", "max_top_load_kg"}.issubset(df.columns):
        # Use provided logistics data
        df["weight_kg"] = df["weight_kg"].astype(float)
        df["max_top_load_kg"] = df["max_top_load_kg"].astype(float)
    else:
        # Demo fallback: approximate weight from volume using a fake density.
        density = 250  # "kg per cubic meter" (illustrative only)
        df["weight_kg"] = df["volume_m3"] * density

        # Demo rule: parcel can carry 3x its own weight on top.
        df["max_top_load_kg"] = 3.0 * df["weight_kg"]

    # ---------- Stackability flag (demo rule) ----------
    # Demo rule: a parcel is "stackable" if its height is at most 40% of the
    # current locker height. This is purely illustrative and can later be
    # replaced with ML or richer business rules.
    df["stackable"] = df["height"] <= 0.4 * locker_h
    # ---------- Canonical parcel schema (v1.0) ----------
    # These columns mirror how real logistics systems tend to represent parcels.
    # If some fields are missing in the CSV, we create sensible defaults so
    # the rest of the app can rely on a stable schema.

    # Core geometry (already ensured earlier): width, depth, height, volume_m3
    # Core physics: weight_kg, max_top_load_kg (from data or demo fallback)

    # Stackability & fragility flags
    df["stackable_flag"] = df["stackable"].astype(bool)

    if "fragile_flag" not in df.columns:
        # False = not fragile by default in this prototype
        df["fragile_flag"] = False

    # Orientation rules: "any", "upright_only", "flat_only", etc.
    if "orientation" not in df.columns:
        df["orientation"] = "any"

    # Parcel ID: use provided ID if present, otherwise synthesize a simple one.
    if "parcel_id" not in df.columns:
        df["parcel_id"] = [f"PARCEL_{i:03d}" for i in range(len(df))]
    # ---------- Fit / no-fit check (bounds only, demo) ----------
    # We treat (x, y, z) as the origin corner of the parcel inside the locker.
    # A parcel "fits" if its full box is within the locker dimensions.
    df["fits_bounds"] = (
        (df["x"] >= 0)
        & (df["y"] >= 0)
        & (df["z"] >= 0)
        & (df["x"] + df["width"]  <= locker_w)
        & (df["y"] + df["depth"]  <= locker_d)
        & (df["z"] + df["height"] <= locker_h)
    )

        # ---------- Summary metrics ----------
    st.subheader("Parcel physics summary (demo)")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Parcels", len(df))

    with col2:
        st.metric("Avg weight (kg)", f'{df["weight_kg"].mean():.2f}')

    with col3:
        st.metric(
            "Avg max top load (kg)",
            f'{df["max_top_load_kg"].mean():.2f}'
        )


    # ---------- Fit / no-fit summary ----------
    total_parcels = len(df)
    fit_count = int(df["fits_bounds"].sum())
    not_fit_count = total_parcels - fit_count

    st.subheader("Fit / no-fit summary (bounds only, demo)")
    st.write(f"Parcels fully inside locker: **{fit_count} / {total_parcels}**")

    if not_fit_count > 0:
        st.error(
            f"{not_fit_count} parcel(s) extend beyond the locker bounds "
            "based on current dimensions and placeholder positions."
        )
    else:
        st.success(
            "All parcels are fully inside the locker bounds for this configuration."
        )

    # ---------- Parcel data model preview ----------
    with st.expander("Show parcel data sample (schema v1.0)", expanded=False):

        cols_to_show = [
            "parcel_id",
            "width", "depth", "height",
            "volume_m3",
            "weight_kg", "max_top_load_kg",
            "stackable_flag", "fragile_flag", "orientation",
        ]
        # Only keep columns that actually exist (in case of future changes)
        cols_to_show = [c for c in cols_to_show if c in df.columns]
        st.dataframe(df[cols_to_show].head(10))

    # ---------- Baseline Matplotlib scatter ----------
    st.subheader("Baseline 3D scatter (parcel centers)")
    st.caption("Each dot is a parcel center inside the locker volume. Axes scale with locker dimensions.")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(df["x"], df["y"], df["z"], s=10)
    ax.set_xlabel("x (W)")
    ax.set_ylabel("y (D)")
    ax.set_zlabel("z (H)")
    ax.set_xlim(0, locker_w)
    ax.set_ylim(0, locker_d)
    ax.set_zlim(0, locker_h)
    st.pyplot(fig)

     # ---------- Plotly 3D boxes ----------
    st.subheader("Plotly 3D boxes (parcels)")
    st.caption("Transparent boxes represent parcel volumes. This view helps spot wasted space.")
    st.markdown(
        "_Stackability rule (demo): parcels with height ≤ 40% of the current locker "
        "height are treated as **stackable** and shown in **green**. Others are "
        "shown in **red** as non-stackable._"
    )

    show_boxes = st.checkbox("Show parcels as 3D boxes", value=True)
    show_only_fit = st.checkbox("Show only parcels that fit (bounds-only)", value=False)

    if show_boxes:
        df_plot = df.copy()
        # st.write(df_plot.columns.tolist())
        # Normalize dimension column names (so plotting code can use w/d/h consistently)
        rename_map = {}
        if "w" not in df_plot.columns and "width" in df_plot.columns:
            rename_map["width"] = "w"
        if "d" not in df_plot.columns and "depth" in df_plot.columns:
            rename_map["depth"] = "d"
        if "h" not in df_plot.columns and "height" in df_plot.columns:
            rename_map["height"] = "h"

        if rename_map:
            df_plot = df_plot.rename(columns=rename_map)
        
        # If user wants only parcels that fit, filter here
        if show_only_fit and "fits_bounds" in df_plot.columns:
            df_plot = df_plot[df_plot["fits_bounds"]]

        # Normalize stackable flag
        if "stackable_flag" in df_plot.columns and "stackable" not in df_plot.columns:
            df_plot["stackable"] = df_plot["stackable_flag"]
        elif "stackable" not in df_plot.columns:
            df_plot["stackable"] = 0

        df_plot["stackable"] = df_plot["stackable"].astype(int)

        fig3d = go.Figure()

        def cuboid_mesh(x, y, z, w, d, h):
            vx = [x, x+w, x+w, x,   x, x+w, x+w, x]
            vy = [y, y,   y+d, y+d, y, y,   y+d, y+d]
            vz = [z, z,   z,   z,   z+h, z+h, z+h, z+h]

            i = [0, 0, 0, 1, 1, 2, 4, 4, 4, 5, 5, 6]
            j = [1, 2, 3, 2, 5, 3, 5, 6, 7, 6, 1, 7]
            k = [2, 3, 1, 5, 6, 7, 6, 7, 5, 1, 4, 3]
            return vx, vy, vz, i, j, k

        legend_shown = {"stackable": False, "non_stackable": False}

        for _, r in df_plot.iterrows():
            is_stackable = r["stackable"] == 1
            color = "green" if is_stackable else "red"

            key = "stackable" if is_stackable else "non_stackable"
            name = "Stackable" if is_stackable else "Non-stackable"
            showlegend = not legend_shown[key]
            legend_shown[key] = True

            vx, vy, vz, i, j, k = cuboid_mesh(
                r["x"], r["y"], r["z"],
                r["w"], r["d"], r["h"]
            )

            fig3d.add_trace(
                go.Mesh3d(
                    x=vx, y=vy, z=vz,
                    i=i, j=j, k=k,
                    color=color,
                    opacity=0.55,
                    name=name,
                    showlegend=showlegend,
                )
            )

        fig3d.update_layout(
            scene=dict(
                xaxis=dict(range=[0, locker_w], title="Width"),
                yaxis=dict(range=[0, locker_d], title="Depth"),
                zaxis=dict(range=[0, locker_h], title="Height"),
                aspectmode="data",
            ),
            legend=dict(title="Parcel type"),
            margin=dict(l=0, r=0, t=30, b=0),
        )

        st.plotly_chart(fig3d, use_container_width=True)






def case2_page():
    st.title("AI Case 2 – UD Incident Embeddings Analyzer")
    st.markdown(Path("ai_cases/case2_ud_embeddings_analyzer.md").read_text(encoding="utf-8"))

    analyzer = UDEmbeddingsAnalyzer(n_clusters=4)
    df = analyzer.load("ai_cases/data/ud_incidents_synth.csv")
    df = analyzer.fit()

    st.subheader("Incident Clusters")
    st.dataframe(df[["incident_id", "free_text", "event_type", "cluster"]])

    st.subheader("Semantic Search (find similar incidents)")
    query = st.text_input(
    "Describe an issue (e.g., 'lock wouldn't open at delivery'):",
    key="case2_query"
)
    if query:
        results = analyzer.search(query, top_k=5)
        st.dataframe(results[["incident_id", "free_text", "event_type", "cluster", "similarity"]])

    st.subheader("Suggested Playbooks by Cluster")
    st.dataframe(analyzer.cluster_playbooks())

    st.markdown("---")
    st.caption("The Chain Never Stops • AI Portfolio")


# --- Router ---
if page.startswith("Case 1"):
    case1_page()
else:
    case2_page()

