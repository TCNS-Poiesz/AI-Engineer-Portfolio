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
    # 1) Rename size columns to expected names
    if {"length_mm", "width_mm", "height_mm"}.issubset(df.columns):
        df = df.rename(
            columns={
                "width_mm": "width",
                "length_mm": "depth",
                "height_mm": "height",
            }
        )
        # Convert mm -> meters  ✅ inside this if
        df[["width", "depth", "height"]] = df[["width", "depth", "height"]] / 1000.0

    # 2) If positions are missing, generate placeholder positions
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

    # ---------- Baseline Matplotlib scatter ----------
    st.subheader("Baseline 3D scatter (parcel centers)")
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
    show_boxes = st.checkbox("Show parcels as 3D boxes", value=True)
    if show_boxes:
        fig3d = go.Figure()

        for _, r in df.iterrows():
            x0, y0, z0 = r["x"], r["y"], r["z"]
            w, d, h = r["width"], r["depth"], r["height"]

            xs = [x0, x0+w, x0+w, x0, x0, x0+w, x0+w, x0]
            ys = [y0, y0, y0+d, y0+d, y0, y0, y0+d, y0+d]
            zs = [z0, z0, z0, z0, z0+h, z0+h, z0+h, z0+h]

            fig3d.add_trace(
                go.Mesh3d(x=xs, y=ys, z=zs, opacity=0.4, alphahull=0)
            )

        fig3d.update_layout(
            scene=dict(
                xaxis=dict(range=[0, locker_w], title="x (W)"),
                yaxis=dict(range=[0, locker_d], title="y (D)"),
                zaxis=dict(range=[0, locker_h], title="z (H)"),
                aspectmode="data",
            ),
            height=650,
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

