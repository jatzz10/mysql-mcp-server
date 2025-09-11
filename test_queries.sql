-- Sample queries to test the MySQL MCP Server
-- These queries demonstrate various capabilities of the MCP server

-- 1. Basic user queries
SELECT 'Basic User Queries' as section;

-- Get all active users
SELECT username, email, first_name, last_name, age, created_at 
FROM users 
WHERE is_active = 1 
ORDER BY created_at DESC 
LIMIT 5;

-- Count users by age group
SELECT 
    CASE 
        WHEN age < 25 THEN 'Under 25'
        WHEN age BETWEEN 25 AND 35 THEN '25-35'
        WHEN age BETWEEN 36 AND 45 THEN '36-45'
        WHEN age > 45 THEN 'Over 45'
        ELSE 'Unknown'
    END as age_group,
    COUNT(*) as user_count
FROM users 
WHERE is_active = 1 
GROUP BY age_group 
ORDER BY user_count DESC;

-- 2. Product and category queries
SELECT 'Product and Category Queries' as section;

-- Products with their categories
SELECT p.name, p.price, c.name as category, p.stock_quantity
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.is_available = 1
ORDER BY p.price DESC
LIMIT 10;

-- Category hierarchy
SELECT 
    c1.name as parent_category,
    c2.name as subcategory,
    COUNT(p.id) as product_count
FROM categories c1
LEFT JOIN categories c2 ON c1.id = c2.parent_id
LEFT JOIN products p ON c2.id = p.category_id
WHERE c1.parent_id IS NULL
GROUP BY c1.id, c1.name, c2.id, c2.name
ORDER BY c1.name, c2.name;

-- 3. Order analysis
SELECT 'Order Analysis Queries' as section;

-- Recent orders with user details
SELECT 
    o.id as order_id,
    u.username,
    u.email,
    o.total_amount,
    o.status,
    o.order_date,
    COUNT(oi.id) as item_count
FROM orders o
JOIN users u ON o.user_id = u.id
LEFT JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, u.username, u.email, o.total_amount, o.status, o.order_date
ORDER BY o.order_date DESC
LIMIT 10;

-- Order status summary
SELECT 
    status,
    COUNT(*) as order_count,
    AVG(total_amount) as avg_amount,
    SUM(total_amount) as total_revenue
FROM orders
GROUP BY status
ORDER BY order_count DESC;

-- 4. Complex analytical queries
SELECT 'Analytical Queries' as section;

-- Top customers by total spending
SELECT 
    u.username,
    u.email,
    COUNT(o.id) as total_orders,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status != 'cancelled'
GROUP BY u.id, u.username, u.email
HAVING total_orders > 0
ORDER BY total_spent DESC
LIMIT 5;

-- Product performance analysis
SELECT 
    p.name,
    p.price,
    COUNT(oi.id) as times_ordered,
    SUM(oi.quantity) as total_quantity_sold,
    SUM(oi.quantity * oi.unit_price) as total_revenue
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id AND o.status != 'cancelled'
GROUP BY p.id, p.name, p.price
ORDER BY total_revenue DESC
LIMIT 10;

-- 5. JSON data queries (MySQL 5.7+)
SELECT 'JSON Data Queries' as section;

-- Extract user preferences
SELECT 
    username,
    JSON_EXTRACT(profile_data, '$.preferences.theme') as theme_preference,
    JSON_EXTRACT(profile_data, '$.preferences.notifications') as notifications_enabled,
    JSON_EXTRACT(profile_data, '$.bio') as bio
FROM users
WHERE profile_data IS NOT NULL
LIMIT 5;

-- Product metadata analysis
SELECT 
    name,
    price,
    JSON_EXTRACT(metadata, '$.brand') as brand,
    JSON_EXTRACT(metadata, '$.color') as color,
    JSON_EXTRACT(metadata, '$.storage') as storage
FROM products
WHERE metadata IS NOT NULL
AND JSON_EXTRACT(metadata, '$.brand') IS NOT NULL
LIMIT 5;

-- 6. Time-based queries
SELECT 'Time-based Queries' as section;

-- User registration trends (by month)
SELECT 
    DATE_FORMAT(created_at, '%Y-%m') as month,
    COUNT(*) as new_users
FROM users
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY month;

-- Recent activity (last 7 days)
SELECT 
    'Recent Orders' as activity_type,
    COUNT(*) as count
FROM orders
WHERE order_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)

UNION ALL

SELECT 
    'Recent Logins' as activity_type,
    COUNT(*) as count
FROM users
WHERE last_login >= DATE_SUB(NOW(), INTERVAL 7 DAY);

-- 7. Data quality checks
SELECT 'Data Quality Checks' as section;

-- Users without email
SELECT COUNT(*) as users_without_email
FROM users
WHERE email IS NULL OR email = '';

-- Products with zero stock
SELECT name, price, stock_quantity
FROM products
WHERE stock_quantity = 0 AND is_available = 1;

-- Orders without items
SELECT o.id, o.user_id, o.total_amount, o.order_date
FROM orders o
LEFT JOIN order_items oi ON o.id = oi.order_id
WHERE oi.id IS NULL;

-- 8. Performance test queries
SELECT 'Performance Test Queries' as section;

-- Large result set (for testing limits)
SELECT 
    u.username,
    p.name as product_name,
    oi.quantity,
    oi.unit_price,
    o.order_date
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
ORDER BY o.order_date DESC;

-- Complex join with aggregation
SELECT 
    c.name as category,
    COUNT(DISTINCT p.id) as product_count,
    COUNT(DISTINCT oi.order_id) as orders_with_products,
    AVG(p.price) as avg_price,
    SUM(oi.quantity * oi.unit_price) as total_revenue
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id AND o.status != 'cancelled'
GROUP BY c.id, c.name
ORDER BY total_revenue DESC;
