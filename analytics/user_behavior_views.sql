CREATE OR REPLACE VIEW analytics.user_behavior_summary AS

SELECT
    event_type,

    COUNT(*) AS total_events,

    COUNT(DISTINCT customer_id) AS unique_customers,

    COUNT(DISTINCT product_id) AS unique_products

FROM warehouse.fact_user_events

GROUP BY
    event_type

ORDER BY total_events DESC;