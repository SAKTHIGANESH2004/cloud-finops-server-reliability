import os
import sqlite3
import pandas as pd

# Paths
csv_path = (
    r"E:\Data_analyst\cloud_infrastructure\data\cleaned_cloud_telemetry.csv"
)
db_path = r"E:\Data_analyst\cloud_infrastructure\data\cloud_telemetry.db"

# Reset database if it already exists (start clean)
if os.path.exists(db_path):
    os.remove(db_path)

print(f"[*] Reading cleaned telemetry data from: {csv_path}")
df = pd.read_csv(csv_path)
df["dt"] = pd.to_datetime(df["timestamp"])
df["date_key"] = df["dt"].dt.strftime("%Y%m%d").astype(int)

# -------------------------------------------------------------
# 1. Dimension Table: dim_instance (Hardware & Specs)
# -------------------------------------------------------------
dim_instance = df[
    [
        "instance_id",
        "service_name",
        "cloud_provider",
        "region",
        "environment",
        "instance_type",
        "vcpus",
        "ram_gb",
        "hourly_cost_usd",
    ]
].drop_duplicates().reset_index(drop=True)

# -------------------------------------------------------------
# 2. Dimension Table: dim_service (Team Ownership & Tier)
# -------------------------------------------------------------
service_mapping = {
    "auth-service": ("Core Platform", "Tier-1 Mission Critical"),
    "payment-gateway": ("FinTech & Billing", "Tier-1 Mission Critical"),
    "catalog-api": ("Retail Experience", "Tier-2 Business Operational"),
    "recommendation-engine": (
        "Data Science / ML",
        "Tier-2 Business Operational",
    ),
    "notification-worker": ("Communications", "Tier-3 Supporting"),
    "orders-db": ("Database Ops", "Tier-1 Mission Critical"),
    "search-service": ("Search & Discovery", "Tier-2 Business Operational"),
    "ml-experiments": ("Data Science / ML", "Tier-4 Non-Production"),
    "qa-testing": ("Quality Assurance", "Tier-4 Non-Production"),
    "legacy-sync": ("Enterprise Migration", "Tier-4 Non-Production"),
}

services_data = []
for svc in df["service_name"].unique():
    team, tier = service_mapping.get(
        svc, ("General Engineering", "Tier-2 Operational")
    )
    services_data.append(
        {"service_name": svc, "owner_team": team, "criticality_tier": tier}
    )
dim_service = pd.DataFrame(services_data)

# -------------------------------------------------------------
# 3. Dimension Table: dim_date (Time Intelligence)
# -------------------------------------------------------------
unique_dates = pd.to_datetime(df["dt"].dt.date.unique())
dim_date = pd.DataFrame(
    {
        "date_key": unique_dates.strftime("%Y%m%d").astype(int),
        "full_date": unique_dates.strftime("%Y-%m-%d"),
        "year": unique_dates.year,
        "month": unique_dates.month,
        "month_name": unique_dates.strftime("%B"),
        "day": unique_dates.day,
        "day_name": unique_dates.strftime("%A"),
        "is_weekend": unique_dates.dayofweek.isin([5, 6]).astype(int),
    }
).sort_values("date_key")

# -------------------------------------------------------------
# 4. Fact Table: fact_cloud_telemetry (Metrics & Costs)
# -------------------------------------------------------------
fact_telemetry = df[
    [
        "timestamp",
        "date_key",
        "instance_id",
        "service_name",
        "cpu_utilization_pct",
        "memory_utilization_pct",
        "rolling_cpu_24h_avg",
        "rolling_ram_24h_avg",
        "network_io_mb",
        "p95_latency_ms",
        "request_count",
        "http_5xx_errors",
        "hourly_cost_usd",
        "wasted_cost_usd",
        "is_idle_zombie",
        "sla_breached",
        "health_status",
    ]
]

# -------------------------------------------------------------
# 5. Load into SQLite & Build Indexes
# -------------------------------------------------------------
print("[*] Writing Star Schema to SQLite...")
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    dim_instance.to_sql("dim_instance", conn, index=False)
    dim_service.to_sql("dim_service", conn, index=False)
    dim_date.to_sql("dim_date", conn, index=False)
    fact_telemetry.to_sql("fact_cloud_telemetry", conn, index=False)

    # Creating B-Tree indexes on foreign keys for fast dashboard joins
    cursor.execute(
        "CREATE INDEX idx_fact_instance ON fact_cloud_telemetry(instance_id);"
    )
    cursor.execute(
        "CREATE INDEX idx_fact_date ON fact_cloud_telemetry(date_key);"
    )
    cursor.execute(
        "CREATE INDEX idx_fact_service ON fact_cloud_telemetry(service_name);"
    )

print("\n[+] Star Schema loaded successfully!")
print(f"    - dim_instance        : {len(dim_instance):,} records")
print(f"    - dim_service         : {len(dim_service):,} records")
print(f"    - dim_date            : {len(dim_date):,} records")
print(f"    - fact_cloud_telemetry: {len(fact_telemetry):,} records")
