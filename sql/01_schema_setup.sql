-- ====================================================================
-- 01_schema_setup.sql
-- Star Schema Architecture for Cloud Telemetry & FinOps Analytics
-- ====================================================================

-- 1. Dimension Table: Server Instances
CREATE TABLE IF NOT EXISTS dim_instance (
    instance_id VARCHAR(50) PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    cloud_provider VARCHAR(20) NOT NULL,
    region VARCHAR(30) NOT NULL,
    environment VARCHAR(30) NOT NULL,
    instance_type VARCHAR(30) NOT NULL,
    vcpus INTEGER NOT NULL,
    ram_gb INTEGER NOT NULL,
    hourly_cost_usd DECIMAL(10, 4) NOT NULL
);

-- 2. Dimension Table: Services & Ownership
CREATE TABLE IF NOT EXISTS dim_service (
    service_name VARCHAR(50) PRIMARY KEY,
    owner_team VARCHAR(50) NOT NULL,
    criticality_tier VARCHAR(50) NOT NULL
);

-- 3. Dimension Table: Date / Calendar (Time Intelligence)
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend INTEGER NOT NULL
);

-- 4. Fact Table: Hourly Cloud Telemetry & Metrics
CREATE TABLE IF NOT EXISTS fact_cloud_telemetry (
    telemetry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    date_key INTEGER NOT NULL,
    instance_id VARCHAR(50) NOT NULL,
    service_name VARCHAR(50) NOT NULL,
    cpu_utilization_pct DECIMAL(5, 2),
    memory_utilization_pct DECIMAL(5, 2),
    rolling_cpu_24h_avg DECIMAL(5, 2),
    rolling_ram_24h_avg DECIMAL(5, 2),
    network_io_mb DECIMAL(10, 2),
    p95_latency_ms DECIMAL(10, 2),
    request_count INTEGER,
    http_5xx_errors INTEGER,
    hourly_cost_usd DECIMAL(10, 4),
    wasted_cost_usd DECIMAL(10, 4),
    is_idle_zombie INTEGER,
    sla_breached INTEGER,
    health_status VARCHAR(20),
    FOREIGN KEY (instance_id) REFERENCES dim_instance(instance_id),
    FOREIGN KEY (service_name) REFERENCES dim_service(service_name),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

-- Performance Optimization Indexes
CREATE INDEX IF NOT EXISTS idx_fact_instance ON fact_cloud_telemetry(instance_id);
CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_cloud_telemetry(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_service ON fact_cloud_telemetry(service_name);
