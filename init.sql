-- MySQL MCP Server Test Database Setup
-- This script creates a test user, database, and populates it with dummy data

-- Create test user (adjust password as needed)
CREATE USER IF NOT EXISTS 'mcp_test'@'localhost' IDENTIFIED BY 'mcp_test_password';
CREATE USER IF NOT EXISTS 'mcp_test'@'%' IDENTIFIED BY 'mcp_test_password';

-- Create test database
CREATE DATABASE IF NOT EXISTS mcp_test_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Grant privileges to test user
GRANT ALL PRIVILEGES ON mcp_test_db.* TO 'mcp_test'@'localhost';
GRANT ALL PRIVILEGES ON mcp_test_db.* TO 'mcp_test'@'%';
FLUSH PRIVILEGES;

-- Use the test database
USE mcp_test_db;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    profile_data JSON
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT,
    stock_quantity INT DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    metadata JSON
);

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    parent_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipping_address JSON,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Add foreign key constraint for products.category_id
ALTER TABLE products ADD CONSTRAINT fk_products_category 
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL;

-- Insert sample categories
INSERT INTO categories (name, description, parent_id) VALUES
('Electronics', 'Electronic devices and accessories', NULL),
('Clothing', 'Apparel and fashion items', NULL),
('Books', 'Books and educational materials', NULL),
('Home & Garden', 'Home improvement and garden supplies', NULL),
('Sports', 'Sports equipment and accessories', NULL),
('Smartphones', 'Mobile phones and accessories', 1),
('Laptops', 'Portable computers', 1),
('Men\'s Clothing', 'Clothing for men', 2),
('Women\'s Clothing', 'Clothing for women', 2),
('Fiction', 'Fiction books', 3),
('Non-Fiction', 'Non-fiction books', 3);

-- Insert sample users
INSERT INTO users (username, email, first_name, last_name, age, is_active, last_login, profile_data) VALUES
('john_doe', 'john.doe@example.com', 'John', 'Doe', 28, TRUE, '2024-01-15 10:30:00', '{"preferences": {"theme": "dark", "notifications": true}, "bio": "Software developer"}'),
('jane_smith', 'jane.smith@example.com', 'Jane', 'Smith', 32, TRUE, '2024-01-14 15:45:00', '{"preferences": {"theme": "light", "notifications": false}, "bio": "Product manager"}'),
('bob_wilson', 'bob.wilson@example.com', 'Bob', 'Wilson', 45, TRUE, '2024-01-13 09:15:00', '{"preferences": {"theme": "auto", "notifications": true}, "bio": "Marketing director"}'),
('alice_brown', 'alice.brown@example.com', 'Alice', 'Brown', 29, FALSE, '2024-01-10 14:20:00', '{"preferences": {"theme": "dark", "notifications": true}, "bio": "Designer"}'),
('charlie_davis', 'charlie.davis@example.com', 'Charlie', 'Davis', 38, TRUE, '2024-01-12 11:00:00', '{"preferences": {"theme": "light", "notifications": true}, "bio": "Data scientist"}'),
('diana_miller', 'diana.miller@example.com', 'Diana', 'Miller', 26, TRUE, '2024-01-15 16:30:00', '{"preferences": {"theme": "dark", "notifications": false}, "bio": "UX researcher"}'),
('eve_jones', 'eve.jones@example.com', 'Eve', 'Jones', 41, TRUE, '2024-01-14 08:45:00', '{"preferences": {"theme": "auto", "notifications": true}, "bio": "Project manager"}'),
('frank_taylor', 'frank.taylor@example.com', 'Frank', 'Taylor', 33, FALSE, '2024-01-08 13:15:00', '{"preferences": {"theme": "light", "notifications": false}, "bio": "DevOps engineer"}'),
('grace_lee', 'grace.lee@example.com', 'Grace', 'Lee', 30, TRUE, '2024-01-15 12:00:00', '{"preferences": {"theme": "dark", "notifications": true}, "bio": "Frontend developer"}'),
('henry_clark', 'henry.clark@example.com', 'Henry', 'Clark', 52, TRUE, '2024-01-11 17:30:00', '{"preferences": {"theme": "light", "notifications": true}, "bio": "Senior architect"}');

-- Insert sample products
INSERT INTO products (name, description, price, category_id, stock_quantity, is_available, metadata) VALUES
('iPhone 15 Pro', 'Latest iPhone with advanced camera system', 999.99, 6, 25, TRUE, '{"brand": "Apple", "model": "iPhone 15 Pro", "storage": "256GB", "color": "Natural Titanium"}'),
('MacBook Pro 16"', 'Powerful laptop for professionals', 2499.99, 7, 15, TRUE, '{"brand": "Apple", "model": "MacBook Pro", "screen_size": "16-inch", "processor": "M3 Pro"}'),
('Samsung Galaxy S24', 'Android flagship smartphone', 799.99, 6, 30, TRUE, '{"brand": "Samsung", "model": "Galaxy S24", "storage": "128GB", "color": "Onyx Black"}'),
('Dell XPS 13', 'Ultrabook with stunning display', 1299.99, 7, 20, TRUE, '{"brand": "Dell", "model": "XPS 13", "screen_size": "13.4-inch", "processor": "Intel i7"}'),
('Nike Air Max 270', 'Comfortable running shoes', 150.00, 5, 50, TRUE, '{"brand": "Nike", "model": "Air Max 270", "size_range": "7-12", "color": "White/Black"}'),
('Adidas Ultraboost 22', 'High-performance running shoes', 180.00, 5, 40, TRUE, '{"brand": "Adidas", "model": "Ultraboost 22", "size_range": "7-13", "color": "Core Black"}'),
('The Great Gatsby', 'Classic American novel', 12.99, 10, 100, TRUE, '{"author": "F. Scott Fitzgerald", "isbn": "978-0-7432-7356-5", "pages": 180}'),
('Clean Code', 'Programming best practices guide', 39.99, 11, 75, TRUE, '{"author": "Robert C. Martin", "isbn": "978-0-13-235088-4", "pages": 464}'),
('Design Patterns', 'Gang of Four design patterns', 49.99, 11, 60, TRUE, '{"author": "Gang of Four", "isbn": "978-0-201-63361-0", "pages": 395}'),
('Men\'s Cotton T-Shirt', 'Comfortable everyday t-shirt', 19.99, 8, 200, TRUE, '{"material": "100% Cotton", "sizes": "S-XXL", "color": "White"}'),
('Women\'s Summer Dress', 'Light and breezy summer dress', 45.99, 9, 80, TRUE, '{"material": "Polyester", "sizes": "XS-L", "color": "Floral Print"}'),
('Garden Hose 50ft', 'Heavy-duty garden hose', 29.99, 4, 25, TRUE, '{"length": "50 feet", "material": "Rubber", "diameter": "5/8 inch"}'),
('LED Plant Grow Light', 'Full spectrum LED grow light', 89.99, 4, 15, TRUE, '{"power": "45W", "coverage": "2x2 feet", "spectrum": "Full spectrum"}');

-- Insert sample orders
INSERT INTO orders (user_id, total_amount, status, order_date, shipping_address, notes) VALUES
(1, 999.99, 'delivered', '2024-01-10 14:30:00', '{"street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001"}', 'Please leave at front door'),
(2, 1299.99, 'shipped', '2024-01-12 09:15:00', '{"street": "456 Oak Ave", "city": "Los Angeles", "state": "CA", "zip": "90210"}', 'Signature required'),
(3, 150.00, 'processing', '2024-01-14 16:45:00', '{"street": "789 Pine Rd", "city": "Chicago", "state": "IL", "zip": "60601"}', 'Gift wrapping requested'),
(1, 52.98, 'pending', '2024-01-15 11:20:00', '{"street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001"}', ''),
(5, 89.99, 'delivered', '2024-01-08 13:10:00', '{"street": "321 Elm St", "city": "Houston", "state": "TX", "zip": "77001"}', ''),
(6, 225.98, 'shipped', '2024-01-13 10:30:00', '{"street": "654 Maple Dr", "city": "Phoenix", "state": "AZ", "zip": "85001"}', 'Fragile items'),
(7, 39.99, 'delivered', '2024-01-09 15:45:00', '{"street": "987 Cedar Ln", "city": "Philadelphia", "state": "PA", "zip": "19101"}', ''),
(9, 2499.99, 'processing', '2024-01-15 08:00:00', '{"street": "147 Birch St", "city": "San Antonio", "state": "TX", "zip": "78201"}', 'Business address'),
(10, 65.98, 'pending', '2024-01-15 17:30:00', '{"street": "258 Spruce Ave", "city": "San Diego", "state": "CA", "zip": "92101"}', ''),
(4, 19.99, 'cancelled', '2024-01-11 12:15:00', '{"street": "369 Willow Way", "city": "Dallas", "state": "TX", "zip": "75201"}', 'Customer requested cancellation');

-- Insert sample order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 999.99),
(2, 4, 1, 1299.99),
(3, 5, 1, 150.00),
(4, 7, 1, 12.99),
(4, 8, 1, 39.99),
(5, 12, 1, 89.99),
(6, 5, 1, 150.00),
(6, 6, 1, 180.00),
(7, 8, 1, 39.99),
(8, 2, 1, 2499.99),
(9, 7, 1, 12.99),
(9, 8, 1, 39.99),
(9, 9, 1, 49.99),
(10, 10, 1, 19.99);

-- Create some indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_active ON users(is_active);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_available ON products(is_available);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);

-- Display summary
SELECT 'Database setup completed successfully!' as message;
SELECT COUNT(*) as total_users FROM users;
SELECT COUNT(*) as total_products FROM products;
SELECT COUNT(*) as total_categories FROM categories;
SELECT COUNT(*) as total_orders FROM orders;
SELECT COUNT(*) as total_order_items FROM order_items;
