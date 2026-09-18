"""
03_load_to_sqlite.py
Builds an enterprise Star Schema (Facts and Dimensions) in SQLite
and populates tables from the cleaned telemetry dataset.
"""

import sqlite3
import pandas as pd
import os

def build_star_schema_and_load(
    csv_path=r"E:\Data_analyst\cloud_infrastructure\data\cleaned_cloud_telemetry.csv",
    db_path=r"E:\Data_analyst\cloud_infrastructure\data\cloud_telemetry.db"
):
    print(f"Connecting to database at: {db_path}")
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    df = pd.read_csv(csv_path)
    
    # 1. Dimension: dim_instance
    dim_instance = df[[
        "instance_id", "service_name", "cloud_provider", "region", 
        "environment", "instance_type", "vcpus", "ram_gb", "hourly_cost_usd"
    ]].drop_duplicates().reset_index(drop=True)
    
    # 2. Dimension: dim_service
    service_teams = {
        "auth-service": ("Core Platform", "Tier-1 Mission Critical"),
        "payment-gateway": ("FinTech & Billing", "Tier-1 Mission Critical"),
        "catalog-api": ("Retail Experience", "Tier-2 Business Operational"),
        "recommendation-engine": ("Data Science / ML", "Tier-2 Business Operational"),
        "notification-worker": ("Communications", "Tier-3 Supporting"),
        "orders-db": ("Database Ops", "Tier-1 Mission Critical"),
        "search-service": ("Search & Discovery", "Tier-2 Business Operational"),
        "ml-experiments": ("Data Science / ML", "Tier-4 Non-Production"),
        "qa-testing": ("Quality Assurance", "Tier-4 Non-Production"),
        "legacy-sync": ("Enterprise Migration", "Tier-4 Non-Production")
    }
    
    services_list = []
    for svc in df["service_name"].unique():
        team, tier = service_teams.get(svc, ("Engineering", "Tier-2 Operational"))
        services_list.append({
            "service_name": svc,
            "owner_team": team,
            "criticality_tier": tier
        })
    dim_service = pd.DataFrame(services_list)
    
    # 3. Dimension: dim_date
    df["dt"] = pd.to_datetime(df["timestamp"])
    unique_dates = pd.DataFrame({"date": df["dt"].dt.date.unique()})
    unique_dates["date"] = pd.to_datetime(unique_dates["date"])
    dim_date = pd.DataFrame({
        "date_key": unique_dates["date"].dt.strftime("%Y%m%d").astype(int),
        "full_date": unique_dates["date"].dt.strftime("%Y-%m-%d"),
        "year": unique_dates["date"].dt.year,
        "month": unique_dates["date"].dt.month,
        "month_name": unique_dates["date"].dt.month_name(),
        "day": unique_dates["date"].dt.day,
        "day_name": unique_dates["date"].dt.day_name(),
        "is_weekend": unique_dates["date"].dt.dayofweek.isin([5, 6]).astype(int)
    })
    
    # 4. Fact Table: fact_cloud_telemetry
    df["date_key"] = df["dt"].dt.strftime("%Y%m%d").astype(int)
    fact_telemetry = df[[
        "timestamp", "date_key", "instance_id", "service_name", 
        "cpu_utilization_pct", "memory_utilization_pct", "rolling_cpu_24h_avg", "rolling_ram_24h_avg",
        "network_io_mb", "p95_latency_ms", "request_count", "http_5xx_errors",
        "hourly_cost_usd", "wasted_cost_usd", "is_idle_zombie", "sla_breached", "health_status"
    ]]
    
    # Save to SQLite tables
    print("Writing tables to SQLite...")
    dim_instance.to_sql("dim_instance", conn, index=False)
    dim_service.to_sql("dim_service", conn, index=False)
    dim_date.to_sql("dim_date", conn, index=False)
    fact_telemetry.to_sql("fact_cloud_telemetry", conn, index=False)
    
    # Create Indexes for fast querying
    cursor.execute("CREATE INDEX idx_fact_instance ON fact_cloud_telemetry(instance_id);")
    cursor.execute("CREATE INDEX idx_fact_date ON fact_cloud_telemetry(date_key);")
    cursor.execute("CREATE INDEX idx_fact_service ON fact_cloud_telemetry(service_name);")
    conn.commit()
    conn.close()
    
    print("SUCCESS: SQLite database populated with Star Schema.")
    print(f" - dim_instance:        {len(dim_instance)} records")
    print(f" - dim_service:         {len(dim_service)} records")
    print(f" - dim_date:            {len(dim_date)} records")
    print(f" - fact_cloud_telemetry:{len(fact_telemetry):,} records")

if __name__ == "__main__":
    build_star_schema_and_load()
