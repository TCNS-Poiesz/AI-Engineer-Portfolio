# AI Case 2 — UD Incident Embeddings Analyzer (MVP)

**case_id:** "002"  
**title:** "UD Incident Embeddings Analyzer (MVP)"  
**domain:** "Last-Mile Logistics / Unattended Delivery"  
**organization:** "The Chain Never Stops (TCNS)"  
**status:** Prototype / MVP  
**date_created:** 2025-11-28  
**version:** v1.0  
**authors:** Annette Poiès  
**collaborators:** TCNS Engineering, Kenneth (3D Space Optimization)

---

## 1. Problem / Opportunity

Unattended Delivery (UD) operations generate many incident reports in free text (driver notes, customer complaints, lock events).  
These reports are:

- **Unstructured and inconsistent**
- **Hard to triage quickly**
- **Difficult to learn from at scale**
- **Not systematically linked to playbooks**

As UD volume grows, manual incident triage becomes a bottleneck.  
TCNS needs a way to convert messy operational text into **structured, learnable intelligence**.

---

## 2. Goal of This MVP

Build a lightweight analyzer that:

1. **Clusters similar incidents** automatically  
2. Enables **semantic search** to find incidents like a new query  
3. Suggests **playbooks by cluster** to speed resolution  
4. Provides a clear baseline before upgrading to OpenAI embeddings

---

## 3. Data

**Source:** Synthetic incident dataset  
**File:** `ai_cases/data/ud_incidents_synth.csv`

**Columns:**
- `incident_id`
- `free_text`
- `event_type`
- (derived) `cluster`

**Why synthetic?**  
This MVP is designed to validate the pipeline without exposing production incident data.  
The same structure will later accept real incidents.

---

## 4. Baseline Model (Current Implementation)

**Model v1 (Offline Baseline):**
- **Vectorizer:** TF-IDF (English stopwords removed)
- **Clustering:** KMeans (`n_clusters=4`)
- **Similarity:** Cosine similarity over TF-IDF vectors

**Reasoning:**  
TF-IDF + KMeans is fast, transparent, and easy to debug.  
It provides a clean **reference baseline** for later comparison with OpenAI embeddings.

---

## 5. System / Pipeline

1. **Load incidents** from CSV  
2. **Vectorize free text** with TF-IDF  
3. **Cluster incidents** via KMeans  
4. **Display cluster table** for inspection  
5. **Semantic search:**  
   - user enters a new incident description  
   - system returns top-k similar incidents with clusters  
6. **Playbooks:**  
   - clusters map to suggested resolution actions  

---

## 6. Demo Output (Screenshots)

> Add your screenshots here after saving them in `ai_cases/assets/`

### 6.1 Incident Clusters Table
![Incident clusters](assets/case2_incident_clusters.png)

### 6.2 Semantic Search (Top-k similar incidents)
![Semantic search](assets/case2_semantic_search.png)

### 6.3 Suggested Playbooks by Cluster
![Playbooks](assets/case2_playbooks.png)

---

## 7. Results / Early Insight

Even with a simple baseline, the system:

- Groups incidents into **logical operational themes**
  (e.g., lock access issues, space fit problems, navigation barriers)
- Enables **fast recall of similar incidents** from free text
- Provides a first version of **cluster-level playbooks**
- Demonstrates how UD operations can become **self-learning over time**

---

## 8. Relevance for TCNS

This approach supports TCNS’s goal to valorize the digital component of UD operations by:

- Reducing time-to-resolution for incidents  
- Creating a feedback loop between operations and product design  
- Turning incident text into actionable intelligence  
- Scaling UD without scaling manual support cost  

---

## 9. Roadmap / Next Iteration

**Upgrade v2: OpenAI embeddings**
- Replace TF-IDF with OpenAI text embeddings  
- Re-cluster and compare coherence vs baseline  
- Add simple evaluation:
  - silhouette score  
  - manual cluster label check  
- Expand dataset to real incidents when permitted

**Potential add-ons**
- Auto-label clusters with LLM summaries  
- Track cluster drift over time  
- Recommend *next best action* rather than static playbooks  
- Integrate with TCNS dashboards (Power BI / internal ops console)

---

## 10. Repo / Code References

- **Analyzer:** `ai_cases/ud_embeddings_analyzer.py`  
- **Streamlit app:** `case_viewer.py`  
- **Dataset:** `ai_cases/data/ud_incidents_synth.csv`

---

## 11. One-Line Summary

A practical MVP that turns UD incident free-text into **clusters, semantic search, and playbooks**, creating a strong baseline for a future OpenAI-embedding powered self-learning ops layer.
