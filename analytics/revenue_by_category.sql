CREATE OR REPLACE VIEW analytics.revenue_by_category AS
SELECT
    p.category,
    SUM(f.quantity * f.unit_price) AS revenue,
    SUM(f.quantity) AS units_sold
FROM warehouse.fact_orders f
JOIN warehouse.dim_products p
    ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;
