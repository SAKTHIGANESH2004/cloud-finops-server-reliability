"""
02_data_cleaning_eda.py
Performs automated ETL, data validation, rolling time-series calculations,
and engineering anomaly detection on cloud telemetry logs.
"""

import pandas as pd
import numpy as np
import os

def clean_and_engineer_telemetry(
    input_path=r"E:\Data_analyst\cloud_infrastructure\data\raw_cloud_telemetry.csv",
    output_path=r"E:\Data_analyst\cloud_infrastructure\data\cleaned_cloud_telemetry.csv"
):
    print("Loading raw cloud telemetry data...")
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df):,} records.")
    
    # 1. Parse Datetime & Sort Chronologically
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by=["instance_id", "timestamp"]).reset_index(drop=True)
    
    # 2. Extract Calendar & Time Dimensions (Useful for SQL & Power BI Time Intelligence)
    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour
    df["day_name"] = df["timestamp"].dt.day_name()
    df["is_weekend"] = df["timestamp"].dt.dayofweek.isin([5, 6]).astype(int)
    
    # 3. Rolling 24-Hour Time-Series Metrics (Smooths out diurnal peaks)
    print("Calculating rolling 24-hour moving averages...")
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
    
    # 4. FinOps Waste Detection (Zombie / Idle Server Classifier)
    # Industry standard FinOps rule: CPU consistently under 5% over 24+ hours
    df["is_idle_zombie"] = (df["rolling_cpu_24h_avg"] < 5.0).astype(int)
    df["wasted_cost_usd"] = np.where(df["is_idle_zombie"] == 1, df["hourly_cost_usd"], 0.0)
    
    # 5. Reliability & SLA Breach Classification
    # Critical: Latency > 1000ms OR 5xx errors > 15 OR RAM > 90%
    # Degraded: Latency 400-1000ms OR CPU > 80%
    # Healthy: Normal operations
    conditions = [
        (df["p95_latency_ms"] > 1000) | (df["http_5xx_errors"] > 15) | (df["memory_utilization_pct"] > 90),
        (df["p95_latency_ms"] > 400) | (df["cpu_utilization_pct"] > 80)
    ]
    choices = ["Critical", "Degraded"]
    df["health_status"] = np.select(conditions, choices, default="Healthy")
    
    # SLA Breach Flag: SLA defined as P95 Latency < 500ms and 5xx errors <= 5
    df["sla_breached"] = ((df["p95_latency_ms"] > 500) | (df["http_5xx_errors"] > 5)).astype(int)
    
    # 6. Save Cleaned Dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved successfully to: {output_path}")
    
    # 7. Executive EDA Insights & Business Impact Summary
    total_spend = df["hourly_cost_usd"].sum()
    total_waste = df["wasted_cost_usd"].sum()
    waste_pct = (total_waste / total_spend) * 100
    total_breaches = df["sla_breached"].sum()
    total_5xx = df["http_5xx_errors"].sum()
    
    print("\n" + "="*50)
    print("      EXECUTIVE FINOPS & RELIABILITY SUMMARY      ")
    print("="*50)
    print(f"Total Fleet Monitored:         {df['instance_id'].nunique()} instances")
    print(f"Total Cloud Spend (60 Days):   ${total_spend:,.2f}")
    print(f"Identified FinOps Waste:       ${total_waste:,.2f} ({waste_pct:.1f}% of total bill!)")
    print(f"Total SLA Breaches:            {total_breaches:,} hours ({total_breaches/len(df)*100:.1f}%)")
    print(f"Total HTTP 5xx Server Errors:  {total_5xx:,}")
    print("="*50)
    
    # Breakdown by instance
    print("\nInstance-level Waste & Health Breakdown:")
    inst_summary = df.groupby("instance_id").agg(
        service=("service_name", "first"),
        env=("environment", "first"),
        total_spend=("hourly_cost_usd", "sum"),
        wasted_spend=("wasted_cost_usd", "sum"),
        avg_cpu=("cpu_utilization_pct", "mean"),
        max_ram=("memory_utilization_pct", "max"),
        sla_breaches=("sla_breached", "sum")
    ).reset_index()
    print(inst_summary.to_string(index=False))

if __name__ == "__main__":
    clean_and_engineer_telemetry()
