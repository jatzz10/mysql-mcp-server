# MySQL MCP Server

A Model Context Protocol (MCP) server that provides read-only access to MySQL databases using SSE (Server-Sent Events) transport.

## Features

- **Read-only access**: Only SELECT queries are allowed for security
- **Multiple tools**: Query data, describe tables, list tables, and get table information
- **SSE transport**: Uses Server-Sent Events for real-time communication over HTTP
- **Environment-based configuration**: Easy setup with environment variables
- **Error handling**: Comprehensive error handling and logging
- **HTTP-based**: Runs as an HTTP server with SSE endpoints

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp env.example .env
   # Edit .env with your MySQL connection details
   ```

## Configuration

Create a `.env` file with your MySQL connection details:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
```

## Usage

### Running the Server

```bash
# Basic usage (default: localhost:3000)
python mysql_mcp_server.py

# Custom host and port
python mysql_mcp_server.py --host 0.0.0.0 --port 8080

# Using the run script
python run_server.py --host localhost --port 3000
```

### Available Tools

1. **query_mysql**: Execute SELECT queries
   - Parameters:
     - `query` (required): SQL SELECT query
     - `limit` (optional): Maximum rows to return (default: 1000)

2. **describe_table**: Get table structure
   - Parameters:
     - `table_name` (required): Name of the table

3. **list_tables**: List all tables in the database
   - Parameters: None

4. **get_table_info**: Get detailed table information
   - Parameters:
     - `table_name` (required): Name of the table

### Example Queries

```python
# Query all users
query_mysql({"query": "SELECT * FROM users"})

# Query with limit
query_mysql({"query": "SELECT name, email FROM users WHERE active = 1", "limit": 100})

# Describe a table
describe_table({"table_name": "users"})

# List all tables
list_tables({})

# Get detailed table info
get_table_info({"table_name": "users"})
```

## Quick Start

### Option 1: Use Test Database (Recommended for testing)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up test database:**
   ```bash
   ./setup_test_db.sh
   ```
   This will create a test user, database, and populate it with sample data.

3. **Test installation:**
   ```bash
   python test_installation.py
   ```

4. **Run the server:**
   ```bash
   python run_server.py
   # Or with custom host/port:
   python run_server.py --host 0.0.0.0 --port 8080
   ```

5. **Test with example client:**
   ```bash
   python example_client.py
   # Or connect to custom server:
   python example_client.py --host localhost --port 3000
   ```

### Option 2: Use Your Own Database

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure database:**
   ```bash
   cp env.example .env
   # Edit .env with your MySQL connection details
   ```

3. **Test installation:**
   ```bash
   python test_installation.py
   ```

4. **Run the server:**
   ```bash
   python run_server.py
   ```

5. **Test with example client:**
   ```bash
   python example_client.py
   ```

## Test Database

The test database includes the following sample data:

- **Users**: 10 sample users with profiles and preferences
- **Products**: 13 products across different categories (electronics, clothing, books, etc.)
- **Categories**: Hierarchical category structure with 11 categories
- **Orders**: 10 sample orders with various statuses
- **Order Items**: Detailed order line items

### Sample Queries

Try these sample queries with the MCP server:

```sql
-- List active users
SELECT username, email, first_name, last_name FROM users WHERE is_active = 1;

-- Get products with categories
SELECT p.name, p.price, c.name as category FROM products p 
LEFT JOIN categories c ON p.category_id = c.id;

-- Recent orders with user details
SELECT o.id, u.username, o.total_amount, o.status, o.order_date 
FROM orders o JOIN users u ON o.user_id = u.id 
ORDER BY o.order_date DESC LIMIT 5;

-- Top customers by spending
SELECT u.username, SUM(o.total_amount) as total_spent 
FROM users u JOIN orders o ON u.id = o.user_id 
WHERE o.status != 'cancelled' 
GROUP BY u.id, u.username 
ORDER BY total_spent DESC LIMIT 5;
```

See `test_queries.sql` for more comprehensive examples.

## Security

- Only SELECT queries are allowed
- No INSERT, UPDATE, DELETE, or DDL operations
- Connection parameters are validated
- Query limits are enforced to prevent large result sets

## Error Handling

The server provides detailed error messages for:
- Connection failures
- Invalid queries
- Missing parameters
- Database errors

## Logging

The server logs important events including:
- Connection establishment
- Query execution
- Errors and warnings

## Requirements

- Python 3.8+
- MySQL database
- Required packages (see requirements.txt)

## License

This project is open source and available under the MIT License.
