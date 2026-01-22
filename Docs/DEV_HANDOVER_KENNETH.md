# DEV_HANDOVER_KENNETH.md

## 1. Purpose of This Branch

This branch (`checkpoint/docs-option-b`) is a **development-first workspace**.

It exists to:
- Explore **algorithmic space allocation logic** (X parcels → Y spaces)
- Make system behavior **visible** (fit vs non-fit, reasons)
- Invite **targeted technical feedback** before formalizing the model

This branch is **not** optimized for external stakeholders.
For a stable narrative / review version, see `master`.

Feedback requested here:
- Algorithmic approach
- Data structures
- Constraint modeling
- Clarity of outputs (especially failure cases)

---

## 2. Conceptual Goal (Non-Code)

We are modeling:

> **X parcels → Y available spaces**

Where:
- Parcels differ in dimensions, weight, destination, and route context
- Spaces differ in size, accessibility, and constraints
- Not all parcels will fit — and that is *expected*

Key design principle:
> **Non-fit parcels are first-class outcomes**, not errors.

Each non-fit parcel should clearly communicate:
- *Why* it didn’t fit
- *Which constraint failed*
- *Whether alternative placement might exist*

This mirrors real-world last-mile and unattended delivery constraints.

---

## 3. How to Run Locally (Streamlit)

### Requirements
- Python 3.10+
- Virtual environment recommended

### Setup
```bash
git checkout checkpoint/docs-option-b
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
If you are on Windows, activate the virtual environment using one of the following:

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bat
.venv\Scripts\activate.bat
```
