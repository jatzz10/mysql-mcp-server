#!/bin/bash

# MySQL MCP Server Test Database Setup Script
# This script sets up the test database and user for the MySQL MCP Server

set -e

echo "🚀 Setting up MySQL MCP Server Test Database"
echo "============================================="

# Check if MySQL is running
if ! pgrep -x "mysqld" > /dev/null; then
    echo "❌ MySQL server is not running. Please start MySQL first."
    echo "   On macOS with Homebrew: brew services start mysql"
    echo "   On Ubuntu/Debian: sudo systemctl start mysql"
    echo "   On CentOS/RHEL: sudo systemctl start mysqld"
    exit 1
fi

echo "✅ MySQL server is running"

# Get MySQL root password
echo ""
echo "Please enter your MySQL root password:"
read -s MYSQL_ROOT_PASSWORD

# Test connection
echo "🔍 Testing MySQL connection..."
if ! mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT 1;" > /dev/null 2>&1; then
    echo "❌ Failed to connect to MySQL. Please check your password and try again."
    exit 1
fi

echo "✅ MySQL connection successful"

# Run the initialization script
echo "📊 Creating test database and user..."
mysql -u root -p"$MYSQL_ROOT_PASSWORD" < init.sql

echo "✅ Test database setup completed!"

# Create .env file for test
echo "⚙️  Creating .env file for test environment..."
cat > .env << EOF
# MySQL Database Configuration for Test Environment
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=mcp_test
MYSQL_PASSWORD=mcp_test_password
MYSQL_DATABASE=mcp_test_db
EOF

echo "✅ .env file created with test credentials"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Test database details:"
echo "  Database: mcp_test_db"
echo "  User: mcp_test"
echo "  Password: mcp_test_password"
echo "  Host: localhost"
echo "  Port: 3306"
echo ""
echo "Next steps:"
echo "1. Run the server: python3 run_server.py"
echo "2. Test with client: python3 example_client.py"
echo "3. Or test installation: python3 test_installation.py"
echo ""
echo "Sample queries you can try:"
echo "  - List all users: SELECT * FROM users LIMIT 5;"
echo "  - Find active users: SELECT username, email FROM users WHERE is_active = 1;"
echo "  - Get product categories: SELECT c.name, COUNT(p.id) as product_count FROM categories c LEFT JOIN products p ON c.id = p.category_id GROUP BY c.id, c.name;"
echo "  - Recent orders: SELECT o.id, u.username, o.total_amount, o.status FROM orders o JOIN users u ON o.user_id = u.id ORDER BY o.order_date DESC LIMIT 5;"
