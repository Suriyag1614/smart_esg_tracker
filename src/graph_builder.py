# src/graph_builder.py
import networkx as nx
import pandas as pd

def build_supplier_graph(suppliers_df, shipments_df):
    G = nx.DiGraph()
    # add supplier nodes
    for _, r in suppliers_df.iterrows():
        G.add_node(r["supplier_id"], type="supplier", name=r["name"], lat=r["lat"], lon=r["lon"])

    # add edges supplier -> destination (as a node per shipment destination or a dest_id)
    for _, sh in shipments_df.iterrows():
        src = sh["supplier_id"]
        dst = f"DEST_{sh['shipment_id']}"
        G.add_node(dst, type="destination", lat=sh["dest_lat"], lon=sh["dest_lon"])
        G.add_edge(src, dst, shipment_id=sh["shipment_id"],
                   mode=sh["mode"], distance_km=sh["distance_km"],
                   weight_tonnes=sh["weight_tonnes"], emissions_kg=sh["emissions_kg"])
    return G

def supplier_risk_scores(G):
    scores = {}
    for n, d in G.nodes(data=True):
        if d.get("type") == "supplier":
            # risk heuristic: total emissions from outgoing edges + avg lead time (if available)
            total_em = sum(e["emissions_kg"] for _, _, e in G.out_edges(n, data=True))
            # normalize (simple)
            scores[n] = {"total_emissions_kg": total_em, "risk": min(1.0, total_em/10000)}
    return scores
