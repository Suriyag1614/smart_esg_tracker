# 🌍 Smart ESG & Carbon Footprint Tracker

An end-to-end sustainability analytics project that tracks supplier emissions, visualizes carbon hotspots in the supply chain, and suggests lower-emission vendor alternatives.  

✅ **Why it matters:** ESG reporting & carbon reduction are top priorities for global firms.  
✅ **What it shows:** Skills in **Python, Graph Analytics, Neo4j, Streamlit, Data Visualization, and Prescriptive Analytics**.  

---

## 🚀 Features
- **Data Ingestion & Processing**  
  - Load supplier + shipment datasets (CSV).  
  - Compute CO₂ emissions per shipment using mode-based emission factors.  
  - Aggregate supplier emissions and identify high-impact vendors.  

- **Graph Analytics**  
  - Build a directed supplier → shipment network with **NetworkX**.  
  - Compute risk scores per supplier (emissions + lead time).  
  - (Optional) Push graph to **Neo4j** for advanced querying.  

- **Interactive Dashboard** (Streamlit)  
  - KPIs: total suppliers, shipments, emissions.  
  - Bar chart of top suppliers by emissions (Plotly).  
  - Force-layout supplier graph visualization.  
  - Suggested lower-emission vendor alternatives for sample shipments.  

- **Free & Open Source Stack**  
  - Data Processing → `pandas`, `numpy`  
  - Graph → `networkx`, `neo4j` (optional)  
  - Visualization → `plotly`, `streamlit`  
  - Hosting → Streamlit Community Cloud (free deployment)  

---

## ⚙️ Setup & Run Locally
1. Clone repo & create virtual env:
   ```
   git clone https://github.com/your-username/smart-esg-tracker.git
   cd smart-esg-tracker
   python -m venv .venv
   source .venv/bin/activate   # (Windows: .venv\Scripts\activate)

2. Install dependencies:
  ```
  pip install -r requirements.txt
  ```
3. Generate sample data:
  ```
  python src/data_generator.py
  ```

4. Run Streamlit app:
  ```
  streamlit run app.py
  ```

## 🌐 Deployment

Deploy free on Streamlit Community Cloud:

- Push repo to GitHub.

- Connect Streamlit Cloud to your repo.

- Set entrypoint as:
  ```
  streamlit run app.py
  ```

- Add .env in secrets for Neo4j (if used).

## 📊 Dashboard

[Click Here](https://smart-esg-tracker.streamlit.app/) to view the stremlit deployment
