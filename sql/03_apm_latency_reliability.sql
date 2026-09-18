-- ====================================================================
-- 03_apm_latency_reliability.sql
-- Application Performance Monitoring (APM) & Reliability Queries
-- ====================================================================

-- --------------------------------------------------------------------
-- QUERY 1: Service SLA Compliance & Health Scorecard
-- SLA Target: P95 Latency < 500ms AND 5xx Server Errors <= 5 / hr
-- --------------------------------------------------------------------
SELECT 
    f.service_name,
    s.owner_team,
    s.criticality_tier,
    COUNT(*) AS total_hours_monitored,
    SUM(f.sla_breached) AS sla_breach_hours,
    ROUND((1.0 - (SUM(f.sla_breached) * 1.0 / COUNT(*))) * 100.0, 2) AS sla_compliance_pct,
    ROUND(AVG(f.p95_latency_ms), 1) AS avg_p95_latency_ms,
    MAX(f.p95_latency_ms) AS peak_latency_ms,
    SUM(f.http_5xx_errors) AS total_5xx_errors
FROM fact_cloud_telemetry f
JOIN dim_service s ON f.service_name = s.service_name
GROUP BY f.service_name, s.owner_team, s.criticality_tier
ORDER BY sla_compliance_pct ASC;


-- --------------------------------------------------------------------
-- QUERY 2: Rolling 6-Hour Latency Smoother (Window Functions)
-- Demonstrates: Moving average using ROWS BETWEEN to detect degrading trends
-- --------------------------------------------------------------------
SELECT 
    timestamp,
    instance_id,
    service_name,
    p95_latency_ms,
    ROUND(AVG(p95_latency_ms) OVER (
        PARTITION BY instance_id 
        ORDER BY timestamp 
        ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_latency_6h,
    http_5xx_errors
FROM fact_cloud_telemetry
WHERE service_name = 'payment-gateway' AND instance_id = 'i-prod-pay01'
ORDER BY timestamp DESC
LIMIT 20;


-- --------------------------------------------------------------------
-- QUERY 3: Outage Risk Matrix - High Memory & CPU Saturation
-- Business Goal: Identify instances at risk of OOM (Out Of Memory) crashes
-- --------------------------------------------------------------------
SELECT 
    f.instance_id,
    i.service_name,
    i.environment,
    ROUND(AVG(f.cpu_utilization_pct), 2) AS avg_cpu_pct,
    ROUND(MAX(f.cpu_utilization_pct), 2) AS max_cpu_pct,
    ROUND(AVG(f.memory_utilization_pct), 2) AS avg_ram_pct,
    ROUND(MAX(f.memory_utilization_pct), 2) AS max_ram_pct,
    SUM(CASE WHEN f.memory_utilization_pct > 85.0 THEN 1 ELSE 0 END) AS hours_critical_memory,
    SUM(f.http_5xx_errors) AS total_5xx_errors
FROM fact_cloud_telemetry f
JOIN dim_instance i ON f.instance_id = i.instance_id
WHERE i.environment = 'Production'
GROUP BY f.instance_id, i.service_name, i.environment
ORDER BY hours_critical_memory DESC;
