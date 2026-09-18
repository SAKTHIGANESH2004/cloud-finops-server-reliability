"""
01_generate_telemetry_data.py
Simulates enterprise cloud telemetry logs modeled after AWS CloudWatch and Cost & Usage Reports (CUR).
Generates 17,000+ hourly records spanning 60 days with embedded IT anomalies (Zombie instances, memory leaks, latency spikes).
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

# Set seed for 100% reproducibility across all runs
np.random.seed(42)

def generate_cloud_telemetry(num_days=60, output_path=r"E:\Data_analyst\cloud_infrastructure\data\raw_cloud_telemetry.csv"):
    print(f"Generating {num_days} days of hourly cloud telemetry and FinOps metrics...")
    
    end_date = datetime(2026, 9, 7, 0, 0)
    start_date = end_date - timedelta(days=num_days)
    date_range = pd.date_range(start=start_date, end=end_date, freq='h')
    
    # Enterprise server fleet configuration
    instances = [
        # Production - Mission Critical
        {"id": "i-prod-auth01", "provider": "AWS", "region": "us-east-1", "env": "Production", "service": "auth-service", "type": "c5.xlarge", "vcpus": 4, "ram": 8, "cost": 0.170, "behavior": "normal_high_load"},
        {"id": "i-prod-pay01", "provider": "AWS", "region": "us-east-1", "env": "Production", "service": "payment-gateway", "type": "m5.xlarge", "vcpus": 4, "ram": 16, "cost": 0.192, "behavior": "memory_leak"},
        {"id": "i-prod-cat01", "provider": "AWS", "region": "us-west-2", "env": "Production", "service": "catalog-api", "type": "t3.large", "vcpus": 2, "ram": 8, "cost": 0.083, "behavior": "normal_steady"},
        {"id": "i-prod-rec01", "provider": "AWS", "region": "us-east-1", "env": "Production", "service": "recommendation-engine", "type": "c5.xlarge", "vcpus": 4, "ram": 8, "cost": 0.170, "behavior": "cpu_spikes"},
        {"id": "i-prod-notif01", "provider": "AWS", "region": "ap-south-1", "env": "Production", "service": "notification-worker", "type": "t3.medium", "vcpus": 2, "ram": 4, "cost": 0.042, "behavior": "normal_steady"},
        {"id": "vm-prod-db01", "provider": "Azure", "region": "eastus", "env": "Production", "service": "orders-db", "type": "Standard_E4s_v5", "vcpus": 4, "ram": 32, "cost": 0.260, "behavior": "normal_steady"},
        {"id": "vm-prod-search01", "provider": "Azure", "region": "eastus", "env": "Production", "service": "search-service", "type": "Standard_D4s_v5", "vcpus": 4, "ram": 16, "cost": 0.192, "behavior": "normal_steady"},
        
        # Staging & Pre-production
        {"id": "i-stg-pay01", "provider": "AWS", "region": "us-east-1", "env": "Staging", "service": "payment-gateway", "type": "t3.medium", "vcpus": 2, "ram": 4, "cost": 0.042, "behavior": "low_traffic"},
        {"id": "i-stg-auth01", "provider": "AWS", "region": "us-east-1", "env": "Staging", "service": "auth-service", "type": "t3.medium", "vcpus": 2, "ram": 4, "cost": 0.042, "behavior": "low_traffic"},
        
        # Development / Sandbox (Embedded FinOps Zombie / Waste Anomalies)
        {"id": "i-dev-sandbox-ml", "provider": "AWS", "region": "us-east-1", "env": "Development", "service": "ml-experiments", "type": "r5.2xlarge", "vcpus": 8, "ram": 64, "cost": 0.504, "behavior": "zombie_idle"},
        {"id": "i-dev-test01", "provider": "AWS", "region": "us-west-2", "env": "Development", "service": "qa-testing", "type": "m5.xlarge", "vcpus": 4, "ram": 16, "cost": 0.192, "behavior": "zombie_idle"},
        {"id": "vm-dev-legacy01", "provider": "Azure", "region": "eastus", "env": "Development", "service": "legacy-sync", "type": "Standard_D4s_v5", "vcpus": 4, "ram": 16, "cost": 0.192, "behavior": "zombie_idle"}
    ]
    
    records = []
    
    for inst in instances:
        behavior = inst["behavior"]
        leak_ram_baseline = 42.0
        leak_cycle_counter = 0
        
        for hour_idx, ts in enumerate(date_range):
            hour_of_day = ts.hour
            is_peak = 10 <= hour_of_day <= 21
            diurnal_mult = 1.35 if is_peak else 0.70
            
            # Scenario 1: Zombie / Idle Instance (FinOps Waste)
            if behavior == "zombie_idle":
                cpu = np.clip(np.random.normal(2.5, 0.8), 0.5, 4.5)
                ram = np.clip(np.random.normal(8.0, 1.2), 5.0, 12.0)
                requests = int(np.clip(np.random.normal(15, 8), 0, 40))
                latency = round(float(np.clip(np.random.normal(25, 5), 15, 45)), 2)
                errors_5xx = 0
                net_io = round(float(np.clip(np.random.normal(5, 2), 1, 12)), 2)
                
            # Scenario 2: Memory Leak (Reliability & Latency Spikes)
            elif behavior == "memory_leak":
                leak_cycle_counter += 1
                current_ram = leak_ram_baseline + (leak_cycle_counter * 0.18)
                
                # Server auto-restart trigger at 92% RAM
                if current_ram >= 92.0:
                    leak_cycle_counter = 0
                    current_ram = leak_ram_baseline
                    cpu = 88.0 + float(np.random.uniform(2, 8))
                    errors_5xx = int(np.random.uniform(45, 120))
                    latency = round(float(np.random.uniform(1400, 2400)), 2)
                else:
                    cpu = float(np.clip(np.random.normal(48 * diurnal_mult, 8), 20, 85))
                    lat_base = 120 if current_ram < 75 else (120 + (current_ram - 75) * 20)
                    latency = round(float(np.clip(np.random.normal(lat_base, 25), 60, 1800)), 2)
                    errors_5xx = int(np.random.poisson(lam=1 if current_ram < 80 else 8))
                
                ram = round(float(np.clip(current_ram, 30, 99)), 2)
                requests = int(np.clip(np.random.normal(1200 * diurnal_mult, 150), 300, 2500))
                net_io = round(float(np.clip(np.random.normal(180 * diurnal_mult, 30), 40, 350)), 2)

            # Scenario 3: CPU Bottlenecks during peak hours
            elif behavior == "cpu_spikes":
                if is_peak:
                    cpu = round(float(np.clip(np.random.normal(88, 6), 72, 98)), 2)
                    ram = round(float(np.clip(np.random.normal(78, 5), 65, 90)), 2)
                    latency = round(float(np.clip(np.random.normal(480, 80), 250, 950)), 2)
                    errors_5xx = int(np.random.poisson(lam=12))
                else:
                    cpu = round(float(np.clip(np.random.normal(42, 6), 25, 60)), 2)
                    ram = round(float(np.clip(np.random.normal(55, 4), 45, 68)), 2)
                    latency = round(float(np.clip(np.random.normal(160, 20), 100, 260)), 2)
                    errors_5xx = int(np.random.poisson(lam=1))
                requests = int(np.clip(np.random.normal(1600 * diurnal_mult, 200), 400, 3000))
                net_io = round(float(np.clip(np.random.normal(250 * diurnal_mult, 40), 60, 450)), 2)

            # Scenario 4: Production High Load Steady
            elif behavior == "normal_high_load":
                cpu = round(float(np.clip(np.random.normal(52 * diurnal_mult, 7), 25, 75)), 2)
                ram = round(float(np.clip(np.random.normal(58, 4), 45, 70)), 2)
                latency = round(float(np.clip(np.random.normal(85, 15), 45, 180)), 2)
                requests = int(np.clip(np.random.normal(2800 * diurnal_mult, 350), 800, 4500))
                errors_5xx = int(np.random.poisson(lam=0.4))
                net_io = round(float(np.clip(np.random.normal(320 * diurnal_mult, 45), 90, 600)), 2)

            # Scenario 5: Normal Steady / Dev Baseline
            else:
                base_cpu = 38 if behavior == "normal_steady" else 15
                base_ram = 45 if behavior == "normal_steady" else 28
                base_req = 950 if behavior == "normal_steady" else 180
                
                cpu = round(float(np.clip(np.random.normal(base_cpu * diurnal_mult, 5), 10, 65)), 2)
                ram = round(float(np.clip(np.random.normal(base_ram, 3), 15, 60)), 2)
                latency = round(float(np.clip(np.random.normal(70, 12), 35, 140)), 2)
                requests = int(np.clip(np.random.normal(base_req * diurnal_mult, 40), 30, 1800))
                errors_5xx = int(np.random.poisson(lam=0.1))
                net_io = round(float(np.clip(np.random.normal(90 * diurnal_mult, 15), 15, 220)), 2)

            records.append({
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "instance_id": inst["id"],
                "cloud_provider": inst["provider"],
                "region": inst["region"],
                "environment": inst["env"],
                "service_name": inst["service"],
                "instance_type": inst["type"],
                "vcpus": inst["vcpus"],
                "ram_gb": inst["ram"],
                "hourly_cost_usd": inst["cost"],
                "cpu_utilization_pct": round(float(cpu), 2),
                "memory_utilization_pct": round(float(ram), 2),
                "network_io_mb": float(net_io),
                "p95_latency_ms": float(latency),
                "request_count": int(requests),
                "http_5xx_errors": int(errors_5xx)
            })

    df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"SUCCESS: Generated {len(df):,} records saved to {output_path}")

if __name__ == "__main__":
    generate_cloud_telemetry()
