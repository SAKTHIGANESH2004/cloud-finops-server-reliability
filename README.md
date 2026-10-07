# ☁️ Enterprise Cloud FinOps & Infrastructure Reliability Analytics Platform
### *An End-to-End Analytics Suite: Python Simulation ETL ➔ SQL Star Schema ➔ Excel FinOps ➔ Power BI Observability*

[![Python Pipeline](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](python/)
[![SQL Star Schema](https://img.shields.io/badge/SQL-Star_Schema-CC292B?style=for-the-badge&logo=postgresql&logoColor=white)](sql/)
[![Power BI Report](https://img.shields.io/badge/POWER_BI-3_PAGE_EXECUTIVE_REPORT-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](Power_bi/Enterprise_Cloud_FinOps_PowerBI_Report.pdf)
[![Excel FinOps](https://img.shields.io/badge/Excel-Financial_What--If_Model-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)](excel/cloud_finops_capacity_model.xlsx)
[![Live Interactive Dashboard](https://img.shields.io/badge/LIVE_DEMO-EXCEL_ONLINE_DASHBOARD-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)](https://1drv.ms/x/c/8603EE4E860307AB/IQD6yuCEn6UARpHHvkH9hklAASLiAYWIPlWbj1hwGuz5rls?e=a05bir)
[![Domain: FinOps](https://img.shields.io/badge/Domain-Cloud_FinOps_&_APM-0EA5E9?style=for-the-badge)](https://www.finops.org/)

> An end-to-end enterprise Data Analytics platform powered by a **custom Python telemetry simulation engine** that models **17,292 hourly multi-cloud logs (AWS CloudWatch & Azure Monitor patterns)** across a 60-day billing cycle to detect idle compute cost leakage, diagnose memory leak anomalies, and model FinOps cost recovery.

---

## 👨‍💻 Project Author
* **Author:** **SAKTHIGANESH K**
* **Education:** B.E. Computer Science & Engineering (2025)
* **Role Focus:** Associate Data Analyst | Business Intelligence & Cloud Analytics
* **Links:** [LinkedIn Profile](https://www.linkedin.com) | [GitHub Portfolio](https://github.com/SAKTHIGANESH2004) | [Email](mailto:sakthiganeshk27@gmail.com)

---

## 📂 Quick Access to Project Source Code & Models

Click any asset below to directly view the source code, raw data, and dashboards in this repository:

| Module | Core Deliverable | Direct Repository Link (Click to Open) |
| :--- | :--- | :--- |
| 🗃️ **Raw & Cleaned Dataset** | 17,292-Row Full CSV Telemetry Data | [📁 `excel/cleaned_cloud_finops_data.csv`](excel/cleaned_cloud_finops_data.csv) |
| 🐍 **Python ETL & Data Pipeline** | Synthetic telemetry generator & EDA cleaning | [📁 `python/`](python/) |
| 🗄️ **SQL Modeling & Queries** | Star Schema DDL, Cost Leakage & RCA Queries | [📁 `sql/`](sql/) |
| 📊 **Power BI Visual Report** | 3-Page Executive Dark-Mode PDF Report | [📑 View Power BI Report (PDF)](power_bi/Enterprise_Cloud_FinOps_PowerBI_Report.pdf) |
| 📈 **Power BI Model File** | Raw Power BI Data Model File | [💾 Download `Cloud_Enterprise_FinOps.pbix`](Cloud_Enterprise_FinOps.pbix) |
| 📑 **Excel Financial Model** | 3-Page What-If Capacity Model (.xlsx) | [📊 Download `excel/cloud_finops_capacity_model.xlsx`](excel/cloud_finops_capacity_model.xlsx) |
| 🌐 **Live Cloud Demo** | Interactive Web Browser Dashboard | [🚀 Launch Excel Online Interactive Dashboard](https://1drv.ms/x/c/8603EE4E860307AB/IQDrQR2m8Y1HR76VquE5YVwGASKdlwENcyOvX0_FDv-EEQE?e=UhFmj2) |

---

## 🧪 Telemetry Generation Methodology (Python Simulation Engine)

To replicate enterprise cloud environments without violating corporate NDAs or PII data privacy, a custom Python pipeline (`python/01_generate_telemetry_data.py`) was engineered to simulate realistic multi-cloud infrastructure behaviors:

* **Diurnal Traffic Curves:** Realistic daytime peak loads and nighttime drops modeled with sine-wave mathematical variations.
* **Zombie Server Simulation:** Non-production instances idling continuously at <5% CPU/RAM across 60 days.
* **Memory Leak Injection:** An escalating heap allocation pattern in `payment-gateway` (45% to 95% RAM saturation) triggering automated container crash-restarts and 5xx cascading failures.
* **Multi-Cloud Billing Math:** Accurate AWS On-Demand vs. Reserved Instance (RI) hourly blended pricing models.

---

## 📌 Executive Summary & Business Impact

Modern enterprise multi-cloud environments suffer from severe capital waste due to unmonitored non-production infrastructure and unhandled cascading microservice latency bottlenecks. 

This analytical platform models **17,292 hourly logs** across AWS and Azure infrastructure over a 60-day billing cycle:

* **💰 Total 60-Day Fleet Spend:** **$2,998.72**
* **🚨 Identified Cloud Waste:** **$1,279.61** (42.7% of total budget wasted on idle workloads)
* **🧟 Zombie Servers Identified:** **3 Unutilized Development Servers** running 24/7 with zero productive traffic.
* **📈 Addressable Annual Cost Recovery:** **$19,067 / Year** via automated decommissioning, staging rightsizing, and 1-Year Reserved Instances (RI).
* **⚡ SRE Outage Triaging:** Diagnosed an unhandled **Heap Memory Leak in `payment-gateway`** causing a 993-hour SLA breach and **14,702 HTTP 5xx error spikes** on AWS Production.

---

## 🏗️ Technical Architecture & Pipeline

```
  ┌─────────────────────────────────┐
  │  17,292 Multi-Cloud Server Logs │  (Synthetic Simulation: AWS EC2 & Azure VMs)
  └────────────────┬────────────────┘
                   │
                   ▼  [Python ETL: Pandas & NumPy]
  ┌─────────────────────────────────┐
  │   Data Cleansing & Outliers     │  (Imputation, Datetime Splitting, Telemetry Normalization)
  └────────────────┬────────────────┘
                   │
                   ▼  [Relational SQL & Star Schema]
  ┌─────────────────────────────────┐
  │  Fact & Dimension Data Modeling │  (Fact_Telemetry, Dim_Server, Dim_Service, Dim_Date)
  └────────────────┬────────────────┘
                   │
          ┌────────┴────────┐
          ▼                 ▼
  ┌───────────────┐ ┌───────────────┐
  │   Microsoft   │ │   Power BI    │
  │   Excel 365   │ │   Desktop     │
  │ (What-If ROI) │ │ (Dark APM UI) │
  └───────────────┘ └───────────────┘
```

---

## 📊 Analytical Deep Dive (3 Core Modules)

### 1️⃣ Module 1: Executive FinOps Overview
* **Donut Fleet Distribution:** Analyzed $2,070.72 AWS vs. $928.00 Azure infrastructure spend.
* **Environment Cost Bleed:** Uncovered that the **Development environment bled 100% of its budget ($1,280.00)** with <3% CPU utilization.
* **60-Day Daily Burn Rate:** Tracked steady $50/day fleet spend with an elevated $21.31/day waste bleed line.

### 2️⃣ Module 2: Application Performance Monitoring (APM) & SRE Observability
* **Microservice SLA Compliance:** Flagged `payment-gateway` (80% compliance) and `recommendation-engine` (50% compliance) breaching enterprise 99.9% uptime targets.
* **Memory Leak Sawtooth Pattern:** Isolated an escalating memory consumption pattern from 45% up to 95% RAM saturation triggering automated container crash-restarts.
* **Error Outage Concentration:** Isolated 14,702 HTTP 5xx server errors localized exclusively to AWS Production workloads.

### 3️⃣ Module 3: DevOps Zombie Resource Audit & Action Center
* **Action Matrix Breakdown:**
  * ⛔ **TERMINATE NOW:** 3 idle servers (`i-dev-sandbox-ml`, `i-dev-test01`, `vm-dev-legacy01`) recovering **$9,667 / year**.
  * ⚡ **CONVERT TO 1-YR RI:** 3 steady-state production workloads saving **$1,989.29 (32% discount)**.
  * ✔ **KEEP ON-DEMAND:** 6 variable staging & ephemeral notification microservices.

---

## 🗄️ SQL Star Schema Architecture

```sql
-- Fact Table
CREATE TABLE fact_server_telemetry (
    telemetry_id INTEGER PRIMARY KEY,
    date_id INTEGER,
    instance_id TEXT,
    service_id INTEGER,
    cpu_utilization_pct REAL,
    memory_utilization_pct REAL,
    http_5xx_errors INTEGER,
    hourly_cost_usd REAL,
    is_idle_zombie INTEGER,
    wasted_cost_usd REAL,
    sla_breached INTEGER
);
```

---

## 📈 Financial Recovery Levers

```text
+------------------------------------+-------------------+-----------------------+
|  FINOPS OPTIMIZATION LEVER         |  MONTHLY SAVINGS  |  ANNUAL RECOVERED ROI |
+------------------------------------+-------------------+-----------------------+
|  Zombie Dev Server Decommission    |  $805.60 / mo     |  $9,667.20 / yr       |
|  Staging Instance Rightsizing      |  $440.00 / mo     |  $5,280.00 / yr       |
|  Production 1-Year RI Commitments  |  $343.33 / mo     |  $4,120.00 / yr       |
+------------------------------------+-------------------+-----------------------+
|  TOTAL ADDRESSABLE FINOPS SAVINGS  |  $1,588.93 / mo   |  $19,067.20 / YR      |
+------------------------------------+-------------------+-----------------------+
```

---

## 💻 Local Setup & Execution

1. Clone the repository:
   ```bash
   git clone https://github.com/SAKTHIGANESH2004/cloud-finops-server-reliability.git
   ```
2. Navigate into the repository:
   ```bash
   cd cloud-finops-server-reliability
   ```
3. Run Python Data Generation & EDA pipeline:
   ```bash
   python python/01_generate_telemetry_data.py
   python python/02_data_cleaning_eda.py
   ```
4. Open `Cloud_Enterprise_FinOps.pbix` in **Power BI Desktop** or explore `excel/cloud_finops_capacity_model.xlsx` in **Microsoft Excel**.

---

⭐ *If you find this project insightful, please consider starring the repository!*
