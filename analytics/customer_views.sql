CREATE OR REPLACE VIEW analytics.customer_summary AS

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.country,

    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.total_amount) AS total_spend,
    AVG(f.total_amount) AS average_order_value,
    MAX(f.order_date) AS last_purchase_date

FROM warehouse.dim_customers c

JOIN warehouse.fact_orders f
ON c.customer_id = f.customer_id

GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.country

ORDER BY total_spend DESC;