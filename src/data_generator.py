# src/data_generator.py
import pandas as pd
import numpy as np
import random
from math import radians, sin, cos, asin, sqrt
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data"
OUT.mkdir(exist_ok=True)

def haversine(lat1, lon1, lat2, lon2):
    # returns km
    R = 6371.0
    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2*asin(sqrt(a))
    return R*c

def gen_suppliers(n=12):
    suppliers = []
    base = (20.5, 78.9)  # centre roughly India for variety; you can change
    for i in range(n):
        lat = base[0] + random.uniform(-10, 10)
        lon = base[1] + random.uniform(-25, 25)
        suppliers.append({
            "supplier_id": f"S{i+1:03}",
            "name": f"Supplier {chr(65+i)}",
            "country": random.choice(["India","China","Germany","US","Brazil"]),
            "lat": lat, "lon": lon,
            "avg_lead_days": random.randint(2, 45)
        })
    pd.DataFrame(suppliers).to_csv(OUT/"suppliers.csv", index=False)
    return pd.DataFrame(suppliers)

def gen_shipments(suppliers, m=80):
    shipments = []
    for j in range(m):
        s = suppliers.sample(1).iloc[0]
        dest_lat = s["lat"] + random.uniform(-3, 3)
        dest_lon = s["lon"] + random.uniform(-3, 3)
        distance = round(haversine(s["lat"], s["lon"], dest_lat, dest_lon), 2)
        weight = round(random.uniform(0.1, 20.0), 2)  # tonnes
        mode = random.choices(["road","rail","sea","air"], weights=[50,20,20,10])[0]
        shipments.append({
            "shipment_id": f"SH{j+1:04}",
            "supplier_id": s["supplier_id"],
            "origin_lat": s["lat"], "origin_lon": s["lon"],
            "dest_lat": dest_lat, "dest_lon": dest_lon,
            "distance_km": distance,
            "weight_tonnes": weight,
            "mode": mode
        })
    pd.DataFrame(shipments).to_csv(OUT/"shipments.csv", index=False)
    return pd.DataFrame(shipments)

if __name__ == "__main__":
    suppliers = gen_suppliers()
    gen_shipments(suppliers)
    print("Generated data in data/ (suppliers.csv, shipments.csv)")
