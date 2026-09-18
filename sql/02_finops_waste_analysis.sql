-- ====================================================================
-- 02_finops_waste_analysis.sql
-- Advanced FinOps Analytics Queries: Idle Server Waste & Cost Leakage
-- ====================================================================

-- --------------------------------------------------------------------
-- QUERY 1: Fleet Cost & Waste Breakdown by Environment
-- Business Goal: Show leadership how much cloud spend is wasted in Dev vs Prod
-- --------------------------------------------------------------------
SELECT 
    i.environment,
    COUNT(DISTINCT i.instance_id) AS total_instances,
    ROUND(SUM(f.hourly_cost_usd), 2) AS total_spend_usd,
    ROUND(SUM(f.wasted_cost_usd), 2) AS total_waste_usd,
    ROUND((SUM(f.wasted_cost_usd) * 100.0 / SUM(f.hourly_cost_usd)), 2) AS waste_percentage,
    ROUND(AVG(f.cpu_utilization_pct), 2) AS avg_cpu_utilization
FROM fact_cloud_telemetry f
JOIN dim_instance i ON f.instance_id = i.instance_id
GROUP BY i.environment
ORDER BY total_waste_usd DESC;


-- --------------------------------------------------------------------
-- QUERY 2: Top Zombie Resources (Ranked by Financial Drain)
-- Demonstrates: CTEs (Common Table Expressions) and Window Functions (DENSE_RANK)
-- Business Goal: Generate actionable hit-list for DevOps to immediately terminate
-- --------------------------------------------------------------------
WITH InstanceWasteSummary AS (
    SELECT 
        f.instance_id,
        i.service_name,
        i.cloud_provider,
        i.environment,
        i.instance_type,
        i.hourly_cost_usd,
        ROUND(SUM(f.hourly_cost_usd), 2) AS total_cost_60d,
        ROUND(SUM(f.wasted_cost_usd), 2) AS wasted_cost_60d,
        ROUND(AVG(f.cpu_utilization_pct), 2) AS avg_cpu_pct,
        SUM(f.is_idle_zombie) AS total_idle_hours
    FROM fact_cloud_telemetry f
    JOIN dim_instance i ON f.instance_id = i.instance_id
    GROUP BY f.instance_id, i.service_name, i.cloud_provider, i.environment, i.instance_type, i.hourly_cost_usd
)
SELECT 
    DENSE_RANK() OVER (ORDER BY wasted_cost_60d DESC) AS waste_rank,
    instance_id,
    service_name,
    environment,
    instance_type,
    total_idle_hours,
    total_cost_60d,
    wasted_cost_60d,
    ROUND((wasted_cost_60d * 100.0 / total_cost_60d), 1) AS waste_ratio_pct
FROM InstanceWasteSummary
WHERE wasted_cost_60d > 0
ORDER BY waste_rank;


-- --------------------------------------------------------------------
-- QUERY 3: Unit Economics - Cost Per 1 Million Requests
-- Demonstrates: Cross-table joins with service metadata and unit economics
-- Business Goal: Measure true software operational efficiency across services
-- --------------------------------------------------------------------
SELECT 
    s.owner_team,
    f.service_name,
    SUM(f.request_count) AS total_requests,
    ROUND(SUM(f.hourly_cost_usd), 2) AS total_cost_usd,
    ROUND((SUM(f.hourly_cost_usd) * 1000000.0 / NULLIF(SUM(f.request_count), 0)), 2) AS cost_per_million_requests
FROM fact_cloud_telemetry f
JOIN dim_service s ON f.service_name = s.service_name
GROUP BY s.owner_team, f.service_name
ORDER BY cost_per_million_requests DESC;


-- --------------------------------------------------------------------
-- QUERY 4: Daily Spend Trend & Day-over-Day Cost Variance
-- Demonstrates: Window Function LAG() to detect unexpected billing jumps
-- --------------------------------------------------------------------
WITH DailySpend AS (
    SELECT 
        d.full_date,
        ROUND(SUM(f.hourly_cost_usd), 2) AS daily_spend,
        ROUND(SUM(f.wasted_cost_usd), 2) AS daily_waste
    FROM fact_cloud_telemetry f
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY d.full_date
)
SELECT 
    full_date,
    daily_spend,
    daily_waste,
    LAG(daily_spend, 1) OVER (ORDER BY full_date) AS prev_day_spend,
    ROUND(daily_spend - LAG(daily_spend, 1) OVER (ORDER BY full_date), 2) AS dod_spend_change
FROM DailySpend
LIMIT 15;
