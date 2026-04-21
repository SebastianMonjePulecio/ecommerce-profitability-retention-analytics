-- 1. Net revenue and margin by acquisition channel
SELECT
    c.acquisition_channel,
    SUM(o.quantity * o.unit_price - o.discount_amount) AS gross_revenue,
    SUM(
        CASE
            WHEN o.returned_flag = 1 THEN 0
            ELSE (o.quantity * o.unit_price - o.discount_amount)
        END
    ) AS net_revenue,
    SUM(
        CASE
            WHEN o.returned_flag = 1 THEN -o.shipping_cost
            ELSE (o.quantity * p.unit_cost * -1) - o.shipping_cost
        END
    ) AS cost_impact
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
GROUP BY c.acquisition_channel;

-- 2. Return rate by category
SELECT
    p.category,
    COUNT(*) AS total_order_lines,
    SUM(CASE WHEN o.returned_flag = 1 THEN 1 ELSE 0 END) AS returned_lines,
    ROUND(
        100.0 * SUM(CASE WHEN o.returned_flag = 1 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS return_rate_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY return_rate_pct DESC;

-- 3. Repeat purchase behavior by customer segment
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(quantity * unit_price - discount_amount) AS total_spend
    FROM orders
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN total_spend >= 1200 THEN 'High Value'
        WHEN total_spend >= 600 THEN 'Mid Value'
        ELSE 'Low Value'
    END AS customer_segment,
    COUNT(*) AS customers,
    AVG(order_count) AS avg_orders_per_customer
FROM customer_orders
GROUP BY 1
ORDER BY avg_orders_per_customer DESC;

