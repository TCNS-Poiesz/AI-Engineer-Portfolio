# AI Case Viewer (TCNS Portfolio)

This repository contains a small, hands-on AI engineering portfolio focused on
**constraint-based reasoning, decision support, and digital twin concepts**
applied to logistics and operations.

The core artifact is a **Streamlit-based Case Viewer** that demonstrates how
real operational constraints can be translated into data models, simulations,
and explainable visual outcomes.

---

## What problem this explores

In real-world operations (e.g. logistics, infrastructure, access systems),
many decisions are still made manually under time pressure, despite being
highly constrained and data-rich.

This project explores:
- How physical and operational constraints can be modeled explicitly
- How spatial problems can be inspected and validated visually
- How AI-assisted tools can support human decision-making without black-box ML

---

## Included case: Unattended Delivery – Space Optimization

The first case models parcel placement inside constrained locker volumes.

It demonstrates:
- 3D spatial reasoning
- Explicit geometry and collision constraints
- Rule-based handling logic (stackability, fragility, orientation)
- Visual validation of “fit / no-fit” decisions

This reflects real challenges observed in last-mile and unattended delivery
operations.

---

## Technical approach (intentionally scoped)

- Python-based data modeling and simulation
- Streamlit for fast, inspectable visualization
- Explicit rules and constraints instead of opaque optimization
- Designed for clarity, extensibility, and reviewability

This is **not a production system**, but a technically honest exploration of
how such systems can be designed.

---

## Quickstart

```bash
pip install -r requirements.txt
streamlit run case_viewer.py
