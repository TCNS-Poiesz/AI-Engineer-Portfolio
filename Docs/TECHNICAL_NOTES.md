# Technical Notes (Option B)

## Goal
This portfolio demonstrates applied AI engineering through explicit constraint-based reasoning,
simulation-friendly data models, and explainable decision support.

## Scope (current)
- Streamlit UI for exploring cases
- Parcel schema + derived physics (demo-safe fallbacks)
- Fit/no-fit evaluation against locker constraints
- 3D visualization of placements (inspection-first)

## Non-goals (current)
- Production-grade optimization solver
- Real-time telemetry ingestion
- Lock integration (future)
- ML model training (future)

## Why rules first (before ML)
- Constraints are explicit and auditable
- Easier to validate and debug than opaque models
- Sets up future ML as an assistant layer, not a replacement

## Roadmap
1. Stabilize schemas & validation
2. Add reproducible datasets & scenarios
3. Introduce optimization baseline (heuristic / ILP / CP-SAT)
4. Add embeddings-based incident playback (case 2)
5. Add CI + tests + packaging for collaboration
