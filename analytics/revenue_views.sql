CREATE OR REPLACE VIEW analytics.revenue_summary AS

SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS average_order_value

FROM warehouse.fact_orders

GROUP BY
    DATE_TRUNC('month', order_date)

ORDER BY month;