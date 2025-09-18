# src/data_processing.py
import pandas as pd

# example factors (kg CO2 per tonne-km) — replace with official factors for real reports
DEFAULT_FACTORS = {
    "road": 0.062,   # 62 g / tkm -> 0.062 kg/tkm (example)
    "rail": 0.021,
    "sea": 0.010,
    "air": 0.600
}

def load_data(suppliers_path, shipments_path):
    suppliers = pd.read_csv(suppliers_path)
    shipments = pd.read_csv(shipments_path)
    return suppliers, shipments

def compute_emissions(shipments_df, factors=DEFAULT_FACTORS):
    df = shipments_df.copy()
    df["ef"] = df["mode"].map(factors).fillna(0.05)
    # emissions in kgCO2 = distance_km * weight_tonnes * ef (kg/tkm)
    df["emissions_kg"] = df["distance_km"] * df["weight_tonnes"] * df["ef"]
    return df

def aggregate_by_supplier(shipments_with_emissions):
    agg = shipments_with_emissions.groupby("supplier_id").agg(
        total_shipments = ("shipment_id","count"),
        total_weight_t = ("weight_tonnes","sum"),
        total_emissions_kg = ("emissions_kg","sum"),
        avg_distance_km = ("distance_km","mean")
    ).reset_index()
    return agg

if __name__ == "__main__":
    s, sh = load_data("data/suppliers.csv","data/shipments.csv")
    sh2 = compute_emissions(sh)
    print(aggregate_by_supplier(sh2).head())
