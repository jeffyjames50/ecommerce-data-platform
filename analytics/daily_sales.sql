CREATE OR REPLACE VIEW analytics.daily_sales AS
SELECT
    order_date,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units,
    SUM(quantity * unit_price) AS revenue
FROM warehouse.fact_orders
GROUP BY order_date
ORDER BY order_date;