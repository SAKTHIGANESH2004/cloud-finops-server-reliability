# ☁️ Multi-Cloud FinOps & Infrastructure Reliability Analytics Engine

[![Live Interactive Dashboard](https://img.shields.io/badge/LIVE_DEMO-EXCEL_ONLINE_DASHBOARD-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)](https://1drv.ms/x/c/8603EE4E860307AB/IQDrQR2m8Y1HR76VquE5YVwGASKdlwENcyOvX0_FDv-EEQE?e=UhFmj2)
[![Domain: FinOps](https://img.shields.io/badge/Domain-Cloud_FinOps_&_APM-0EA5E9?style=for-the-badge)](https://www.finops.org/)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Database: SQLite Star Schema](https://img.shields.io/badge/Database-SQLite_Star_Schema-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)

> An end-to-end enterprise Data Analytics platform powered by a **custom Python telemetry simulation engine** that models **17,292 hourly multi-cloud logs (AWS CloudWatch & Azure Monitor patterns)** across a 60-day billing cycle to detect idle compute cost leakage, diagnose memory leak anomalies, and model FinOps cost recovery.

---

## 👤 Project Author
* **Author:** **SAKTHIGANESH K**
* **Education:** B.E. Computer Science & Engineering (2025)
* **Role Focus:** Associate Data Analyst | Business Intelligence & Cloud Analytics
* **Links:** [GitHub Portfolio](https://github.com/SAKTHIGANESH2004) | [Email](mailto:sakthiganeshk27@gmail.com)

---

## 🚀 Quick Access to Project Source Code & Models

| Module | Core Deliverable | Direct Repository Link |
| :--- | :--- | :--- |
| 📊 **Cleaned Dataset** | 17,292-Row Telemetry Data | [`excel/cleaned_cloud_finops_data.csv`](excel/cleaned_cloud_finops_data.csv) |
| 🐍 **Python ETL Pipeline** | Telemetry generator & Data Cleaning | [`python/`](python/) |
| 🗄️ **SQL Modeling & Queries** | Star Schema DDL, Cost Leakage & RCA Queries | [`sql/`](sql/) |
| 📑 **Power BI Visual Report** | 3-Page Executive Dark-Mode PDF Report | [View Power BI Report (PDF)](Power_bi/Enterprise_Cloud_FinOps_PowerBI_Report.pdf) |
| 📈 **Excel Financial Model** | 3-Page What-If Capacity Model (.xlsx) | [`excel/cloud_finops_capacity_model.xlsx`](excel/cloud_finops_capacity_model.xlsx) |
| 🌐 **Live Cloud Demo** | Interactive Web Browser Dashboard | [Launch Excel Online Interactive Dashboard](https://1drv.ms/x/c/8603EE4E860307AB/IQDrQR2m8Y1HR76VquE5YVwGASKdlwENcyOvX0_FDv-EEQE?e=UhFmj2) |

---

## ⚙️ Telemetry Generation Methodology (Python Simulation Engine)

To replicate enterprise cloud environments without violating corporate NDAs or PII data privacy, a custom Python pipeline (`python/01_generate_telemetry_data.py`) was engineered to simulate realistic multi-cloud infrastructure behaviors:

* **Diurnal Traffic Curves:** Realistic daytime peak loads and nighttime drops modeled with sine-wave mathematical variations.
* **Zombie Server Simulation:** Non-production instances idling continuously at <5% CPU/RAM across 60 days.
* **Memory Leak Injection:** An escalating heap allocation pattern in `payment-gateway` (45% to 95% RAM saturation) triggering automated container crash-restarts and 5xx cascading failures.
* **Multi-Cloud Billing Math:** Accurate AWS On-Demand vs. Reserved Instance (RI) hourly blended pricing models.

---

## 📊 Executive Summary & Business Impact

Modern enterprise multi-cloud environments suffer from severe capital waste due to unmonitored non-production infrastructure and unhandled cascading microservice latency bottlenecks. 

This analytical platform models **17,292 hourly logs** across AWS and Azure infrastructure over a 60-day billing cycle:

* 💰 **Total 60-Day Fleet Spend:** **$2,998.72**
* 📉 **Identified Cloud Waste:** **$1,279.61** (42.7% of total budget wasted on idle workloads)
* 🧟 **Zombie Servers Identified:** **3 Unutilized Development Servers** running 24/7 with zero productive traffic.
* 💵 **Addressable Annual Cost Recovery:** **$19,067 / Year** via automated decommissioning, staging rightsizing, and 1-Year Reserved Instances (RI).
* 🚨 **SRE Outage Triaging:** Diagnosed an unhandled **Heap Memory Leak in `payment-gateway`** causing a 993-hour SLA breach and **14,702 HTTP 5xx error spikes** on AWS Production.

---

## 🏗️ Technical Architecture & Pipeline

```text
+-------------------------------------------------------------------+
|     17,292 Multi-Cloud Server Logs (AWS EC2 & Azure VMs)          |
+-------------------------------------------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|                  Python Data Pipeline (Pandas & NumPy)            |
|   • Timestamp normalization & time dimension extraction           |
|   • 24-Hour rolling baseline averages (groupby().transform())     |
|   • Zombie detection (<5% CPU) & vectorized SLA health tagging    |
+-------------------------------------------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|               Relational Star Schema (SQLite Database)            |
|   • Fact Table: fact_cloud_telemetry                              |
|   • Dimension Tables: dim_instance, dim_service, dim_date         |
|   • B-Tree Indexes on Foreign Keys (instance_id, date_key)       |
+-------------------------------------------------------------------+
                                  │
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
+-----------------------------------+ +-----------------------------+
|        Microsoft Excel 365        | |      Power BI Desktop       |
|    • What-If ROI Capacity Model   | |   • Dark APM Observability  |
|    • FinOps Recovery Matrix       | |   • SLA Health Scorecard    |
+-----------------------------------+ +-----------------------------+
