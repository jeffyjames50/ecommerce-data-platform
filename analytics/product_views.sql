CREATE OR REPLACE VIEW analytics.product_performance AS

SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.brand,

    SUM(f.quantity) AS units_sold,
    SUM(f.total_amount) AS revenue,
    AVG(f.unit_price) AS average_price

FROM warehouse.fact_orders f

JOIN warehouse.dim_products p
ON f.product_id = p.product_id

GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.brand

ORDER BY revenue DESC;