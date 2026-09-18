# Power BI FinOps & Server Reliability Dashboard Implementation Guide

This guide gives you the exact blueprint to build a professional, dark-themed **Cloud FinOps & Infrastructure Analytics Dashboard** in Power BI Desktop.

---

## 1. Data Connection & Star Schema Modeling

### Connecting the Data
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Select `E:\Data_analyst\cloud_infrastructure\data\cleaned_cloud_telemetry.csv`.
4. (Optional Alternative) You can also connect directly to SQLite or export the dimension tables from the database.

### Relationships (Star Schema)
Ensure the following relationships are established in the **Model View**:
* `fact_cloud_telemetry[instance_id]`  -->  `dim_instance[instance_id]` *(Many-to-One, Single direction)*
* `fact_cloud_telemetry[service_name]` -->  `dim_service[service_name]`  *(Many-to-One, Single direction)*
* `fact_cloud_telemetry[date_key]`     -->  `dim_date[date_key]`         *(Many-to-One, Single direction)*

---

## 2. Core DAX Measures Library

Create a new dedicated table in Power BI called `_DAX_Measures` and add these formulas:

### Financial & FinOps Metrics
```dax
-- Total Cloud Fleet Spend ($)
Total Spend = SUM(fact_cloud_telemetry[hourly_cost_usd])

-- Identified Idle / Zombie Server Waste ($)
Identified Waste = SUM(fact_cloud_telemetry[wasted_cost_usd])

-- Net Potential FinOps Savings (%)
Potential Savings Pct = 
DIVIDE([Identified Waste], [Total Spend], 0)

-- Production Spend ($)
Production Spend = 
CALCULATE(
    [Total Spend],
    fact_cloud_telemetry[environment] = "Production"
)

-- Development Waste ($)
Development Waste = 
CALCULATE(
    [Identified Waste],
    fact_cloud_telemetry[environment] = "Development"
)
```

### Fleet Health & Reliability (APM) Metrics
```dax
-- Active Instances Monitored
Monitored Fleet Count = DISTINCTCOUNT(fact_cloud_telemetry[instance_id])

-- Zombie / Idle Instances Count
Zombie Server Count = 
CALCULATE(
    DISTINCTCOUNT(fact_cloud_telemetry[instance_id]),
    fact_cloud_telemetry[is_idle_zombie] = 1
)

-- Overall SLA Compliance % (Target: > 99.0%)
Fleet SLA Compliance = 
1 - DIVIDE(
    SUM(fact_cloud_telemetry[sla_breached]),
    COUNTROWS(fact_cloud_telemetry),
    0
)

-- Average P95 Latency (ms)
Avg P95 Latency = AVERAGE(fact_cloud_telemetry[p95_latency_ms])

-- Total HTTP 5xx Server Errors
Total 5xx Errors = SUM(fact_cloud_telemetry[http_5xx_errors])
```

---

## 3. Dashboard Layout & Page Design (Dark Theme)

**Recommended Theme Colors**:
* Background: `#0F172A` (Slate Dark Navy)
* Card Visuals: `#1E293B`
* Primary Accent (Cyan/Blue): `#06B6D4`
* Warning Accent (Orange/Amber): `#F59E0B`
* Critical/Waste (Crimson/Red): `#EF4444`
* Text: `#F8FAFC`

---

### Page 1: FinOps Executive Cost Overview
* **Top KPI Row (Cards)**:
  1. `[Total Spend]` -> **\$2,998.72**
  2. `[Identified Waste]` -> **\$1,279.61** *(Card Callout formatted in Red)*
  3. `[Potential Savings Pct]` -> **42.7%**
  4. `[Zombie Server Count]` -> **3 Instances**
* **Visual 1 (Donut Chart)**: Spend by Cloud Provider (`AWS` vs. `Azure`).
* **Visual 2 (Stacked Bar Chart)**: Total Spend vs Wasted Spend by `environment` (`Production`, `Staging`, `Development`).
* **Visual 3 (Line & Clustered Column Chart)**: Daily Cloud Spend trend over time with Wasted Spend as shaded area.
* **Slicers (Top Right)**: Date Range slider, Cloud Provider dropdown.

---

### Page 2: APM & Microservice Reliability
* **Top KPI Row (Cards)**:
  1. `[Fleet SLA Compliance]` -> **94.3%**
  2. `[Avg P95 Latency]` -> **103.8 ms**
  3. `[Total 5xx Errors]` -> **14,997**
* **Visual 1 (Clustered Bar Chart)**: SLA Compliance % by `service_name` (instantly highlights `recommendation-engine` at 50.4% and `payment-gateway` at 90.4%).
* **Visual 2 (Line Chart)**: P95 Latency trend over 60 days for `payment-gateway` showing the repeating sawtooth memory leak pattern.
* **Visual 3 (Matrix Heatmap)**: `service_name` vs `hour` (0 to 23) colored by Average CPU Utilization to show diurnal peak bottlenecks.

---

### Page 3: Zombie Resource Decommission Action Center
* **Executive Value**: This page gives the DevOps & Infrastructure teams an immediate checklist to eliminate waste.
* **Main Visual (Interactive Table)**:
  * Columns: `instance_id`, `service_name`, `environment`, `instance_type`, `hourly_cost_usd`, `wasted_cost_usd`, `avg_cpu_pct`.
  * Filter condition on visual: `is_idle_zombie = 1`.
  * Conditional formatting: Wasted Cost highlighted with red data bars.
* **Call-to-Action Box**:
  > *"Decommissioning these 3 idle instances recovers **\$1,279.61 every 60 days** (**\$7,677.66 / year**) with zero impact on production traffic."*
