import numpy as np
import pandas as pd

# 1. Load the raw telemetry data
input_path = r"E:\Data_analyst\cloud_infrastructure\data\raw_cloud_telemetry.csv"
output_path = (
    r"E:\Data_analyst\cloud_infrastructure\data\cleaned_cloud_telemetry.csv"
)

df = pd.read_csv(input_path)

# 2. Convert timestamps and sort chronologically per instance
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values(by=["instance_id", "timestamp"]).reset_index(drop=True)

# 3. Time dimensions (needed for Power BI / SQL date slicing)
df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour
df["day_name"] = df["timestamp"].dt.day_name()
df["is_weekend"] = df["timestamp"].dt.dayofweek.isin([5, 6]).astype(int)

# 4. 24-Hour rolling averages (CPU and Memory)
df["rolling_cpu_24h_avg"] = (
    df.groupby("instance_id")["cpu_utilization_pct"]
    .transform(lambda x: x.rolling(24, min_periods=1).mean())
    .round(2)
)

df["rolling_ram_24h_avg"] = (
    df.groupby("instance_id")["memory_utilization_pct"]
    .transform(lambda x: x.rolling(24, min_periods=1).mean())
    .round(2)
)

# 5. FinOps: Zombie / Idle server detection (rolling CPU < 5%)
df["is_idle_zombie"] = (df["rolling_cpu_24h_avg"] < 5.0).astype(int)
df["wasted_cost_usd"] = np.where(
    df["is_idle_zombie"] == 1, df["hourly_cost_usd"], 0.0
)

# 6. Service Health Classification
conditions = [
    (df["p95_latency_ms"] > 1000)
    | (df["http_5xx_errors"] > 15)
    | (df["memory_utilization_pct"] > 90),
    (df["p95_latency_ms"] > 400) | (df["cpu_utilization_pct"] > 80),
]
df["health_status"] = np.select(
    conditions, ["Critical", "Degraded"], default="Healthy"
)

# 7. SLA Breach Flag (Latency > 500ms OR 5xx errors > 5)
df["sla_breached"] = (
    (df["p95_latency_ms"] > 500) | (df["http_5xx_errors"] > 5)
).astype(int)

# 8. Save cleaned data for Power BI / Analysis
df.to_csv(output_path, index=False)
print("Pipeline finished successfully. Output saved to:", output_path)

# Quick sanity check print
print("\n--- Project Quick Summary ---")
print(f"Total Records : {len(df):,}")
print(f"Total Spend   : ${df['hourly_cost_usd'].sum():,.2f}")
print(f"Wasted Spend  : ${df['wasted_cost_usd'].sum():,.2f}")
print(f"SLA Breaches  : {df['sla_breached'].sum():,}")
