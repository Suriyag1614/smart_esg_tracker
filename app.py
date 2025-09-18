# app.py
import streamlit as st
import pandas as pd
import src.data_processing as dp
import src.graph_builder as gb
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go

st.set_page_config(page_title="Smart ESG Tracker", layout="wide")
st.title("Smart ESG & Carbon Footprint Tracker (Demo)")

st.sidebar.header("Data")
use_sample = st.sidebar.checkbox("Use sample generated data", value=True)
uploaded_suppliers = st.sidebar.file_uploader("Suppliers CSV", type="csv")
uploaded_shipments = st.sidebar.file_uploader("Shipments CSV", type="csv")

if use_sample or (uploaded_suppliers is None or uploaded_shipments is None):
    suppliers, shipments = dp.load_data("data/suppliers.csv","data/shipments.csv")
else:
    suppliers = pd.read_csv(uploaded_suppliers)
    shipments = pd.read_csv(uploaded_shipments)

# compute emissions
shipments = dp.compute_emissions(shipments)
agg = dp.aggregate_by_supplier(shipments)

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Total Suppliers", int(suppliers.shape[0]))
c2.metric("Total Shipments", int(shipments.shape[0]))
c3.metric("Total Emissions (kg CO2)", f"{shipments['emissions_kg'].sum():,.0f}")

# Top suppliers bar
st.subheader("Top suppliers by emissions")
topn = st.slider("Top N", 3, 20, 8)
fig = px.bar(agg.sort_values("total_emissions_kg", ascending=False).head(topn),
             x="supplier_id", y="total_emissions_kg", labels={"total_emissions_kg":"emissions (kg)"})
st.plotly_chart(fig, use_container_width=True)

# Build graph and show a simple network plot
G = gb.build_supplier_graph(suppliers, shipments)

st.subheader("Supplier -> Shipments network (force layout)")
pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
edge_x = []
edge_y = []
for u,v in G.edges():
    x0,y0 = pos[u]
    x1,y1 = pos[v]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=0.5), hoverinfo='none')

node_x = []
node_y = []
node_text = []
node_size = []
for node, data in G.nodes(data=True):
    x,y = pos[node]
    node_x.append(x); node_y.append(y)
    if data.get("type") == "supplier":
        node_text.append(f"{data.get('name')} ({node})")
        # size by outgoing emissions
        total_em = sum(e["emissions_kg"] for _,_,e in G.out_edges(node, data=True))
        node_size.append(max(8, min(40, total_em/1000 + 8)))
    else:
        node_text.append(node)
        node_size.append(6)

node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text,
                        marker=dict(size=node_size), textposition="top center")

fig_net = go.Figure(data=[edge_trace, node_trace])
fig_net.update_layout(height=500, showlegend=False)
st.plotly_chart(fig_net, use_container_width=True)

# Suggest vendor alternatives (simple)
st.subheader("Suggest lower-emission suppliers for a sample shipment")
sample_ship = shipments.sample(1).iloc[0]
st.write("Selected shipment:", sample_ship.to_dict())

def suggest_alternatives(shipment_row, shipments_df, suppliers_df, top_k=5):
    # compute hypothetical emissions if other suppliers shipped same weight/distance using their avg mode factor
    candidate_suppliers = suppliers_df.copy()
    # choose representative mode to compute using global mean factors
    mode = shipment_row["mode"]
    distance = shipment_row["distance_km"]
    weight = shipment_row["weight_tonnes"]
    # compute per-supplier average emission rate (from their shipments)
    avg_factors = shipments_df.groupby("supplier_id").apply(
        lambda g: (g["emissions_kg"].sum() / (g["distance_km"]*g["weight_tonnes"]).sum()) if (g["distance_km"]*g["weight_tonnes"]).sum()>0 else 0.05
    ).rename("avg_ef").reset_index()
    cand = candidate_suppliers.merge(avg_factors, left_on="supplier_id", right_on="supplier_id", how="left")
    cand["hyp_emissions_kg"] = distance * weight * cand["avg_ef"].fillna(0.05)
    return cand.sort_values("hyp_emissions_kg").head(top_k)

alts = suggest_alternatives(sample_ship, shipments, suppliers, top_k=5)
st.table(alts[["supplier_id","name","country","avg_ef","hyp_emissions_kg"]])
