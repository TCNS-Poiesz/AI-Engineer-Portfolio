
# AI Engineer Portfolio — Annette

> 30-day sprint to complete **DataCamp AI Engineer Certification**, build **visible portfolio projects**, and align outcomes with **Unattended Delivery JV** and **Digital Component Valorisation (DCV)**.

**Start date:** 2025-09-19 · **Duration:** 30 days

## 📦 Repository Structure
```
AI-Engineer-Portfolio/
├─ projects/
│  ├─ case1-logistics-route-clustering/
│  ├─ case2-dcv-microbiome-study/
│  └─ case3-end-to-end-pipeline/
├─ notebooks/
│  ├─ 01_exploration.ipynb
│  └─ 02_modeling.ipynb
├─ data/            # raw/ interim/ processed/ are gitignored
├─ dashboard/       # optional Streamlit DCV dashboard
├─ api/             # optional FastAPI service for logistics
├─ scripts/         # setup and utility scripts
├─ docs/
│  ├─ ROADMAP-30DAYS.md
│  └─ PORTFOLIO-LOG.md
├─ requirements.txt
├─ Makefile
├─ .gitignore
└─ LICENSE
```

## 🗺️ 30-Day Roadmap (High-Level)
- **Week 1:** Setup + Case 1 kick-off (logistics clustering quick win)
- **Week 2:** Complete Case 1 with write-up & visuals
- **Week 3:** Case 2 — DCV microbiome analysis (InnoGI/InnoGO study)
- **Week 4:** Case 3 — deployment (Streamlit dashboard or FastAPI API)

## 🧰 Environment
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 🚀 Quick Start
- Put any small sample data into `data/raw/` (gitignored).
- Open `notebooks/01_exploration.ipynb` and start exploring.
- Use `Makefile` for common commands (see below).

## 🧪 Makefile Commands
```bash
make setup        # create venv & install deps
make notebook     # launch Jupyter Lab
make dashboard    # run Streamlit app (if using dashboard option)
make api          # run FastAPI (if using API option)
```

## 🧩 Cases
- **Case 1 (Logistics):** `projects/case1-logistics-route-clustering/`
- **Case 2 (DCV):** `projects/case2-dcv-microbiome-study/`
- **Case 3 (Pipeline):** `projects/case3-end-to-end-pipeline/`

Each case includes: problem statement, data, methods, results, next steps.

## 🔗 Visibility
- Keep a weekly post on LinkedIn with visuals and key learnings.
- Update `docs/PORTFOLIO-LOG.md` after each work session.
